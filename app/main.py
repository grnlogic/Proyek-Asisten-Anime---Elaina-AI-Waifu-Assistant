# app/main.py

# --- AWAL KODE PENEKAN ERROR ALSA ---
import ctypes
import platform # Untuk mengecek sistem operasi
import emoji # Untuk menghapus emoji dari input teks

# Hanya coba implementasi ini jika berjalan di sistem Linux
if platform.system() == 'Linux':
    try:
        # Definisikan tipe fungsi C untuk error handler ALSA
        # Signature: void handler(const char *file, int line, const char *function, int err, const char *format, ...)
        ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(
            None,  # Return type: void
            ctypes.c_char_p,  # const char *file
            ctypes.c_int,     # int line
            ctypes.c_char_p,  # const char *function
            ctypes.c_int,     # int err
            ctypes.c_char_p   # const char *format (va_list ...)
        )

        # Fungsi Python yang akan menjadi error handler baru (tidak melakukan apa-apa)
        def py_error_handler(filename, line, function, err, fmt):
            pass
        
        # Buat C callable function pointer dari fungsi Python kita
        c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

        # Muat library ALSA (libasound.so.2)
        asound = ctypes.cdll.LoadLibrary('libasound.so.2')
        
        # Set error handler ALSA ke fungsi kustom kita
        asound.snd_lib_error_set_handler(c_error_handler)
        
        print(">>> Penangan error ALSA diatur untuk senyap (pesan error ALSA dari C library tidak akan ditampilkan).")
    
    except (OSError, AttributeError) as e_alsa_suppress:
        print(f">>> Gagal mengatur penangan error ALSA untuk senyap: {e_alsa_suppress}")
        print("    Pesan error ALSA mungkin masih akan muncul.")
        pass
# --- AKHIR KODE PENEKAN ERROR ALSA ---

# Import yang benar
from app.config_loader import load_config
from app.gemini_service import get_chat_response, init_chat_session 
from app.tts_service import speak_text, init_tts_engine
from app.stt_service import dengarkan_suara

def hapus_emoji(text): # Definisi fungsi jika di main.py
    if text is None:
        return None
    return emoji.replace_emoji(text, replace='')

def run_assistant():
    try:
        # 1. Muat konfigurasi
        load_config()

        # 2. Inisialisasi sesi chat Gemini
        if not init_chat_session():
            print("Tidak bisa menginisialisasi sesi chat Gemini. Program berhenti.")
            return

        # 3. Inisialisasi engine TTS
        tts_engine = init_tts_engine()
        if not tts_engine:
            print("Tidak bisa melanjutkan tanpa engine TTS. Program berhenti.")
            return

        print("Halo Fajar!, Ada yang bisa saya bantu hari ini?")
        speak_text("Halo Fajar!, Ada yang bisa saya bantu hari ini?")

        while True:
            # 4. Dapatkan input dari pengguna melalui suara
            user_input = dengarkan_suara()

            if user_input: # Jika ada teks hasil STT
                if user_input.lower() == "stop":
                    farewell_message = "Baik, sampai jumpa lagi!"
                    print(f"Asisten: {farewell_message}")
                    speak_text(farewell_message)
                    break

                # 5. Dapatkan respons dari Gemini dengan memori chat
                print(f"\nAsisten: (Sedang memikirkan jawaban untuk: '{user_input}')...")
                gemini_answer = get_chat_response(user_input)
                print(f"Asisten (teks): {gemini_answer}")

                # 6. Ucapkan respons Gemini
                speak_text(gemini_answer)
            else:
                print("Tidak ada input suara yang valid terdeteksi atau tidak dimengerti. Saya mendengarkan lagi...")

    except ValueError as ve:
        print(ve)
    except ConnectionError as ce:
        print(ce)
    except Exception as e:
        print(f"Terjadi kesalahan tak terduga di aplikasi utama: {e}")

if __name__ == "__main__":
    run_assistant()