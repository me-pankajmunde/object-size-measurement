# Quick Start Guide - Object Size Measurement

## Installation

```bash
# Clone the repository
git clone https://github.com/me-pankajmunde/object-size-measurement.git
cd object-size-measurement

# Install dependencies
pip install -r requirements.txt
```

## Quick Demo

Test the application with the provided demo image:

```bash
# Generate demo image
python create_demo_image.py

# Measure objects (reference is 5cm wide)
python measure_object_size.py --image example_objects.jpg --width 5.0 --output result.jpg

# Run automated test
python test_measurement.py
```

## Usage Modes

### 1. Image Mode (Static Images)

```bash
python measure_object_size.py --image <path> --width <reference_width>
```

**Example with a credit card reference (85.6mm):**
```bash
python measure_object_size.py --image photo.jpg --width 85.6 --output measured.jpg
```

### 2. Webcam Mode (Real-time)

```bash
python measure_object_size.py --webcam --width <reference_width>
```

**Interactive controls:**
- `c` - Calibrate with current frame (place reference object first)
- `r` - Reset calibration
- `q` - Quit

**Example with a US quarter (24.26mm):**
```bash
python measure_object_size.py --webcam --width 24.26
```

## Tips for Accurate Measurements

1. **Reference Object Selection**
   - Use an object with known dimensions (credit card, coin, ruler, etc.)
   - Ensure it's the largest object in the frame during calibration
   - Keep it on the same plane as objects you want to measure

2. **Lighting**
   - Use even, diffuse lighting
   - Avoid harsh shadows and glare

3. **Background**
   - Use a plain, contrasting background
   - Avoid cluttered backgrounds

4. **Camera Position**
   - Keep camera parallel to the surface
   - Maintain consistent distance from objects
   - Avoid perspective distortion

5. **Object Size**
   - Objects should be at least 100 pixels in area
   - Larger objects produce more accurate measurements

## Common Reference Objects

| Object | Width | Units |
|--------|-------|-------|
| Credit card | 85.6 | mm |
| Credit card | 3.37 | inches |
| US Quarter | 24.26 | mm |
| US Quarter | 0.955 | inches |
| Euro coin (2€) | 25.75 | mm |
| A4 Paper (short side) | 210 | mm |
| A4 Paper (long side) | 297 | mm |
| Letter Paper (short side) | 8.5 | inches |
| Letter Paper (long side) | 11 | inches |

## Understanding the Output

The application annotates images with:

- **Green boxes** - Object contours (detected objects)
- **Red dots** - Corner points of bounding boxes
- **Blue dots** - Midpoints of bounding box edges
- **Purple lines** - Dimension measurement lines
- **White text** - Measured dimensions in your specified units

## Troubleshooting

**Problem: No objects detected**
- Solution: Increase contrast between objects and background
- Solution: Ensure objects are large enough (>100 pixels area)
- Solution: Check lighting conditions

**Problem: Inaccurate measurements**
- Solution: Verify reference object dimensions
- Solution: Ensure camera is perpendicular to surface
- Solution: Keep all objects at the same depth/distance

**Problem: Webcam won't open**
- Solution: Close other apps using the webcam
- Solution: Check webcam permissions
- Solution: Try a different camera if you have multiple

**Problem: Calibration fails**
- Solution: Ensure reference object is clearly visible
- Solution: Make sure reference object has sufficient contrast
- Solution: Verify reference object is the largest in frame

## Advanced Usage

### Custom Output Path
```bash
python measure_object_size.py --image input.jpg --width 5.0 --output /path/to/output.jpg
```

### Different Units
You can use any unit (cm, mm, inches, feet) - just specify the reference width in that unit, and all measurements will be in the same unit.

```bash
# Measurements in centimeters
python measure_object_size.py --image photo.jpg --width 8.56

# Measurements in inches
python measure_object_size.py --image photo.jpg --width 3.37

# Measurements in millimeters
python measure_object_size.py --image photo.jpg --width 85.6
```

## Examples

### Example 1: Measuring screws and bolts
```bash
# Use a credit card as reference (85.6mm wide)
python measure_object_size.py --image screws.jpg --width 85.6 --output measured_screws.jpg
```

### Example 2: Real-time measurement for crafts
```bash
# Use a ruler marking (10cm) as reference
python measure_object_size.py --webcam --width 10.0
# Press 'c' when ruler is in frame, then measure your craft items
```

### Example 3: Package dimensions
```bash
# Use a US quarter (24.26mm) as reference
python measure_object_size.py --image packages.jpg --width 24.26
```

## Support

For issues or questions, please visit:
https://github.com/me-pankajmunde/object-size-measurement/issues
