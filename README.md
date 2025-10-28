# Subpixel Rendering Simulator

This project is a Python script that simulates the effect of subpixel rendering on a digital display. It processes an input image and generates an output that visualizes how the image might be reconstructed using individual red, green, and blue subpixels, with a focus on color and energy accuracy.

The simulation is highly configurable and implements advanced techniques to ensure the output is physically accurate, including:
-   **Perceptual Weighting**: Subpixels are sized according to their contribution to human perception of brightness (luminance).
-   **Energy Correction**: The brightness of each subpixel is scaled to compensate for its smaller area, ensuring the final pixel maintains its original color and intensity.
-   **Gamma-Correct Workflow**: All calculations are performed in a linear color space to correctly model the physics of light, preventing color shifts that occur when performing linear math on non-linear sRGB data.
-   **Pixel Grid Simulation**: An optional black border can be rendered around each pixel to simulate the physical grid of a real display, making the subpixel effect easier to inspect.


## How It Works

1.  **Linearization**: The input sRGB image is converted to a linear color space, where pixel values are directly proportional to light energy.
2.  **Upscaling**: A high-resolution canvas is created, scaling the image by a large factor (`SCALE_FACTOR`).
3.  **Subpixel Drawing**: For each pixel of the original image, the script draws R, G, and B rectangles (subpixels) onto the upscaled canvas.
    -   The **width** of each subpixel is determined by the `SUBPIXEL_WEIGHTS` (e.g., green is wider as it contributes most to luminance).
    -   The **intensity** of each subpixel is divided by its weight (`original_val / weight`). This crucial "energy correction" step ensures smaller subpixels emit more intense light, preserving the pixel's overall energy.
4.  **Downscaling**: The high-resolution canvas, now covered in a subpixel pattern, is downscaled back to the original image size using a `BOX` filter, which accurately averages the light energy.
5.  **Gamma Correction**: The final, downscaled linear image is converted back to the sRGB color space for correct viewing and saving.
6.  **Optional Zoom**: The final image can be slightly enlarged using a nearest-neighbor filter to allow for easy inspection of the resulting pixel patterns.

## How to Use

### 1. Setup

First, clone the repository and set up the environment.

```bash
git clone 
cd subpixel-simulator
```

It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Prepare Images

Place the images you want to process inside the `./images` directory. If the directory does not exist, create it.

### 3. Run the Script

Execute the script from your terminal:
```bash
python subpixel.py
```

The script will list all available images and prompt you to choose which ones to process. You can enter a comma-separated list of numbers or type `all` to process every image.

```
Available images:

 portrait.jpg
 landscape.png

Enter numbers to process (comma-separated) or 'all': 0,1
```

### 4. View the Output

The processed images will be saved in the `./output` directory.

## Configuration

You can modify the simulation's behavior by changing the global variables at the top of `subpixel.py`:

-   `IMAGES_DIR`: Directory for input images.
-   `OUTPUT_DIR`: Directory for output images.
-   `SCALE_FACTOR`: The internal upscaling factor. A higher value leads to more accurate subpixel sizing and less rounding error.
-   `SUBPIXEL_ORDER`: The layout of the subpixels (e.g., "RGB" or "BGR").
-   `SUBPIXEL_WEIGHTS`: The perceptual weights for R, G, and B. These should sum to 1.0. The default `[0.3, 0.4, 0.3]` gives green the most importance.
-   `FINAL_ZOOM_FACTOR`: Set greater than `1.0` to produce an upscaled final image for easier inspection.
-   `PIXEL_BORDER`: The width of the black border to draw around each pixel group on the upscaled canvas to simulate a physical pixel grid.
