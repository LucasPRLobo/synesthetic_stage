import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import time
import json
import librosa
import threading

# Load feature matrix and audio
with open("features.json", "r") as f:
    feature_matrix = np.array(json.load(f))

audio_file = "test_audio.wav"
y, sr = librosa.load(audio_file, sr=44100)
duration = len(y) / sr

# Feature info
window_hop = 1024
window_duration = window_hop / sr
n_windows = len(feature_matrix)
time_axis = np.arange(n_windows) * window_duration

# Select which features to show
labels = ["RMS", "Centroid", "Pitch", "Beat Strength"]
colors = ["green", "blue", "purple", "red"]
data_indices = [0, 1, 2, 6]  # column indices in feature_matrix

# Initialize plots
fig, axs = plt.subplots(len(labels), 1, figsize=(12, 8), sharex=True)
lines = []

# Initial plot setup with empty data
for i, (ax, label, color, idx) in enumerate(zip(axs, labels, colors, data_indices)):
    ax.set_xlim(0, duration)
    ax.set_ylim(0, np.max(feature_matrix[:, idx]) * 1.1)
    ax.set_title(label)
    ax.grid(True)
    line, = ax.plot([], [], color=color)
    lines.append(line)

axs[-1].set_xlabel("Time (s)")
plt.tight_layout()

# Start audio playback in a thread
def play_audio():
    sd.play(y, samplerate=sr)

threading.Thread(target=play_audio).start()

# Animate live drawing
start_time = time.time()
frame = 0

x_vals = []
y_vals = [[] for _ in lines]

while frame < n_windows:
    elapsed = time.time() - start_time

    if elapsed >= frame * window_duration:
        t = time_axis[frame]
        x_vals.append(t)

        for i, idx in enumerate(data_indices):
            y_vals[i].append(feature_matrix[frame, idx])
            lines[i].set_data(x_vals, y_vals[i])
            axs[i].relim()
            axs[i].autoscale_view()

        plt.pause(0.001)
        frame += 1

plt.show()
