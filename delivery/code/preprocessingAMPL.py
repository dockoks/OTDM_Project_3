#!/usr/bin/env python3
"""
Auxiliary script to clean data into AMPL readable .txt files for the problem at hand.
"""
import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist

def arrange_dat(dat_file, k, output_file, line_split=None, dist_file=None):
    # Read the data file into a DataFrame
    data = pd.read_csv(dat_file, delimiter=line_split)
    
    # Extract feature names
    feature_names = data.columns
    
    # Standardize the data (Z-score normalization)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    
    # Convert scaled data back to a DataFrame for easier handling
    scaled_df = pd.DataFrame(scaled_data, columns=feature_names)
    
    # Convert scaled data to a NumPy array
    xs = scaled_df.to_numpy()
    m = xs.shape[0]
    d = xs.shape[1]
    
    # Write to output file (scaled data)
    with open(output_file, "w") as f:
        f.write(f"param m:={m};\n")
        f.write(f"param k:={k};\n")
        xranges = ' '.join(map(str, list(range(1, d+1))))
        f.write(f"param d: {xranges}:=\n")
        for i in range(1, m + 1):
            if i < m:
                f.write(f"{i} {list_to_string(xs[i - 1])}\n")
            else:
                f.write(f"{i} {list_to_string(xs[i - 1])};\n")

    # Compute the Euclidean distance matrix
    dist_matrix = cdist(xs, xs, metric='euclidean')
    np.fill_diagonal(dist_matrix, 0)  # Ensure diagonal elements are 0

    # Write distance matrix to dist_file
    if dist_file:
        with open(dist_file, "w") as f:
            f.write(f"param DistanceMatrix:\n")
            xranges = ' '.join(map(str, list(range(1, m + 1))))
            f.write(f"{xranges} :=\n")
            for i in range(m):
                row = f"{i + 1} " + " ".join(f"{dist_matrix[i, j]:.6f}" for j in range(m))
                if i < m - 1:
                    f.write(row + "\n")
                else:
                    f.write(row + ";\n")  # Add ";" at the end of the last line

def list_to_string(list):
    string = ""
    for elem in list:
        string += " " + str(elem)
    return string

if __name__ == "__main__":
    dat_file = sys.argv[1]  # Input CSV file
    k = int(sys.argv[2])  # Number of clusters
    output_file = sys.argv[3]  # Output scaled .txt file
    dist_file = sys.argv[4]  # Output distance matrix file
    line_split = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != "None" else None
    
    arrange_dat(dat_file, k, output_file, line_split, dist_file)
