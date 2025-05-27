# app/tts_service.py
import asyncio
import edge_tts
import os
import subprocess # Pastikan ini sudah diimport

# Path ke direktori utama Mangio-RVC-Fork Anda
RVC_DIR = "/home/fajar/Documents/ProyekAsistenAnime/rvc_workspace/Mangio-RVC-Fork/" # SESUAIKAN JIKA PERLU
# Path ke interpreter python di dalam venv RVC Anda
RVC_PYTHON_EXEC = os.path.join(RVC_DIR, "venv-rvc-mangio/bin/python") # SESUAIKAN JIKA PERLU

# File audio sementara
BASE_AUDIO_FILE = os.path.join(RVC_DIR, "saudio/temp_base_audio_for_rvc.wav") # Simpan di saudio agar mudah diakses RVC CLI
CONVERTED_AUDIO_FILE = os.path.join(RVC_DIR, "audio-outputs/temp_converted_elaina.wav") # RVC CLI akan menyimpan di sini

# Parameter RVC Elaina Anda (SESUAIKAN DENGAN HASIL TES ANDA)
# Argumen untuk CLI RVC
MODEL_NAME_PTH = "Elaina.pth"
# Tambahkan path lengkap ke file model Elaina.pth
ELAINAPTH_PATH = os.path.join(RVC_DIR, "weights", MODEL_NAME_PTH) # Hapus "assets/"# SOURCE_AUDIO_PATH_RVC akan diisi oleh BASE_AUDIO_FILE nanti
OUTPUT_AUDIO_NAME_RVC = "temp_converted_elaina.wav" # Hanya nama file, karena akan disimpan di ./audio-outputs
ELAINA_INDEX_PATH = "logs/Elaina_v2_trained/added_IVF561_Flat_nprobe_1_Elaina_v2.index" # Ganti nama variabel di sini
SPEAKER_ID_VAL = "0"
TRANSPOSE_VAL = "0" # Ganti dengan nilai optimal Anda
F0_METHOD_VAL = "rmvpe" # Ganti dengan F0 method optimal Anda
CREPE_HOP_LENGTH_VAL = "160"
RMVPE_FILTER_RADIUS_VAL = "3"
POST_RESAMPLE_RATE_VAL = "0"
MIX_VOLUME_ENVELOPE_VAL = "1" 
FEATURE_INDEX_RATIO_VAL = "0.78" 
PROTECTION_VAL = "0.33"
# Tambahkan parameter ke-14 yang kita temukan (0.45)
UNKNOWN_PARAM_14_VAL = "0.45" 
FORMANT_SHIFT_ACTIVE_VAL = "False"
QUEFRENCY_VAL = "8.0"
TIMBRE_VAL = "1.2"


async def generate_base_audio_with_edge_tts(text_to_speak, voice_name="id-ID-GadisNeural", output_file=BASE_AUDIO_FILE):
    """Menghasilkan audio dasar menggunakan edge-tts dan menyimpannya ke file."""
    try:
        print(f"\n[TTS Service] Membuat audio dasar dengan edge-tts ({voice_name})...")
        communicate = edge_tts.Communicate(text_to_speak, voice_name)
        await communicate.save(output_file)
        print(f"[TTS Service] Audio dasar disimpan sebagai {output_file}")
        return True
    except Exception as e:
        print(f"[TTS Service] Error saat edge-tts membuat audio dasar: {e}")
        return False

