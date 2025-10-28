import os
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, shift

# --- Configuration ---
IMAGES_DIR = "./images"
OUTPUT_DIR = "./output"
SUBPIXEL_ORDER = "RGB"
SUBPIXEL_OFFSETS = [0.0, 1/3, 2/3]  # fraction of a pixel shift per channel
GAUSSIAN_SIGMA = 0.5               # optional blur to simulate optical mixing

def list_images(folder):
    valid_exts = {".png", ".jpg", ".jpeg", ".bmp"}
    return [f for f in os.listdir(folder)
            if os.path.splitext(f)[1].lower() in valid_exts]

def simulate_subpixel(img):
    """Simulate subpixel rendering using fractional shifts and blending."""
    arr = np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0
    h, w, _ = arr.shape

    rgb = np.zeros_like(arr)

    for i, c in enumerate(SUBPIXEL_ORDER):
        # Fractional shift along width (axis=1)
        shifted = shift(arr[..., i], shift=(0, SUBPIXEL_OFFSETS[i]), order=1, mode='nearest')
        rgb[..., i] = shifted

    # Apply mild Gaussian blur to simulate optical blending
    rgb = gaussian_filter(rgb, sigma=(GAUSSIAN_SIGMA, GAUSSIAN_SIGMA, 0))

    # Convert back to uint8
    rgb_disp = np.clip(rgb * 255, 0, 255).astype(np.uint8)
    return Image.fromarray(rgb_disp, "RGB")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    images = list_images(IMAGES_DIR)
    if not images:
        print("No images found in ./images")
        return

    print("\nAvailable images:\n")
    for i, name in enumerate(images):
        print(f"[{i}] {name}")

    choice = input("\nEnter numbers to process (comma-separated) or 'all': ").strip()
    if choice.lower() == "all":
        indices = range(len(images))
    else:
        indices = [int(x) for x in choice.split(",") if x.strip().isdigit()]

    print(f"\nProcessing {len(indices)} image(s)...\n")

    for idx in indices:
        filename = images[idx]
        path = os.path.join(IMAGES_DIR, filename)
        img = Image.open(path)
        print(f"→ {filename}")
        result = simulate_subpixel(img)
        name, ext = os.path.splitext(filename)
        out_path = os.path.join(OUTPUT_DIR, f"{name}_subpixel{ext}")
        result.save(out_path)

    print("\n✅ Done! Subpixel-simulated images saved in ./output")

if __name__ == "__main__":
    main()
