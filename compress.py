import argparse
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def normalize_to_image(arr):
    """Normalize a 2D array to 0-255 uint8 for image saving."""
    arr_min, arr_max = arr.min(), arr.max()
    if arr_max - arr_min < 1e-8:
        return np.zeros_like(arr, dtype=np.uint8)
    norm = (arr - arr_min) / (arr_max - arr_min)
    return (255 * norm).astype(np.uint8)


def svd_compress_channel(channel, r, save_components=False, base_path=None, ch_name=""):
    # Compute full SVD
    U, S, Vt = np.linalg.svd(channel, full_matrices=False)

    # Truncate to r
    U_r = U[:, :r]
    S_r = S[:r]
    Vt_r = Vt[:r, :]

    # Optionally save U, S, Vt as images
    if save_components and base_path:
        # U matrix image
        U_img = normalize_to_image(U_r)
        Image.fromarray(U_img).save(f"{base_path}_{ch_name}_U.png")
        # Sigma as diagonal matrix image
        S_mat = np.diag(S_r)
        S_img = normalize_to_image(S_mat)
        Image.fromarray(S_img).save(f"{base_path}_{ch_name}_S.png")
        # Vt matrix image
        Vt_img = normalize_to_image(Vt_r)
        Image.fromarray(Vt_img).save(f"{base_path}_{ch_name}_Vt.png")

    # Reconstruct truncated channel
    comp = U_r @ np.diag(S_r) @ Vt_r
    return comp, S


def compress_image(input_path, output_path, r, plot_path=None, save_components=False):
    # Load image
    img = Image.open(input_path).convert('RGBA')
    arr = np.array(img, dtype=float)

    # Separate channels
    channels = [arr[..., i] for i in range(4)]  # R, G, B, A
    compressed = []
    singular_values = []

    # Base for component output filenames
    base = output_path.rsplit('.', 1)[0]
    names = ['R', 'G', 'B', 'A']

    # Process each channel
    for idx, ch in enumerate(channels):
        comp_ch, S = svd_compress_channel(
            ch, r,
            save_components=save_components,
            base_path=base,
            ch_name=names[idx]
        )
        compressed.append(np.clip(comp_ch, 0, 255))
        singular_values.append(S)

    # Reassemble and save compressed image
    comp_arr = np.stack(compressed, axis=-1).astype(np.uint8)
    comp_img = Image.fromarray(comp_arr, mode='RGBA')
    comp_img.save(output_path)

    # Plot singular values dropoff for R channel
    if plot_path:
        plt.figure()
        plt.semilogy(singular_values[0], marker='o', linestyle='-')
        plt.title('Singular Values Dropoff (R channel)')
        plt.xlabel('Index')
        plt.ylabel('Singular value (log scale)')
        plt.grid(True)
        plt.savefig(plot_path)
        plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SVD Image Compression with Component Outputs')
    parser.add_argument('input', help='Input image file path')
    parser.add_argument('output', help='Output image file path')
    parser.add_argument('-r', type=int, default=50, help='Rank for SVD compression')
    parser.add_argument('--plot', help='Path to save singular values plot')
    parser.add_argument('--components', action='store_true', help='Save U, S, Vt component images')
    args = parser.parse_args()

    compress_image(args.input, args.output, args.r, args.plot, save_components=args.components)