def convert_voice_with_rvc_cli(input_audio_path_relative_to_rvc_dir, output_audio_name):
    """Menjalankan RVC CLI untuk konversi suara menggunakan subprocess."""
    print(f"[TTS Service] Memulai konversi suara dengan RVC CLI untuk input: {input_audio_path_relative_to_rvc_dir}")

    rvc_script_path = os.path.join(RVC_DIR, "infer-web.py")

    # Susun semua argumen sebagai string tunggal seperti yang diterima CLI interaktif
    # setelah perintah 'go infer'
    cli_arguments_string = (
        f"{MODEL_NAME_PTH} "
        f"{input_audio_path_relative_to_rvc_dir} " # Ini akan menjadi 'saudio/temp_base_audio_for_rvc.wav'
        f"{output_audio_name} " # Ini akan menjadi 'temp_converted_elaina.wav' (disimpan di audio-outputs/)
        f"{ELAINA_INDEX_PATH} "
        f"{SPEAKER_ID_VAL} "
        f"{TRANSPOSE_VAL} "
        f"{F0_METHOD_VAL} "
        f"{CREPE_HOP_LENGTH_VAL} "
        f"{RMVPE_FILTER_RADIUS_VAL} "
        f"{POST_RESAMPLE_RATE_VAL} "
        f"{MIX_VOLUME_ENVELOPE_VAL} "
        f"{FEATURE_INDEX_RATIO_VAL} "
        f"{PROTECTION_VAL} "
        f"{UNKNOWN_PARAM_14_VAL} " # Parameter ke-14 yang kita tambahkan
        f"{FORMANT_SHIFT_ACTIVE_VAL} "
        f"{QUEFRENCY_VAL} "
        f"{TIMBRE_VAL}"
    )

    # Perintah untuk masuk ke mode CLI, lalu ke infer, lalu masukkan argumen
    # Kita akan menggunakan Popen untuk interaksi stdin/stdout
    command_to_run_rvc = [
        RVC_PYTHON_EXEC,
        rvc_script_path,
        "--is_cli"
    ]

    try:
        # Jalankan RVC CLI dan kirim perintah secara interaktif
        # cwd=RVC_DIR memastikan path relatif seperti 'saudio/...' dan 'logs/...' bekerja dari dalam RVC_DIR
        process = subprocess.Popen(command_to_run_rvc, cwd=RVC_DIR, 
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                   text=True, bufsize=1, universal_newlines=True)

        # Kirim perintah 'go infer' dan kemudian string argumennya
        # Pastikan ada newline character (\n) agar perintah dieksekusi
        commands_to_send = "go infer\n" + cli_arguments_string + "\n"

        print(f"[TTS Service] Mengirim perintah ke RVC CLI: go infer")
        print(f"[TTS Service] Mengirim argumen ke RVC CLI: {cli_arguments_string}")

        # Berkomunikasi dengan proses: kirim input, dapatkan output dan error
        stdout_data, stderr_data = process.communicate(input=commands_to_send, timeout=120) # Timeout 120 detik

        print("[TTS Service] Output RVC CLI STDOUT:")
        print(stdout_data)
        print("[TTS Service] RVC CLI STDERR (jika ada, sebelum EOFError):") # Tambahkan ini untuk melihat stderr sebelum EOF
        print(stderr_data) # stderr mungkin berisi pesan EOFError itu sendiri

        # Periksa apakah pesan sukses ada di stdout MESKIPUN ADA EOFError di akhir
        # EOFError di stderr setelah RVC selesai bekerja bisa kita abaikan untuk penentuan sukses konversi
        if "Inference succeeded" in stdout_data and f"Saved output to audio-outputs/{output_audio_name}" in stdout_data:
            print(f"[TTS Service] Konversi RVC berhasil (mengabaikan EOFError di akhir). Output di audio-outputs/{output_audio_name}")
            return True # Anggap sukses jika file output dibuat
        else:
            print(f"[TTS Service] RVC CLI selesai tapi pesan sukses tidak ditemukan atau ada error lain sebelum EOF.")
            # Jika returncode bukan 0 DAN pesan sukses tidak ada, baru anggap gagal
            if process.returncode != 0: 
                print(f"[TTS Service] RVC CLI STDERR (return code {process.returncode}): {stderr_data}")
            print(f"[TTS Service] Gagal mengkonversi suara dengan RVC CLI.")
            return False

    except subprocess.TimeoutExpired:
        print(f"[TTS Service] Error: RVC CLI timeout setelah 120 detik.")
        process.kill()
        stdout_data, stderr_data = process.communicate()
        print(f"[TTS Service] RVC CLI STDOUT (timeout): {stdout_data}")
        print(f"[TTS Service] RVC CLI STDERR (timeout): {stderr_data}")
        return False
    except FileNotFoundError:
        print(f"[TTS Service] Error: Skrip RVC atau Python RVC tidak ditemukan. Periksa path RVC_DIR dan RVC_PYTHON_EXEC.")
        return False
    except Exception as e:
        print(f"[TTS Service] Error tak terduga saat menjalankan RVC CLI: {e}")
        return False


