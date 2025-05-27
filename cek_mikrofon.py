# cek_mikrofon.py
import speech_recognition as sr

print("Mencari mikrofon yang tersedia...")
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Mikrofon ke-{index} dengan nama \"{name}\"")

if not sr.Microphone.list_microphone_names():
    print("Tidak ada mikrofon yang ditemukan oleh SpeechRecognition.")