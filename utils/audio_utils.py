from utils.config import config
import simpleaudio as sa

def play_audio(file_path: str):
    """Plays an audio file (WAV only) using simpleaudio."""
    if not file_path.lower().endswith(".wav"):
        raise ValueError("Only WAV files are supported for playback.")

    try:
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        print(f"Error playing audio: {e}")