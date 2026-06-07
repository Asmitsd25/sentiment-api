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
        "love", "loved", "like", "liked", "enjoy", "enjoyed",
        "good", "great", "excellent", "amazing", "awesome",
        "wonderful", "fantastic", "best", "happy", "joy",
        "joyful", "delighted", "thrilled", "excited",
        "perfect", "brilliant", "outstanding", "superb",
        "pleased", "positive", "nice"
    ]

    sad_words = [
        "sad", "unhappy", "bad", "terrible", "awful",
        "hate", "hated", "horrible", "worst", "poor",
        "angry", "upset", "disappointed", "disappointing",
        "frustrated", "annoyed", "negative", "disgusting",
        "pathetic", "useless", "problem", "issue", "fail",
        "failed", "failure"
    ]

    happy_score = sum(word in text for word in happy_words)
    sad_score = sum(word in text for word in sad_words)

    if happy_score > sad_score:
        return "happy"

    if sad_score > happy_score:
        return "sad"

    return "neutral"

@app.get("/")
def root():
    return {"status": "ok"}

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
