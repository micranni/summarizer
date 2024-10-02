from groq import Groq
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator
import os
import re

app = FastAPI()

client = Groq(
    api_key= os.environ.get("GROQ_API_KEY")
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

class RequestModel(BaseModel):
    message: str

    @field_validator("message")
    def format_input(cls, value):
        value = value.replace('"', '\\"').replace("'", "\\'")
        
        # Optionally sanitize to remove other unwanted characters
        sanitized_value = re.sub(r'[^\w\s-]', '', value)
        
        return sanitized_value.capitalize()

class ResponseModel(BaseModel):
    response: str

@app.get("/")
async def read_root(request: Request):
    context = {"request": request, "title": "Home Page", "message": "Welcome to FastAPI with Jinja2!"}
    return templates.TemplateResponse("index.html", context)

@app.post("/summarize", response_model=ResponseModel)
def summarize_post(request: RequestModel):
    system_message="You are a great summarizer. Summarize the following text based on the most important information. Only include the summary in your response. Do not describe the text, simply summarize it."

    summary = client.chat.completions.create(
        messages=[
            {"role":"system",
             "content":system_message},
             {"role":"user",
              "content": request.message}
        ],
        model="llama3-8b-8192",
        temperature=0,
        max_tokens=8192    
        )

    response_message = summary.choices[0].message.content
    print(response_message)
    return ResponseModel(response=response_message)


