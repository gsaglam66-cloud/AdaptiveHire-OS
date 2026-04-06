# Temel kütüphanelerin kurulumu gerekecek: pip install fastapi uvicorn openai
from fastapi import FastAPI, UploadFile, File
import openai

app = FastAPI()

@app.post("/mulakat/transkript")
async def transcribe_audio(file: UploadFile = File(...)):
    # Ses dosyası geçici olarak işlenir ama kaydedilmez
    # OpenAI Whisper API kullanılarak ses yazıya çevrilir
    response = openai.Audio.transcribe("whisper-1", file.file)
    return {"text": response["text"]}

@app.post("/mulakat/analiz")
async def analyze_interview(transcript: str):
    # GPT-4 modeli metni analiz eder ve puanlama yapar
    analysis = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Sen bir İK uzmanısın. Metni puanla."},
                  {"role": "user", "content": transcript}]
    )
    return {"report": analysis.choices[0].message.content}
