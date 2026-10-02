import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import json
from prompt import build_prompt
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY", ""),
    base_url="https://api.deepseek.com"
)

class ResumeRequest(BaseModel):
    resume: str
    jd: str = ""

@app.post("/diagnose")
def diagnose(req: ResumeRequest):
    prompt = build_prompt(req.resume, req.jd)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content.strip()

    # 清理可能的markdown包裹
    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        content = content.rsplit("```", 1)[0]

    try:
        result = json.loads(content)
    except json.JSONDecodeError:
        return {"error": "AI返回格式错误", "raw": content}

    return result