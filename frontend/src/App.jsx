
import { useState } from "react";
import * as SpeechSDK from
  "microsoft-cognitiveservices-speech-sdk";

import "./App.css";

function App() {

  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState("Ready");
  const [input, setInput] = useState("");

  const history = messages.map(m => ({
    role: m.role,
    content: m.text
  }));

  async function getSpeechConfig() {
    const res = await fetch(
      "http://127.0.0.1:8000/speech-token"
    );

    if (!res.ok) throw new Error("Speech token failed");

    const data = await res.json();

    const config =
      SpeechSDK.SpeechConfig.fromAuthorizationToken(
        data.token,
        data.region
      );

    config.speechSynthesisVoiceName = "en-US-AvaNeural";
    config.speechRecognitionLanguage = "en-IN";

    return config;
  }

  async function speak(text) {
    const config = await getSpeechConfig();

    const speaker =
      new SpeechSDK.SpeechSynthesizer(config);

    return new Promise((resolve, reject) => {
      speaker.speakTextAsync(
        text,
        result => {
          speaker.close();

          if (result.reason ===
              SpeechSDK.ResultReason.SynthesizingAudioCompleted) {
            resolve();
          } else {
            reject(new Error("Speech synthesis failed"));
          }
        },
        error => {
          speaker.close();
          reject(new Error(error));
        }
      );
    });
  }

  async function sendMessage(text) {

    if (!text.trim()) return;

    const userMessage = {
      role: "user",
      text
    };

    const updated = [...messages, userMessage];

    setMessages(updated);
    setInput("");
    setStatus("Thinking...");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            message: text,
            history: history
          })
        }
      );

      if (!response.ok) {
        throw new Error("AI request failed");
      }

      const data = await response.json();

      setMessages([
        ...updated,
        { role: "assistant", text: data.reply }
      ]);

      setStatus("Speaking...");
      await speak(data.reply);

      setStatus("Ready");

    } catch (error) {
      console.error(error);
      setStatus("Something went wrong");
    }
  }

  async function startListening() {

    try {
      setStatus("Listening...");

      const config = await getSpeechConfig();

      const audio =
        SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();

      const recognizer =
        new SpeechSDK.SpeechRecognizer(config, audio);

      recognizer.recognizeOnceAsync(
        async result => {

          recognizer.close();

          if (result.reason ===
              SpeechSDK.ResultReason.RecognizedSpeech) {

            await sendMessage(result.text);

          } else {
            setStatus("No speech detected");
          }
        },
        error => {
          console.error(error);
          recognizer.close();
          setStatus("Microphone error");
        }
      );

    } catch (error) {
      console.error(error);
      setStatus("Unable to start microphone");
    }
  }

  return (
    <div className="app">

      <h1>AURA</h1>
      <p>Your personal Azure AI assistant</p>

      <div className="orb">
        <button onClick={startListening}>
          🎙️
        </button>
      </div>

      <h3>{status}</h3>

      <div className="chat">
        {messages.map((msg, index) => (
          <div key={index} className={msg.role}>
            <strong>{msg.role === "user"
              ? "You" : "AURA"}</strong>
            <p>{msg.text}</p>
          </div>
        ))}
      </div>

      <form onSubmit={e => {
        e.preventDefault();
        sendMessage(input);
      }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask AURA anything..."
        />
        <button type="submit">Send</button>
      </form>

    </div>
  );
}

export default App;
