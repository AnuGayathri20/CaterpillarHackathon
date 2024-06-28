import google.generativeai as genai
import os
from middleware import FirebaseAuthMiddleware
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI

app=FastAPI()

app.add_middleware(FirebaseAuthMiddleware)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')


async def getChat():
    chat = model.start_chat(history=[])
    return chat


@app.post("/summarize")
async def summarize(body):
    chat=await getChat()
    response=chat.send_message(str(body.text)+"Summarize this and return the same in 5 languages")
    return response.text