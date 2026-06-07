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

```
positive = {
    "love","loved","like","liked","enjoy","enjoyed",
    "good","great","excellent","amazing","awesome",
    "wonderful","fantastic","best","happy","joy",
    "joyful","delighted","thrilled","excited",
    "perfect","brilliant","outstanding","superb",
    "pleased","positive","nice","beautiful",
    "fun","funny","cool","success","successful",
    "win","won","better","favorite","favourite",
    "glad","smile","recommend"
}

negative = {
    "sad","unhappy","bad","terrible","awful",
    "hate","hated","horrible","worst","poor",
    "angry","upset","disappointed","disappointing",
    "frustrated","annoyed","negative","disgusting",
    "pathetic","useless","problem","issue","fail",
    "failed","failure","boring","broken","bug",
    "bugs","error","errors","wrong","nasty",
    "complaint","complain","pain","regret"
}

pos = sum(1 for w in positive if w in text)
neg = sum(1 for w in negative if w in text)

if pos > neg:
    return "happy"
if neg > pos:
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
