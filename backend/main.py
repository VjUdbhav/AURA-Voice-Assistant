
import os
import requests

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()

app = FastAPI(title="AURA AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Microsoft Foundry client
client = OpenAI(
    api_key=os.getenv("FOUNDRY_API_KEY"),
    base_url=os.getenv("FOUNDRY_OPENAI_ENDPOINT")
)

MODEL = os.getenv("FOUNDRY_MODEL_DEPLOYMENT")


@app.get("/")
def home():
    return {"message": "AURA backend is running!"}


# Generate a temporary Azure Speech token
@app.get("/speech-token")
def speech_token():

    key = os.getenv("SPEECH_KEY")
    region = os.getenv("SPEECH_REGION")

    response = requests.post(
        f"https://{region}.api.cognitive.microsoft.com/sts/v1.0/issueToken",
        headers={"Ocp-Apim-Subscription-Key": key},
        timeout=10
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate Speech token"
        )

    return {
        "token": response.text,
        "region": region
    }


class ChatRequest(BaseModel):
    message: str
    history: list = []


@app.post("/chat")
def chat(data: ChatRequest):

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are AURA, a helpful AI voice assistant. "
                    "Give concise, natural and conversational answers. "
                    "Avoid unnecessary formatting."
                )
            }
        ]

        # Add previous conversation
        messages.extend(data.history[-10:])

        messages.append({
            "role": "user",
            "content": data.message
        })

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        answer = response.choices[0].message.content

        return {"reply": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
