# app/stt_service.py
import speech_recognition as sr
import ctypes
import os
import platform

# Suppress ALSA error messages on Linux
if platform.system() == 'Linux':
    try:
        ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)
        
        def py_error_handler(filename, line, function, err, fmt):
            pass

        c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
        asound = ctypes.cdll.LoadLibrary('libasound.so.2') 
        asound.snd_lib_error_set_handler(c_error_handler)
        print(">>> Penangan error ALSA diatur untuk senyap.")
    except (OSError, AttributeError):
        print(">>> Tidak bisa mengatur penangan error ALSA. Pesan error mungkin masih muncul.")
        pass

def dengarkan_suara(device_idx=10, timeout_detik=5, phrase_limit_detik=50):
    """
    Mendengarkan input suara dari mikrofon dan mengubahnya menjadi teks.
    Mengembalikan teks hasil pengenalan atau None jika gagal.
    """
    recognizer = sr.Recognizer()
    # Atur pause_threshold di sini, pada objek recognizer
    recognizer.pause_threshold = 4.0  # Atur menjadi 2 detik (atau nilai lain yang Anda inginkan)

    microphone = sr.Microphone(device_index=device_idx) 

    try:
        print("\n🎙️  Menyesuaikan dengan kebisingan sekitar...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=2) 
        print("Penyesuaian kebisingan selesai.")

        print("🎙️  Saya mendengarkan... (ucapkan sesuatu)")
        with microphone as source:
            # Panggil listen() TANPA argumen pause_threshold
            audio = recognizer.listen(
                source, 
                timeout=timeout_detik,
                phrase_time_limit=phrase_limit_detik
            )
        print("🎤 Merekam selesai, sedang memproses suara Anda...")

        text_input = recognizer.recognize_google(audio, language='id-ID')
        print(f"✅ Anda berkata: {text_input}")
        return text_input
        
    except sr.WaitTimeoutError:
        print("⏰ Tidak ada suara terdeteksi dalam batas waktu.")
        return None
    except sr.UnknownValueError:
        print("🤔 Maaf, saya tidak mengerti apa yang Anda ucapkan.")
        return None
    except sr.RequestError as e:
        print(f"⚠️ Tidak bisa meminta hasil dari Google Speech Recognition; {e}")
        return None
    except Exception as e_mic:
        print(f"🚫 Masalah dengan mikrofon (index: {device_idx}) atau input suara: {e_mic}")
        return None