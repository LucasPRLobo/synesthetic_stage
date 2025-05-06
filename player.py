import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import time
import json
import librosa

# Load feature matrix
with open("features.json", "r") as f:
    feature_matrix = np.array(json.load(f))

# Load audio to get duration
audio_file = "test_audio.wav"
y, sr = librosa.load(audio_file, sr=44100)
duration = len(y) / sr

# Parameters
window_hop = 1024
window_duration = window_hop / sr  # duration per feature row
n_windows = len(feature_matrix)

# Time axis for the feature matrix
time_axis = np.arange(n_windows) * window_duration

# Play audio in a separate thread
def play_audio():
    sd.play(y, samplerate=sr)

# Start audio playback
import threading
audio_thread = threading.Thread(target=play_audio)
audio_thread.start()

# Plot setup
fig, axs = plt.subplots(4, 1, figsize=(12, 8), sharex=True)

labels = ["RMS", "Centroid", "Pitch", "Beat Strength"]
colors = ["green", "blue", "purple", "red"]
data_indices = [0, 1, 2, 6]  # corresponding to your features

lines = []
for i, (ax, label, color, idx) in enumerate(zip(axs, labels, colors, data_indices)):
    ax.plot(time_axis, feature_matrix[:, idx], label=label, color=color)
    ax.set_ylabel(label)
    ax.grid(True)
    line = ax.axvline(0, color='black', linestyle='--')  # moving cursor
    lines.append(line)

axs[-1].set_xlabel("Time (s)")
plt.tight_layout()

# Animate cursor
start_time = time.time()
while True:
    elapsed = time.time() - start_time
    if elapsed > duration:
        break

    for line in lines:
        line.set_xdata([elapsed])

    plt.pause(0.01)

plt.show()
