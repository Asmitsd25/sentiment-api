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
positive_words = [
    "love","like","enjoy","happy","joy","glad","pleased",
    "great","good","excellent","amazing","awesome",
    "wonderful","fantastic","best","perfect","brilliant",
    "outstanding","superb","beautiful","nice","cool",
    "fun","success","successful","win","won","better",
    "favorite","favourite","recommend","excited",
    "thrilled","delighted","positive","smile",
    "thank","thanks","helpful","helped","works",
    "working","valuable","useful","impressive",
    "incredible","remarkable","satisfied"
]

negative_words = [
    "hate","sad","bad","awful","terrible","horrible",
    "worst","poor","angry","upset","frustrated",
    "annoyed","disappointed","disappointing",
    "negative","disgusting","pathetic","useless",
    "problem","issue","fail","failed","failure",
    "broken","bug","bugs","error","errors",
    "wrong","complaint","pain","regret"
]

pos = sum(word in text for word in positive_words)
neg = sum(word in text for word in negative_words)

if pos > 0 and pos >= neg:
    return "happy"

if neg > pos:
    return "sad"

return "neutral"
```


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
