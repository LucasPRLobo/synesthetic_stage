import numpy as np
import pyaudio
from visuals.matplotlib_vis import plot_audio

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def analyze_live(duration=5):
    print("🎤 Recording from mic...")
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for _ in range(int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(np.frombuffer(data, dtype=np.int16))

    stream.stop_stream()
    stream.close()
    p.terminate()

    y = np.concatenate(frames).astype(np.float32)
    y /= np.max(np.abs(y))  # Normalize to [-1, 1]
    plot_audio(y, RATE, source="Live Mic")
