import argparse
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def svd_compress_channel(channel, r):
    # channel: 2D array
    U, S, Vt = np.linalg.svd(channel, full_matrices=False)
    # keep top-r components
    U_r = U[:, :r]
    S_r = S[:r]
    Vt_r = Vt[:r, :]
    # reconstruct
    return U_r @ np.diag(S_r) @ Vt_r, S

def compress_image(input_path, output_path, r, plot_path=None):
    # Load image
    img = Image.open(input_path).convert('RGBA')
    arr = np.array(img, dtype=float)

    # Separate channels
    channels = [arr[..., i] for i in range(4)]  # R, G, B, A
    compressed_channels = []
    singular_values = []

    # Process each channel
    for ch in channels:
        comp_ch, S = svd_compress_channel(ch, r)
        compressed_channels.append(np.clip(comp_ch, 0, 255))
        singular_values.append(S)

    # Reassemble compressed image
    comp_arr = np.stack(compressed_channels, axis=-1).astype(np.uint8)
    comp_img = Image.fromarray(comp_arr, mode='RGBA')
    comp_img.save(output_path)

    # Plot singular values dropoff for first channel (R)
    if plot_path is not None:
        plt.figure()
        plt.semilogy(singular_values[0], marker='o', linestyle='-')
        plt.title('Singular Values Dropoff (R channel)')
        plt.xlabel('Index')
        plt.ylabel('Singular value (log scale)')
        plt.grid(True)
        plt.savefig(plot_path)
        plt.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SVD Image Compression')
    parser.add_argument('input', help='Input image file path')
    parser.add_argument('output', help='Output image file path')
    parser.add_argument('-r', type=int, default=50, help='Rank for SVD compression')
    parser.add_argument('--plot', help='Path to save singular values plot')
    args = parser.parse_args()

    compress_image(args.input, args.output, args.r, args.plot)
