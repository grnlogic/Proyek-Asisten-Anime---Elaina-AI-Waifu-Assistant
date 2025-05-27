# buat_audio_tes.py
import asyncio
import edge_tts
import os

TEXT_TO_SAY = "Halo, nama saya adalah Elaina. Ini adalah percobaan suara saya. Semoga hasilnya bagus."
VOICE = "id-ID-GadisNeural" # Atau id-ID-GadisNeural
OUTPUT_FILE = "input_tts_netral.wav" # Simpan sebagai wav untuk kualitas baik

async def amain() -> None:
    communicate = edge_tts.Communicate(TEXT_TO_SAY, VOICE)
    # Simpan ke direktori saat ini, atau tentukan path lengkap
    target_path = os.path.join(os.getcwd(), OUTPUT_FILE) 
    await communicate.save(target_path)
    print(f"Audio disimpan sebagai: {target_path}")

if __name__ == "__main__":
    # Jika ada di Windows dan error, asyncio.run() mungkin butuh ini:
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(amain())