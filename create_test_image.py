#!/usr/bin/env python3
"""
Generate a sample test image for the object size measurement script.
This creates a simple image with geometric shapes for testing purposes.
"""

import cv2
import numpy as np


def create_test_image():
    """Create a test image with geometric shapes"""
    # Create a light gray canvas (not pure white to avoid edge detection issues)
    img = np.ones((600, 800, 3), dtype=np.uint8) * 200
    
    # Draw a rectangle (25mm equivalent) - dark objects on light background
    cv2.rectangle(img, (100, 100), (200, 200), (50, 50, 150), -1)
    
    # Draw another rectangle (21x17mm equivalent)
    cv2.rectangle(img, (300, 150), (400, 230), (50, 150, 50), -1)
    
    # Draw a square (8x8mm equivalent)
    cv2.rectangle(img, (500, 180), (550, 230), (150, 50, 50), -1)
    
    # Draw a circle
    cv2.circle(img, (150, 400), 60, (100, 100, 50), -1)
    
    # Draw a polygon
    pts = np.array([[400, 350], [450, 420], [380, 480], [320, 440]], np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.fillPoly(img, [pts], (80, 50, 100))
    
    # Save the image
    cv2.imwrite('test.png', img)
    print("Test image 'test.png' created successfully!")
    print("You can now run: python size_measurement.py")


if __name__ == "__main__":
    create_test_image()
