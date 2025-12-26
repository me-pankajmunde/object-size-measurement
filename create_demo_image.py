#!/usr/bin/env python3
"""
Demo script to create a sample image for testing the object size measurement app.
This creates a simple test image with geometric shapes.
"""

import cv2
import numpy as np


def create_demo_image():
    """Create a demo image with various shapes for testing."""
    # Create a white background
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255
    
    # Draw reference object (a rectangle) - let's say this is 5.0 cm wide
    cv2.rectangle(img, (50, 250), (150, 350), (0, 0, 0), -1)
    cv2.putText(img, "REF: 5cm", (55, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    # Draw various shapes to measure
    # Circle
    cv2.circle(img, (300, 300), 60, (0, 0, 0), -1)
    
    # Rectangle
    cv2.rectangle(img, (450, 250), (600, 350), (0, 0, 0), -1)
    
    # Another rectangle
    cv2.rectangle(img, (200, 400), (350, 500), (0, 0, 0), -1)
    
    # Small square
    cv2.rectangle(img, (500, 450), (580, 530), (0, 0, 0), -1)
    
    # Add title
    cv2.putText(img, "Sample Objects - Leftmost is largest/reference (5cm wide)",
                (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    return img


if __name__ == "__main__":
    print("Creating demo image...")
    demo_img = create_demo_image()
    
    output_path = "example_objects.jpg"
    cv2.imwrite(output_path, demo_img)
    print(f"Demo image saved to: {output_path}")
    print("\nYou can now test the measurement app with:")
    print(f"python measure_object_size.py --image {output_path} --width 5.0 --output measured_output.jpg")
    print("\nThe leftmost rectangle is the largest object and will be used as reference (5cm wide).")
