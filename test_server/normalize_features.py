import numpy as np
import json

# Load raw features
with open("features.json", "r") as f:
    raw_matrix = np.array(json.load(f))

# Normalization function
def normalize_column(col, min_val=None, max_val=None):
    col = np.array(col)
    if min_val is None: min_val = np.min(col)
    if max_val is None: max_val = np.max(col)
    if max_val - min_val == 0:
        return np.zeros_like(col)
    return (col - min_val) / (max_val - min_val)

# Normalize each feature
norm_matrix = np.zeros_like(raw_matrix)
norm_matrix[:, 0] = normalize_column(raw_matrix[:, 0])                      # RMS
norm_matrix[:, 1] = normalize_column(raw_matrix[:, 1], 0, 6000)             # Centroid
norm_matrix[:, 2] = normalize_column(raw_matrix[:, 2], 50, 2000)            # Pitch
norm_matrix[:, 3] = normalize_column(raw_matrix[:, 3], 0, 6000)             # Bandwidth
norm_matrix[:, 4] = normalize_column(raw_matrix[:, 4], -12, 12)             # Interval Score
norm_matrix[:, 5] = normalize_column(raw_matrix[:, 5], 60, 180)             # Tempo
norm_matrix[:, 6] = normalize_column(raw_matrix[:, 6])                      # Beat Strength

# Save the result
with open("features_normalized.json", "w") as f:
    json.dump(norm_matrix.tolist(), f)

print("✅ Normalized features saved to features_normalized.json")
