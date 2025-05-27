import google.generativeai as genai
import os
from dotenv import load_dotenv
import pyttsx3 # <-- Tambahkan import pyttsx3

# Muat variabel lingkungan dari file .env
load_dotenv()

# Ambil API key dari environment variable
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY tidak ditemukan. Pastikan sudah diatur di file .env")
else:
    try:
        # Konfigurasi API key
        genai.configure(api_key=api_key)

        # Inisialisasi model Generative
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

        # Kirim prompt (pertanyaan) ke Gemini
        prompt_text = "Halo Gemini! Apa kabar hari ini?" # Prompt bisa diganti lagi
        print(f"Mengirim prompt: {prompt_text}")

        response = model.generate_content(prompt_text)

        # Cetak dan ucapkan respons dari Gemini
        if response.text:
            print("\nRespons Gemini (teks):")
            print(response.text)

            # --- BAGIAN TTS DENGAN pyttsx3 DIMULAI DI SINI ---
            print("\nMencoba mengubah teks menjadi suara dengan pyttsx3...")
            try:
                # Inisialisasi engine pyttsx3
                engine = pyttsx3.init()
                
                # (Opsional) Anda bisa mengatur properti suara di sini jika mau
                # voices = engine.getProperty('voices')
                # engine.setProperty('voice', voices[0].id) # Coba suara berbeda jika ada
                # engine.setProperty('rate', 150) # Atur kecepatan bicara

                # Ucapkan teksnya
                engine.say(response.text)
                
                # Tunggu sampai semua ucapan selesai
                engine.runAndWait()
                print("Selesai mengucapkan.")

            except Exception as e_tts:
                print(f"Error saat TTS dengan pyttsx3: {e_tts}")
            # --- BAGIAN TTS SELESAI ---

        else:
            print("Tidak ada respons teks dari Gemini.")
            if response.prompt_feedback:
                 print(f"Prompt Feedback: {response.prompt_feedback}")

    except Exception as e:
        print(f"Terjadi kesalahan dengan Gemini API: {e}")