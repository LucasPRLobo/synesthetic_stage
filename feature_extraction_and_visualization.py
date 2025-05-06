
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import json


# Load your audio file
file_path = "test_audio.wav"  # Change this to your file name
y, sr = librosa.load(file_path, sr=44100)

# Define windowing parameters
window_size = 2048
hop_size = 1024

# Calculate number of windows
n_windows = (len(y) - window_size) // hop_size

print(f"Analyzing {n_windows} windows...\n")



def featureExtraction():
    rms_values = []
    centroid_values = []
    bandwidth_values = []
    pitch_values = []
    interval_values = []
    tempo_values = []
    beat_strength_values = []
    


    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)
    beat_strengths = onset_env[beats] if len(beats) > 0 else np.zeros(1)




    # Loop over each window and compute RMS
    for i in range(n_windows):
        start = i * hop_size
        end = start + window_size
        y_segment = y[start:end]

        # Feature 1: RMS Energy
        rms = librosa.feature.rms(y=y_segment).mean()
        rms_values.append(rms)
        # print(f"Window {i+1:03d}: RMS = {rms:.4f}")

        # Feature 2: Spectral Centroid
        centroid = librosa.feature.spectral_centroid(y=y_segment, sr=sr).mean()
        centroid_values.append(centroid)

         # Feature 3: Spectral Bandwidth
        bandwidth = librosa.feature.spectral_bandwidth(y=y_segment, sr=sr).mean()
        bandwidth_values.append(bandwidth)

        # Feature 4: Pitch using YIN
        try:
            pitch_frame = librosa.yin(y_segment,
                                    fmin=librosa.note_to_hz('C2'),
                                    fmax=librosa.note_to_hz('C7'),
                                    sr=sr)
            pitch_frame = pitch_frame[np.isfinite(pitch_frame)]
            pitch = np.mean(pitch_frame) if len(pitch_frame) > 0 else 0.0
        except:
            pitch = 0.0
        pitch_values.append(pitch)


        # Feature 5: Tonal Interval Score
        chroma = librosa.feature.chroma_stft(y=y_segment, sr=sr)
        chroma_mean = chroma.mean(axis=1)

        # Find "active" pitch classes
        chroma_threshold = 0.2  # tweak as needed
        active_notes = np.where(chroma_mean > chroma_threshold)[0]

        # Calculate score from ordered intervals
        interval_score = 0
        for j in range(len(active_notes) - 1):
            diff = (active_notes[j + 1] - active_notes[j]) % 12
            if diff <= 6:
                interval_score += diff     # ascending movement
            else:
                interval_score -= (12 - diff)  # descending movement
        interval_values.append(interval_score)

        # Feature 6: Global Tempo (same repeated for each window)
        tempo_values.append(tempo)

        # Feature 7: Beat Strength (in this window)
        window_time = librosa.frames_to_time([i], sr=sr, hop_length=hop_size)[0]
        close_beats = np.where((beat_times >= window_time) &
                            (beat_times < window_time + window_size / sr))[0]

        strength = beat_strengths[close_beats].mean() if len(close_beats) > 0 else 0.0
        beat_strength_values.append(strength)
    
    
    # 🎨 Split into subplots
    fig, axs = plt.subplots(7, 1, figsize=(12, 6), sharex=True)

    # Plot RMS
    axs[0].plot(rms_values, color='green')
    axs[0].set_title("RMS Energy Over Time")
    axs[0].set_ylabel("RMS (0–1)")

    # Plot Spectral Centroid
    axs[1].plot(centroid_values, color='blue')
    axs[1].set_title("Spectral Centroid Over Time")
    axs[1].set_ylabel("Centroid (Hz)")

    axs[2].plot(bandwidth_values, color='orange')
    axs[2].set_title("Spectral Bandwidth")
    axs[2].set_ylabel("Hz")

    axs[3].plot(pitch_values, color='purple')
    axs[3].set_title("Pitch (YIN)")
    axs[3].set_ylabel("Hz")

    axs[4].plot(interval_values, color='brown')
    axs[4].set_title("Tonal Interval Score")
    axs[4].set_ylabel("Score")
   
    
    axs[5].plot(tempo_values, color='teal')
    axs[5].set_title("Tempo (BPM)")
    axs[5].set_ylabel("BPM")

    axs[6].plot(beat_strength_values, color='red')
    axs[6].set_title("Beat Strength")
    axs[6].set_ylabel("Strength")
    axs[6].set_xlabel("Window Index")


   # Combine all features into rows of native Python types
    feature_matrix = [
        [float(r), float(c), float(p), float(b), float(i), float(t), float(s)]
        for r, c, p, b, i, t, s in zip(
            rms_values,
            centroid_values,
            pitch_values,
            bandwidth_values,
            interval_values,
            tempo_values,
            beat_strength_values
        )
    ]

    # Export as JSON
    with open("features.json", "w") as f:
        json.dump(feature_matrix, f)

    print("✅ Feature matrix saved to features.json")



    plt.tight_layout()
    plt.show()

featureExtraction()