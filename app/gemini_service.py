import google.generativeai as genai
from app.config import SYSTEM_PROMPT # <-- BARU: Import SYSTEM_PROMPT dari config.py

DEFAULT_MODEL_NAME = 'models/gemini-1.5-flash-latest' 

_model_instance = None 
_chat_session = None   

def init_chat_session(model_name=DEFAULT_MODEL_NAME):
    """Menginisialisasi model Gemini dan memulai sesi chat baru dengan system prompt."""
    global _model_instance, _chat_session
    try:
        if _model_instance is None: 
             _model_instance = genai.GenerativeModel(
                 model_name=model_name,
                 system_instruction=SYSTEM_PROMPT # <-- BARU: Tambahkan system_instruction
             )

        _chat_session = _model_instance.start_chat(history=[]) 
        print(">>> Sesi chat dengan Gemini berhasil dimulai (riwayat percakapan dan persona aktif).")
        return True
    except Exception as e:
        print(f"Error saat memulai sesi chat Gemini: {e}")
        _chat_session = None 
        return False

def get_chat_response(prompt_text):
    """Mengirim prompt ke sesi chat yang sedang berjalan dan mendapatkan respons."""
    global _chat_session
    if not _chat_session:
        print("Error: Sesi chat belum diinisialisasi. Panggil init_chat_session() dulu.")
        return "Maaf, sesi chat belum siap. Coba mulai ulang."

    try:
        response = _chat_session.send_message(prompt_text)

        if response.text:
            return response.text
        else:
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                print(f"Gemini Prompt Feedback: {response.prompt_feedback}")
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'finish_reason') and candidate.finish_reason != 'STOP':
                        print(f"Kandidat dihentikan karena: {candidate.finish_reason}")

            return "Maaf, saya tidak mendapatkan respons teks yang diharapkan dari Gemini."
    except Exception as e:
        print(f"Error saat mengirim pesan ke Gemini dalam sesi chat: {e}")
        return f"Maaf, terjadi kesalahan saat berkomunikasi dengan Gemini: {str(e)}"