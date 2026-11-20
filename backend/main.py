import logging
import os
from typing import Literal

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

logger = logging.getLogger("aura")

app = FastAPI(title="AURA AI Assistant")

# FIX: allow both hostnames Vite can be opened on
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def require_env(*names: str) -> dict:
    """Return env vars, or raise a clear 500 naming the missing ones."""
    values = {n: os.getenv(n) for n in names}
    missing = [n for n, v in values.items() if not v]
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Missing environment variables in backend/.env: {', '.join(missing)}",
        )
    return values


_client = None


def get_client() -> OpenAI:
    # FIX: created lazily so the server still starts (and /  works) with an
    # empty .env, and the error is reported clearly when /chat is called.
    global _client
    if _client is None:
        env = require_env("FOUNDRY_API_KEY", "FOUNDRY_OPENAI_ENDPOINT")
        _client = OpenAI(
            api_key=env["FOUNDRY_API_KEY"],
            base_url=env["FOUNDRY_OPENAI_ENDPOINT"],
        )
    return _client


@app.get("/")
def home():
    return {"message": "AURA backend is running!"}


@app.get("/speech-token")
def speech_token():
    env = require_env("SPEECH_KEY", "SPEECH_REGION")
    region = env["SPEECH_REGION"]

    # FIX: network errors used to raise an unhandled exception -> bare 500
    # (no CORS header, so the browser showed a misleading CORS error).
    try:
        response = requests.post(
            f"https://{region}.api.cognitive.microsoft.com/sts/v1.0/issueToken",
            headers={"Ocp-Apim-Subscription-Key": env["SPEECH_KEY"]},
            timeout=10,
        )
    except requests.RequestException as e:
        logger.exception("Speech token request failed")
        raise HTTPException(status_code=502, detail=f"Could not reach Azure Speech: {e}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Azure Speech rejected the key/region (HTTP {response.status_code})",
        )

    return {"token": response.text, "region": region}


# FIX: history was an untyped `list`, so any junk (or a bad role) went straight
# to the model API and came back as a confusing 500.
class HistoryItem(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[HistoryItem] = []


@app.post("/chat")
def chat(data: ChatRequest):
    env = require_env("FOUNDRY_MODEL_DEPLOYMENT")

    messages = [
        {
            "role": "system",
            "content": (
                "You are AURA, a helpful AI voice assistant. "
                "Give concise, natural and conversational answers. "
                "Avoid unnecessary formatting."
            ),
        }
    ]
    messages.extend(h.model_dump() for h in data.history[-10:])
    messages.append({"role": "user", "content": data.message})

    try:
        response = get_client().chat.completions.create(
            model=env["FOUNDRY_MODEL_DEPLOYMENT"],
            messages=messages,
            # FIX: newer Foundry/Azure models (gpt-5, o-series) reject
            # `max_tokens` and a non-default `temperature` with a 400.
            max_completion_tokens=500,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Chat completion failed")
        raise HTTPException(status_code=502, detail=f"AI request failed: {e}")

    return {"reply": response.choices[0].message.content or ""}
