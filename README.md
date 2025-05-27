# Anime Assistant Project - Elaina AI Waifu Assistant

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

An AI waifu assistant named **Elaina** that can communicate through voice using Speech-to-Text (STT), Text-to-Speech (TTS), and AI conversation powered by Google Gemini API. Elaina can speak with voice converted using RVC (Real-time Voice Conversion) to provide a more immersive waifu experience.

## 🌟 Key Features

- **🎤 Speech-to-Text (STT)**: Listens to user voice input using Google Speech Recognition
- **🧠 AI Conversation**: Powered by Google Gemini 1.5 Flash with Elaina's friendly and cheerful persona
- **🗣️ Text-to-Speech (TTS)**: Uses Edge-TTS as base voice
- **🎵 Voice Conversion**: RVC (Real-time Voice Conversion) to transform voice into Elaina character
- **💬 Chat Memory**: Stores conversation history within the same session
- **🔇 ALSA Error Suppression**: Handles ALSA errors on Linux systems

## 🚀 Technologies Used

- **AI Engine**: Google Gemini 1.5 Flash API
- **Speech Recognition**: Google Speech Recognition API (via `speech_recognition`)
- **Text-to-Speech**: Microsoft Edge-TTS (`edge-tts`)
- **Voice Conversion**: Mangio-RVC-Fork
- **Audio Playback**: MPV player
- **Language**: Python 3.8+
- **Environment Management**: python-dotenv

## 📋 Prerequisites

Make sure your system has:

### Basic Software

- **Python 3.8+** with pip
- **MPV player** for audio playback
- **Working microphone**
- **Speakers/Headphones** for audio output

### Linux System (Recommended)

- ALSA libraries (usually pre-installed)
- PulseAudio or ALSA for audio

### Python Dependencies

See `requirements.txt` file for complete list of dependencies.

## 🛠️ Installation

### 1. Clone Repository

```bash
git clone [REPOSITORY_URL]
cd ProyekAsistenAnime
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Main dependencies required:

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

- Download and setup **Mangio-RVC-Fork** in `rvc_workspace/` directory
- Prepare Elaina model (`Elaina.pth`) and index file
- Ensure RVC virtual environment is active in `rvc_workspace/Mangio-RVC-Fork/venv-rvc-mangio/`

### 5. Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` file and add:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 6. Test Microphone

```bash
python cek_mikrofon.py
```

Note the microphone index you want to use and adjust it in `stt_service.py`.

## 🎯 Usage

### 1. Run Assistant

```bash
python -m app.main
```

### 2. Interact with Elaina

- **Start speaking** after hearing the prompt "I'm listening..."
- **Wait for response** from Elaina (text + RVC voice)
- **Say "stop"** to end the conversation

### 3. Audio Troubleshooting

If there are microphone issues:

```bash
# Check microphone list
python cek_mikrofon.py

# Edit device_idx in stt_service.py according to results
```

## 🏗️ Project Structure

```
ProyekAsistenAnime/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Application entry point
│   ├── config.py            # Elaina system prompt configuration
│   ├── config_loader.py     # Configuration and API key loader
│   ├── gemini_service.py    # Google Gemini API service
│   ├── stt_service.py       # Speech-to-Text service
│   └── tts_service.py       # Text-to-Speech + RVC service
├── rvc_workspace/
│   └── Mangio-RVC-Fork/     # RVC installation directory
├── .env                     # Environment variables (not committed)
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
├── cek_mikrofon.py         # Utility to check microphone
├── buat_audio_tes.py       # Utility to test edge-tts
├── tes_gemini.py           # Utility to test Gemini API
└── README.md               # This documentation
```

## ⚙️ Configuration

### Elaina Persona

Edit `app/config.py` to modify Elaina's personality:

```python
SYSTEM_PROMPT = """
You are Elaina, a friendly, cheerful, and very helpful AI waifu assistant...
"""
```

### RVC Parameters

Edit `app/tts_service.py` for fine-tuning Elaina's voice:

```python
TRANSPOSE_VAL = "0"           # Pitch adjustment
F0_METHOD_VAL = "rmvpe"       # F0 extraction method
FEATURE_INDEX_RATIO_VAL = "0.78"  # Voice similarity
PROTECTION_VAL = "0.33"      # Voice protection
```

### STT Configuration

Edit `app/stt_service.py` for microphone settings:

```python
device_idx = 10              # Your microphone index
timeout_detik = 5            # Detection timeout
phrase_limit_detik = 50      # Speaking time limit
```

## 🐛 Troubleshooting

### ALSA Errors (Linux)

ALSA errors are already handled with error suppression in the code.

### Microphone Not Detected

```bash
# Check microphone permissions
sudo usermod -a -G audio $USER

# Restart audio service
pulseaudio -k && pulseaudio --start
```

### RVC Not Working

- Ensure `RVC_DIR` and `RVC_PYTHON_EXEC` paths are correct in `tts_service.py`
- Check that `Elaina.pth` model and index file exist
- Test RVC manually first

### Gemini API Error

- Ensure `GEMINI_API_KEY` is correct in `.env` file
- Check your Gemini API quota
- Ensure stable internet connection

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Credits & Acknowledgments

- **Google Gemini API** for AI conversation engine
- **Microsoft Edge-TTS** for base voice synthesis
- **Mangio-RVC-Fork** for real-time voice conversion
- **SpeechRecognition library** for STT functionality
- **Indonesian AI Community** for support and feedback

## 📞 Contact

- **Developer**: Fajar
- **Project**: Anime Assistant Elaina
- **Persona**: Elaina - Friendly AI Waifu Assistant

---

⭐ **If Elaina helps you, don't forget to give this repository a star!**

_"Hello Fajar! Is there anything I can help you with today?" - Elaina_ 💫
