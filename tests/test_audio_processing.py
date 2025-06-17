from utils.config import config
import librosa

def test_audio_processing(audio_path):
    # Using librosa to extract BPM
    y, sr = librosa.load(audio_path)
    tempo_librosa, _ = librosa.beat.beat_track(y=y, sr=sr)

    print(f"BPM using librosa: {tempo_librosa}")

# Provide a sample audio file to test
audio_sample_path = 'data/samples/Drum Loop 2 120BPM.wav'  # Replace with your sample path
test_audio_processing(audio_sample_path)
    