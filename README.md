# Object Size Measurement

A Python application that measures object dimensions in images using OpenCV and computer vision techniques.

## Features

- Automatic object detection using contour detection
- Real-time size measurement in millimeters
- Support for reference object calibration
- Visual display of measurements with bounding boxes and midpoints
- Edge detection using Canny algorithm
- Handles multiple objects in a single image

## Requirements

- Python 3.x
- OpenCV
- imutils
- scipy
- numpy

## Installation

1. Clone this repository:
```bash
git clone https://github.com/me-pankajmunde/object-size-measurement.git
cd object-size-measurement
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your test image as `test.png` in the project root directory
2. Run the script:
```bash
python size_measurement.py
```

3. The application will:
   - Load the test image
   - Detect objects using contour detection
   - Calculate dimensions based on a reference metric
   - Display the annotated image with measurements
   - Press ESC key to exit

## How It Works

1. **Preprocessing**: The image is converted to grayscale and Gaussian blur is applied
2. **Edge Detection**: Canny edge detection identifies object boundaries
3. **Contour Detection**: Finds contours in the edge map
4. **Bounding Box**: Computes rotated bounding boxes for each object
5. **Measurement**: Calculates dimensions using Euclidean distance and reference calibration
6. **Display**: Shows measurements in millimeters on the annotated image

## Configuration

The `pixelsPerMetric` variable (default: 116) can be adjusted for calibration based on your specific setup and reference object.

## Notes

- Ensure good lighting and contrast for better detection
- The script includes special handling for common object sizes (25mm, 21x17mm, 8mm)
- Minimum contour area threshold is set to 100 pixels to filter noise

## License

This project is open source and available for educational and commercial use.