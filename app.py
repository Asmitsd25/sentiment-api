from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

def classify(text: str) -> str:
    text = text.lower()

    happy_words = [
        "love","great","excellent","amazing","awesome",
        "good","happy","wonderful","fantastic","best",
        "like","enjoy"
    ]

    sad_words = [
        "hate","terrible","awful","bad","sad",
        "worst","poor","horrible","angry",
        "disappointed","disappointing"
    ]

    if any(word in text for word in happy_words):
        return "happy"

    if any(word in text for word in sad_words):
        return "sad"

    return "neutral"

@app.post("/sentiment")
async def sentiment(req: SentimentRequest):
    return {
        "results": [
            {
                "sentence": s,
                "sentiment": classify(s)
            }
            for s in req.sentences
        ]
    }
