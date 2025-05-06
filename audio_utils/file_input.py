import librosa
from visuals.matplotlib_vis import plot_audio

def analyze_file(path):
    y, sr = librosa.load(path, sr=44100)
    plot_audio(y, sr, source="File")
