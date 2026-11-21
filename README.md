# AURA

An AI-powered voice assistant built and hosted entirely on Microsoft Azure, combining speech recognition, generative AI, and neural text-to-speech to deliver a natural conversational experience.


## Overview

**AURA is a browser-based AI voice assistant designed to understand spoken commands, generate intelligent responses, and communicate naturally through voice.

The project integrates Microsoft's Azure AI services with a Python backend and a web-based frontend to create an end-to-end conversational AI application.

The primary objective is to explore practical AI application development, cloud deployment, speech processing, and integration of generative AI models.

## Key Features

- **Voice Input:** Convert spoken language into text using Azure AI Speech.
- **AI-Powered Responses:** Generate contextual responses using a model deployed through Microsoft Foundry.
- **Text-to-Speech:** Convert AI-generated responses into natural-sounding speech.
- **Text Chat:** Interact with AURA without using a microphone.
- **Conversation History:** Maintain conversational context across messages.
- **Web Interface:** Access the assistant through a browser.
- **Multilingual Support:** Planned support for English and Hindi.
- **Cloud Deployment:** Host the application and its AI services on Microsoft Azure.

## Architecture

```text
              USER
                |
                v
        Web Application
          (React + Vite)
                |
          Voice / Text
                |
                v
        FastAPI Backend
        (Azure App Service)
                |
        +-------+--------+
        |                |
        v                v
  Azure AI Speech   Microsoft Foundry
        |                |
   Speech-to-Text    Generative AI
        |                |
        |           AI Response
        |                |
        +-------+--------+
                |
                v
         Text-to-Speech
                |
                v
         Audio Response
                |
                v
              USER
```

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | React.js, Vite |
| Backend | Python, FastAPI |
| AI Model | Microsoft Foundry |
| Speech Recognition | Azure AI Speech |
| Speech Synthesis | Azure AI Speech |
| API Communication | REST API |
| Cloud Hosting | Azure App Service |
| Cloud Environment | Microsoft Azure |
| Version Control | Git and GitHub |

## Azure Infrastructure

The project uses the following Azure resources:

| Azure Resource | Purpose | Planned Region |
|---|---|---|
| Azure AI Speech | Speech recognition and synthesis | Central India |
| Microsoft Foundry | Generative AI model deployment | South India |
| Azure App Service | Hosting frontend and backend | Central India, subject to availability |
| Azure Resource Group | Resource management | Central India |

**Note:** The Foundry region is separate from the Speech region because model availability depends on regional deployment support. The selected model and deployment type must be verified in the Foundry model catalog.

## Project Structure

```text
AURA/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── static/
│   └── .env.example
│
├── .gitignore
└── README.md
```

## How It Works

### 1. Speech Recognition
The user speaks through their browser microphone. Azure AI Speech processes the audio and converts it into text.

### 2. AI Processing
The recognized text is sent to the FastAPI backend, which communicates with the deployed generative AI model through Microsoft Foundry.

### 3. Response Generation
The AI model generates a response using the current message and relevant conversation history.

### 4. Speech Synthesis
The generated response is converted into audio using Azure AI Speech.

### 5. User Interaction
The browser plays the generated audio and displays the response as text.

## Installation and Setup

### Prerequisites

- Microsoft Azure account
- Azure AI Speech resource
- Microsoft Foundry project
- Deployed chat model
- Python 3.11 or another supported App Service runtime
- Node.js and npm
- Git

### 2. Set Up the Backend

```bash
cd backend

python -m venv venv
```

Activate the environment:

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the backend directory.

```env
SPEECH_KEY=your_azure_speech_key
SPEECH_REGION=centralindia

FOUNDRY_API_KEY=your_foundry_api_key
FOUNDRY_OPENAI_ENDPOINT=your_foundry_endpoint
FOUNDRY_MODEL_DEPLOYMENT=your_model_deployment_name
```

**Security:** Never upload `.env` files, API keys, or credentials to GitHub. Use Azure App Service application settings or Azure Key Vault for deployed applications.

### 4. Start the Backend

```bash
uvicorn main:app --reload
```

Backend development server:

```text
http://127.0.0.1:8000
```

### 5. Set Up the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm install microsoft-cognitiveservices-speech-sdk
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

### Production Security

- Keep permanent API keys on the backend.
- Use short-lived Speech authorization tokens for browser access.
- Store secrets in Azure Key Vault where appropriate.
- Enable HTTPS.
- Configure application monitoring through Azure Application Insights.

## Future Enhancements

- Multilingual voice conversations.
- Continuous voice interaction.
- Wake-word detection.
- Conversation memory.
- Custom AI personalities.
- Tool calling and external API integrations.
- User authentication and personalized settings.
- Improved real-time speech interaction.

## Learning Objectives

This project explores:

- Integrating generative AI models into real-world applications.
- Working with cloud-based speech recognition and synthesis.
- Building REST APIs using FastAPI.
- Developing interactive interfaces using React.
- Managing cloud resources through Microsoft Azure.
- Deploying and securing AI-powered applications.

## Project Status

**Status:** Initial development and Azure infrastructure setup.

The project is being developed incrementally, beginning with speech recognition, AI response generation, and speech synthesis before expanding into advanced assistant capabilities.
