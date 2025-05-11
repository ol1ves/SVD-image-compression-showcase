# SVD Image Compression Showcase

This repository contains a simple Python script (`compress.py`) that demonstrates how to use **Singular Value Decomposition (SVD)** for image compression and visualization of SVD components (U, S, and Vt). It’s designed to experiment with truncation rank and see how it affects both image quality and singular‑value decay.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/SVD-image-compression-showcase.git
   cd SVD-image-compression-showcase
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # macOS/Linux
   .\.venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Basic compression

```bash
python compress.py <input_image> <output_image> -r <rank>
```

* `<input_image>`: Path to the source PNG/JPG image.
* `<output_image>`: Path where the compressed RGBA image will be saved.
* `-r <rank>`: Number of singular values (modes) to retain (default: 50).

### Additional options

* **Plot singular-value drop‑off**

  ```bash
  python compress.py in.png out.png -r 30 --plot dropoff.png
  ```

  Saves a semilog plot of singular values for the red channel to `dropoff.png`.

* **Save SVD components (U, S, Vt)**

  ```bash
  python compress.py in.png out.png -r 30 --components
  ```

  Produces per‑channel component images named `<base>_R_U.png`, `<base>_R_S.png`, `<base>_R_Vt.png`, etc.

---

## Examples

Inside the `test-inputs/ollie-the-polite-cat/` directory, you’ll find:

* **`otpc-original.png`**: Original RGBA source image.
* **`otpc-dropoff-graph.png`**: Sample singular-value decay plot.
* **`compressed/otpc-r{...}.png`**: Compressed outputs at various ranks.
* **`components/otpc_{R,G,B,A}_{U,S,Vt}.png`**: Visualizations of truncated SVD matrices.

Feel free to run your own experiments with different `-r` values and input images to see how compression quality and file size change.

---

## License

This project is released under the MIT License. Feel free to use, modify, and distribute for educational purposes.

---

## Contact
Feel free to contact me at oliversantana8686@gmail.com for any questions.

