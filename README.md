# Object Size Measurement with OpenCV

An OpenCV-based application that measures the size of objects in images or real-time video using a reference object for calibration.

## Features

- **Reference Object Calibration**: Use a known-size reference object to calibrate pixel-to-metric conversion
- **Multiple Object Measurement**: Automatically detect and measure multiple objects in a single image
- **Image Mode**: Process static images with saved output
- **Webcam Mode**: Real-time object measurement using your webcam
- **Visual Feedback**: Color-coded contours, bounding boxes, and dimension annotations

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/me-pankajmunde/object-size-measurement.git
cd object-size-measurement
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Image Mode

Measure objects in a static image using a reference object:

```bash
python measure_object_size.py --image <path_to_image> --width <reference_width>
```

**Example:**
```bash
# Measure objects where the reference object is 2.5 cm wide
python measure_object_size.py --image objects.jpg --width 2.5

# Save the output image
python measure_object_size.py --image objects.jpg --width 2.5 --output result.jpg
```

### Webcam Mode

Real-time object measurement using your webcam:

```bash
python measure_object_size.py --webcam --width <reference_width>
```

**Example:**
```bash
# Use webcam with a 3.0 inch reference object
python measure_object_size.py --webcam --width 3.0
```

**Webcam Controls:**
- **'c'**: Calibrate using the current frame (place reference object first)
- **'r'**: Reset calibration
- **'q'**: Quit the application

## How It Works

### 1. Reference Object Calibration

The application uses a reference object with a known width to establish the pixel-to-metric ratio:

1. Place your reference object in the image/frame (ensure it's the largest object by area)
2. The app detects the reference object's contour (automatically selects the largest contour)
3. Calculates pixels per unit based on the known width
4. This ratio is then used for all subsequent measurements

### 2. Object Detection and Measurement

For each detected object:
- Converts image to grayscale
- Applies Gaussian blur for noise reduction
- Performs Canny edge detection
- Finds external contours
- Computes minimum area rectangles around objects
- Calculates dimensions using the calibrated pixel ratio
- Annotates the image with measurements

### 3. Visual Output

- **Green boxes**: Detected object contours
- **Red dots**: Corner points of bounding boxes
- **Blue dots**: Midpoints of bounding box edges
- **Purple lines**: Dimension measurement lines
- **White text**: Actual dimensions in your specified units

## Tips for Best Results

1. **Good Lighting**: Ensure even lighting without harsh shadows
2. **Contrasting Background**: Use a plain background that contrasts with your objects
3. **Reference Object**: Place the reference object clearly visible and at the same depth as objects to measure
4. **Camera Position**: Keep the camera parallel to the surface for accurate measurements
5. **Object Size**: Objects should be at least 100 pixels in area to be detected

## Command-Line Arguments

| Argument | Short | Description | Required |
|----------|-------|-------------|----------|
| `--image` | `-i` | Path to input image file | No (unless not using --webcam) |
| `--width` | `-w` | Width of reference object in desired units | Yes |
| `--output` | `-o` | Path to save output image (image mode only) | No |
| `--webcam` | | Use webcam for real-time measurement | No |

## Examples

### Measuring with a Credit Card Reference

A standard credit card is 85.6 mm wide:

```bash
python measure_object_size.py --image items.jpg --width 85.6 --output measured.jpg
```

### Measuring with a US Quarter

A US quarter is 0.955 inches in diameter:

```bash
python measure_object_size.py --webcam --width 0.955
```

## Troubleshooting

**No objects detected:**
- Ensure sufficient contrast between objects and background
- Try adjusting lighting conditions
- Objects might be too small (< 100 pixels area)

**Inaccurate measurements:**
- Verify reference object dimensions
- Ensure camera is parallel to the surface
- Check that all objects are at the same depth as the reference

**Webcam not opening:**
- Check that no other application is using the webcam
- Try a different camera index if you have multiple cameras

## Dependencies

- **opencv-python**: Computer vision and image processing
- **numpy**: Numerical computations
- **scipy**: Scientific computing (distance calculations)
- **imutils**: Convenience functions for OpenCV

## License

This project is open source and available for educational and commercial use.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Acknowledgments

This application uses:
- OpenCV for computer vision operations
- Adrian Rosebrock's imutils library for OpenCV convenience functions