def speak_text_rvc(text_to_speak):
    """Menghasilkan audio dasar, mengkonversinya dengan RVC, lalu memutarnya."""
    # Pastikan folder saudio dan audio-outputs ada di RVC_DIR
    os.makedirs(os.path.join(RVC_DIR, "saudio"), exist_ok=True)
    os.makedirs(os.path.join(RVC_DIR, "audio-outputs"), exist_ok=True)

    # Path relatif untuk audio dasar dari dalam RVC_DIR
    base_audio_relative_path = "saudio/" + os.path.basename(BASE_AUDIO_FILE) 
    # Nama file output relatif (akan disimpan di audio-outputs/ oleh RVC)
    converted_audio_relative_name = os.path.basename(CONVERTED_AUDIO_FILE) 

    if asyncio.run(generate_base_audio_with_edge_tts(text_to_speak, output_file=os.path.join(RVC_DIR, base_audio_relative_path))):
        if convert_voice_with_rvc_cli(base_audio_relative_path, converted_audio_relative_name):
            try:
                # Path lengkap ke file hasil konversi RVC
                full_converted_audio_path = os.path.join(RVC_DIR, "audio-outputs", converted_audio_relative_name)
                print(f"[TTS Service] Memutar audio hasil konversi RVC: {full_converted_audio_path}...")
                os.system(f"mpv --no-terminal --audio-display=no {full_converted_audio_path}") 
                print("[TTS Service] Pemutaran audio RVC selesai.")
                # Hapus file sementara jika perlu
                # if os.path.exists(os.path.join(RVC_DIR, base_audio_relative_path)): os.remove(os.path.join(RVC_DIR, base_audio_relative_path))
                # if os.path.exists(full_converted_audio_path): os.remove(full_converted_audio_path)
            except Exception as e_play:
                print(f"[TTS Service] Error saat memutar audio hasil RVC: {e_play}")
        else:
            print("[TTS Service] Gagal mengkonversi suara dengan RVC. Memutar suara dasar sebagai fallback.")
            # Fallback: putar suara dasar jika RVC gagal
            os.system(f"mpv --no-terminal --audio-display=no {os.path.join(RVC_DIR, base_audio_relative_path)}")
    else:
        print("[TTS Service] Gagal membuat audio dasar dengan edge-tts.")

# Arahkan speak_text utama ke fungsi RVC baru kita
speak_text = speak_text_rvc

def init_tts_engine():
    print(">>> Menggunakan engine TTS: RVC (via edge-tts base) dengan panggilan CLI.")
    if not os.path.isdir(RVC_DIR): # Cek direktori
        print(f"ERROR: Direktori RVC_DIR tidak ditemukan: {RVC_DIR}")
        return False
    if not os.path.isfile(RVC_PYTHON_EXEC): # Cek file python exec
        print(f"ERROR: Python RVC_PYTHON_EXEC tidak ditemukan: {RVC_PYTHON_EXEC}")
        return False
    if not os.path.isfile(os.path.join(RVC_DIR, "infer-web.py")): # Cek script RVC
        print(f"ERROR: Skrip infer-web.py RVC tidak ditemukan di {RVC_DIR}")
        return False
    if not os.path.isfile(ELAINAPTH_PATH):
        print(f"ERROR: File model Elaina.pth tidak ditemukan: {ELAINAPTH_PATH}")
        return False
    if not os.path.isfile(os.path.join(RVC_DIR, ELAINA_INDEX_PATH)): # Index path relatif thd RVC_DIR
        print(f"ERROR: File index Elaina tidak ditemukan: {os.path.join(RVC_DIR, ELAINA_INDEX_PATH)}")
        return False
    print(">>> Semua path penting untuk RVC engine TTS terverifikasi.")
    return True