from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import requests

# We use dotenv to load environment variables
# from the .env file
from dotenv import load_dotenv

import os


# Load variables from .env file
load_dotenv()

# Access API key from .env file
api_key = os.getenv("MY_API")

# Why use .env files?
# 1. To keep API keys secure
# 2. To avoid exposing secret keys in code
# 3. To make projects safer and production-ready


app = FastAPI()

# Enable CORS so frontend can connect to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request body model
class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):

    user_message = request.message

    # OpenRouter API URL
    url = "https://openrouter.ai/api/v1/chat/completions"

    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Request body
    payload = {
        "model": "openai/gpt-3.5-turbo",

        "messages": [
            {
                "role": "system",
                "content": "Tum ek highly energetic aur strict Fitness Coach ho. Tumhara naam Rocky hai. Tumhe logo ko motivate karna hai aur aalsi logo par thoda gussa bhi karna hai. Rule 1: Apne jawab ko hamesha chote sentences mei rakho. Rule 2: Important baaton ko bullet points aur bold text mei highlight karo. Rule 3: Har message mei kam se kam 2 fitness emojis ka use karo. "
                
                
                
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    # Send request to OpenRouter
    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    data = response.json()

    # Extract AI response
    ai_reply = data["choices"][0]["message"]["content"]

    # Return response to frontend
    return {
        "reply": ai_reply
    }