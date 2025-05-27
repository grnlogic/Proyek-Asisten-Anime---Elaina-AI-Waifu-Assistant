import os
from dotenv import load_dotenv
import google.generativeai as genai

def load_config():
    """Memuat konfigurasi dan API key."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Error: GEMINI_API_KEY tidak ditemukan. Pastikan sudah diatur di file .env")

    try:
        genai.configure(api_key=api_key)
        print("Konfigurasi Gemini API berhasil.")
    except Exception as e:
        raise ConnectionError(f"Gagal mengkonfigurasi Gemini API: {e}")

    return api_key