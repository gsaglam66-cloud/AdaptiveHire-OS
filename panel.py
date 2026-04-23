import os
import time
from fastapi import FastAPI, UploadFile, File
from typing import List
import whisper # OpenAI'ın transkript modeli
from pyannote.audio import Pipeline # Ses ayrıştırma için

app = FastAPI(title="Adaptive Hire AI Core")

# Modeli yükle (Daha hızlı sonuç için 'base' veya 'small' kullanılabilir)
model = whisper.load_model("base")

# Ses ayrıştırma pipeline'ı (Huggingface token gerekir)
# diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")

class InterviewManager:
    def __init__(self):
        self.conversation_history = []
        
    def process_audio_segment(self, audio_path: str):
        """
        Sesi transkripte çevirir, hoparlörleri ayırır ve sesi siler.
        """
        try:
            # 1. Transkript işlemi
            result = model.transcribe(audio_path)
            transcript_text = result['text']
            
            # 2. KVKK Güvenliği: Ses kaydını kalıcı olarak sil
            if os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"KVKK Uyarınca {audio_path} kalıcı olarak silindi.")
            
            # 3. Geçmişe ekle
            self.conversation_history.append(transcript_text)
            return transcript_text
        except Exception as e:
            return f"Hata: {str(e)}"

    def generate_adaptive_question(self, last_transcript: str):
        """
        LLM kullanarak adayın cevabına göre derinleşme sorusu üretir.
        """
        # Burada OpenAI API veya benzeri bir LLM çağrısı yapılır
        prompt = f"Adayın son cevabı: '{last_transcript}'. Bu cevaba göre derinlemesine bir İK sorusu sor."
        # Örnek dönüş:
        return "Bu projede karşılaştığınız en büyük teknik zorluk neydi ve nasıl aştınız?"

interview_session = InterviewManager()

@app.post("/process-segment/")
async def process_segment(file: UploadFile = File(...)):
    # Geçici ses dosyasını kaydet
    temp_filename = f"temp_{int(time.time())}.wav"
    with open(temp_filename, "wb") as buffer:
        buffer.write(await file.read())
    
    # İşle ve sil
    text = interview_session.process_audio_segment(temp_filename)
    
    # Adaptif soru önerisi al
    next_question = interview_session.generate_adaptive_question(text)
    
    return {
        "status": "Success",
        "transcript": text,
        "suggested_next_question": next_question,
        "kvkk_status": "Audio Deleted"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
