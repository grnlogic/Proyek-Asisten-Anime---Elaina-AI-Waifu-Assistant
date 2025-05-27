# Proyek Asisten Anime - Elaina AI Waifu Assistant

```
    ______     __         ______     __     __   __     ______
   /\  ___\   /\ \       /\  __ \   /\ \   /\ "-.\ \   /\  __ \
   \ \  __\   \ \ \____  \ \  __ \  \ \ \  \ \ \-.  \  \ \  __ \
    \ \_____\  \ \_____\  \ \_\ \_\  \ \_\  \ \_\\"\_\  \ \_\ \_\
     \/_____/   \/_____/   \/_/\/_/   \/_/   \/_/ \/_/   \/_/\/_/

            ✨ AI Waifu Assistant with Voice Interaction ✨
```

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-1.5_Flash-4285F4.svg?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Speech Recognition](https://img.shields.io/badge/Speech_Recognition-Google_API-green.svg?style=for-the-badge&logo=google&logoColor=white)](https://cloud.google.com/speech-to-text)
[![Edge TTS](https://img.shields.io/badge/Edge_TTS-Microsoft-0078d4.svg?style=for-the-badge&logo=microsoft&logoColor=white)](https://github.com/rany2/edge-tts)
[![RVC](https://img.shields.io/badge/RVC-Voice_Conversion-ff6b6b.svg?style=for-the-badge&logo=waveform&logoColor=white)](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
[![Linux](https://img.shields.io/badge/Linux-Supported-FCC624.svg?style=for-the-badge&logo=linux&logoColor=black)](https://www.linux.org/)

---

Sebuah asisten AI waifu bernama **Elaina** yang dapat berkomunikasi melalui suara dengan teknologi Speech-to-Text (STT), Text-to-Speech (TTS), dan AI conversation menggunakan Google Gemini API. Elaina dapat berbicara dengan suara yang diconvert menggunakan RVC (Real-time Voice Conversion) untuk memberikan pengalaman waifu yang lebih imersif.

## 🌟 Fitur Utama

- **🎤 Speech-to-Text (STT)**: Mendengarkan input suara pengguna menggunakan Google Speech Recognition
- **🧠 AI Conversation**: Powered by Google Gemini 1.5 Flash dengan persona Elaina yang ramah dan ceria
- **🗣️ Text-to-Speech (TTS)**: Menggunakan Edge-TTS sebagai base voice
- **🎵 Voice Conversion**: RVC (Real-time Voice Conversion) untuk mengubah suara menjadi karakter Elaina
- **💬 Memory Chat**: Menyimpan riwayat percakapan dalam sesi yang sama
- **🔇 ALSA Error Suppression**: Mengatasi error ALSA pada sistem Linux

## 🚀 Teknologi yang Digunakan

- **AI Engine**: Google Gemini 1.5 Flash API
- **Speech Recognition**: Google Speech Recognition API (via `speech_recognition`)
- **Text-to-Speech**: Microsoft Edge-TTS (`edge-tts`)
- **Voice Conversion**: Mangio-RVC-Fork
- **Audio Playback**: MPV player
- **Language**: Python 3.8+
- **Environment Management**: python-dotenv

## 📋 Prasyarat

Pastikan sistem Anda memiliki:

### Software Dasar

- **Python 3.8+** dengan pip
- **MPV player** untuk audio playback
- **Mikrofon** yang berfungsi
- **Speaker/Headphone** untuk output audio

### Sistem Linux (Recommended)

- ALSA libraries (biasanya sudah terinstall)
- PulseAudio atau ALSA untuk audio

### Dependencies Python

Lihat file `requirements.txt` untuk daftar lengkap dependencies.

## 🛠️ Instalasi

### 1. Clone Repository

```bash
git clone [URL_REPOSITORY]
cd ProyekAsistenAnime
```

### 2. Install Dependencies Python

```bash
pip install -r requirements.txt
```

Dependencies utama yang dibutuhkan:

```bash
pip install google-generativeai python-dotenv speech_recognition edge-tts emoji
```

### 3. Install MPV Player

```bash
# Ubuntu/Debian
sudo apt install mpv

# Fedora
sudo dnf install mpv

# Arch Linux
sudo pacman -S mpv
```

### 4. Setup RVC (Real-time Voice Conversion)

- Download dan setup **Mangio-RVC-Fork** di direktori `rvc_workspace/`
- Siapkan model Elaina (`Elaina.pth`) dan index file
- Pastikan virtual environment RVC aktif di `rvc_workspace/Mangio-RVC-Fork/venv-rvc-mangio/`

### 5. Konfigurasi Environment

```bash
cp .env.example .env
```

Edit file `.env` dan tambahkan:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 6. Test Mikrofon

```bash
python cek_mikrofon.py
```

Catat index mikrofon yang ingin digunakan dan sesuaikan di `stt_service.py`.

## 🎯 Cara Penggunaan

### 1. Jalankan Asisten

```bash
python -m app.main
```

### 2. Berinteraksi dengan Elaina

- **Mulai berbicara** setelah mendengar prompt "Saya mendengarkan..."
- **Tunggu respons** dari Elaina (teks + suara RVC)
- **Ucapkan "stop"** untuk mengakhiri percakapan

### 3. Troubleshooting Audio

Jika ada masalah dengan mikrofon:

```bash
# Cek daftar mikrofon
python cek_mikrofon.py

# Edit device_idx di stt_service.py sesuai hasil
```

## 🏗️ Struktur Proyek

```
ProyekAsistenAnime/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Entry point aplikasi
│   ├── config.py            # Konfigurasi sistem prompt Elaina
│   ├── config_loader.py     # Loader konfigurasi dan API key
│   ├── gemini_service.py    # Service untuk Google Gemini API
│   ├── stt_service.py       # Speech-to-Text service
│   └── tts_service.py       # Text-to-Speech + RVC service
├── rvc_workspace/
│   └── Mangio-RVC-Fork/     # RVC installation directory
├── .env                     # Environment variables (tidak dicommit)
├── .env.example             # Template environment variables
├── requirements.txt         # Python dependencies
├── cek_mikrofon.py         # Utility untuk cek mikrofon
├── buat_audio_tes.py       # Utility untuk test edge-tts
├── tes_gemini.py           # Utility untuk test Gemini API
└── README.md               # Dokumentasi ini
```

## ⚙️ Konfigurasi

### Persona Elaina

Edit `app/config.py` untuk mengubah kepribadian Elaina:

```python
SYSTEM_PROMPT = """
Kamu adalah Elaina, sebuah asisten AI waifu yang ramah, ceria, dan sangat membantu...
"""
```

### Parameter RVC

Edit `app/tts_service.py` untuk fine-tuning suara Elaina:

```python
TRANSPOSE_VAL = "0"           # Pitch adjustment
F0_METHOD_VAL = "rmvpe"       # F0 extraction method
FEATURE_INDEX_RATIO_VAL = "0.78"  # Voice similarity
PROTECTION_VAL = "0.33"      # Voice protection
```

### STT Configuration

Edit `app/stt_service.py` untuk pengaturan mikrofon:

```python
device_idx = 10              # Index mikrofon Anda
timeout_detik = 5            # Timeout detection
phrase_limit_detik = 50      # Batas waktu bicara
```

## 🐛 Troubleshooting

### Error ALSA (Linux)

Error ALSA sudah diatasi dengan error handler suppression di kode.

### Mikrofon tidak terdeteksi

```bash
# Cek permission mikrofon
sudo usermod -a -G audio $USER

# Restart audio service
pulseaudio -k && pulseaudio --start
```

### RVC tidak berfungsi

- Pastikan path `RVC_DIR` dan `RVC_PYTHON_EXEC` benar di `tts_service.py`
- Cek model `Elaina.pth` dan index file sudah ada
- Test RVC secara manual terlebih dahulu

### Gemini API Error

- Pastikan `GEMINI_API_KEY` sudah benar di file `.env`
- Cek quota API Gemini Anda
- Pastikan koneksi internet stabil

## 🤝 Kontribusi

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

## 🙏 Credits & Acknowledgments

- **Google Gemini API** untuk AI conversation engine
- **Microsoft Edge-TTS** untuk base voice synthesis
- **Mangio-RVC-Fork** untuk real-time voice conversion
- **SpeechRecognition library** untuk STT functionality
- **Komunitas AI Indonesia** untuk dukungan dan feedback

## 📞 Kontak

- **Developer**: Fajar
- **Project**: Anime Assistant Elaina
- **Persona**: Elaina - Friendly AI Waifu Assistant

---

⭐ **Jika Elaina membantu Anda, jangan lupa berikan star di repository ini!**

_"Halo Fajar! Ada yang bisa saya bantu hari ini?" - Elaina_ 💫
