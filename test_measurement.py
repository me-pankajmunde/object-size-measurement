#!/usr/bin/env python3
"""
Test script for object size measurement without GUI display.
This script tests the core functionality without cv2.imshow() calls.
"""

import cv2
import numpy as np
import sys
sys.path.insert(0, '/home/runner/work/object-size-measurement/object-size-measurement')

from measure_object_size import calibrate_with_reference, find_contours_and_measure
import imutils


def test_measurement():
    """Test the measurement functionality."""
    print("="*60)
    print("Testing Object Size Measurement Application")
    print("="*60)
    
    # Load the demo image
    image_path = "example_objects.jpg"
    print(f"\n1. Loading image: {image_path}")
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return False
    
    print(f"   ✓ Image loaded successfully: {image.shape}")
    
    # Resize image
    image = imutils.resize(image, width=800)
    print(f"   ✓ Image resized to: {image.shape}")
    
    # Test calibration
    reference_width = 5.0  # The leftmost object is 5cm wide
    print(f"\n2. Calibrating with reference object (width: {reference_width} cm)")
    
    try:
        pixels_per_metric = calibrate_with_reference(image, reference_width)
        print(f"   ✓ Calibration successful!")
        print(f"   ✓ Pixels per metric: {pixels_per_metric:.2f} pixels/cm")
    except Exception as e:
        print(f"   ✗ Calibration failed: {e}")
        return False
    
    # Test measurement
    print(f"\n3. Measuring objects in the image...")
    try:
        output = find_contours_and_measure(image, pixels_per_metric)
        print(f"   ✓ Measurement successful!")
        print(f"   ✓ Output image shape: {output.shape}")
    except Exception as e:
        print(f"   ✗ Measurement failed: {e}")
        return False
    
    # Save output
    output_path = "test_output.jpg"
    cv2.imwrite(output_path, output)
    print(f"\n4. Output saved to: {output_path}")
    
    print("\n" + "="*60)
    print("All tests passed successfully! ✓")
    print("="*60)
    
    return True


if __name__ == "__main__":
    success = test_measurement()
    sys.exit(0 if success else 1)
