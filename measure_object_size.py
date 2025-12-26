#!/usr/bin/env python3
"""
Object Size Measurement Application using OpenCV
This application measures the size of objects using a reference object for calibration.
"""

import cv2
import numpy as np
import argparse
from scipy.spatial import distance as dist
from imutils import perspective, contours
import imutils


def midpoint(ptA, ptB):
    """Calculate the midpoint between two points."""
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def find_contours_and_measure(image, pixels_per_metric):
    """
    Find contours in the image and measure their dimensions.
    
    Args:
        image: Input image
        pixels_per_metric: Calibration value (pixels per unit of measurement)
    
    Returns:
        Annotated image with measurements
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Perform edge detection
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    
    # Find contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    # Sort contours from left to right
    (cnts, _) = contours.sort_contours(cnts)
    
    # Create output image
    output = image.copy()
    
    # Loop over the contours
    for c in cnts:
        # Skip small contours
        if cv2.contourArea(c) < 100:
            continue
        
        # Compute the rotated bounding box
        box = cv2.minAreaRect(c)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        
        # Order the points
        box = perspective.order_points(box)
        
        # Draw the contour
        cv2.drawContours(output, [box.astype("int")], -1, (0, 255, 0), 2)
        
        # Loop over the points and draw them
        for (x, y) in box:
            cv2.circle(output, (int(x), int(y)), 5, (0, 0, 255), -1)
        
        # Unpack the ordered bounding box
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
        
        # Draw midpoints
        cv2.circle(output, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(output, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(output, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(output, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
        
        # Draw lines between midpoints
        cv2.line(output, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
        cv2.line(output, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)
        
        # Calculate dimensions
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        
        # Calculate dimensions in real units
        dimA = dA / pixels_per_metric
        dimB = dB / pixels_per_metric
        
        # Draw dimensions on image
        cv2.putText(output, "{:.1f}".format(dimB),
                    (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 2)
        cv2.putText(output, "{:.1f}".format(dimA),
                    (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 2)
    
    return output


def calibrate_with_reference(image, reference_width):
    """
    Calibrate the pixels per metric using a reference object.
    
    Args:
        image: Input image containing reference object
        reference_width: Known width of reference object in desired units (e.g., cm, inches)
    
    Returns:
        pixels_per_metric: Calibration value
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Perform edge detection
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    
    # Find contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Sort contours and get the largest one (assumed to be reference object)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    if len(cnts) == 0:
        raise ValueError("No contours found in the image")

    # Use the largest contour as reference
    c = cnts[0]
    
    # Compute the rotated bounding box
    box = cv2.minAreaRect(c)
    box = cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    
    # Order the points
    box = perspective.order_points(box)
    (tl, tr, br, bl) = box
    
    # Calculate midpoints
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)
    
    # Calculate pixel distance
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
    
    # Calculate pixels per metric
    pixels_per_metric = dB / reference_width
    
    return pixels_per_metric


def process_image_file(image_path, reference_width, output_path=None):
    """
    Process an image file for object measurement.
    
    Args:
        image_path: Path to input image
        reference_width: Width of reference object in desired units
        output_path: Optional path to save output image
    """
    print(f"Loading image: {image_path}")
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return
    
    # Resize image for easier viewing
    image = imutils.resize(image, width=800)
    
    print(f"Calibrating with reference object (width: {reference_width} units)...")
    print("Using the largest object as reference.")
    
    try:
        pixels_per_metric = calibrate_with_reference(image, reference_width)
        print(f"Calibration complete! Pixels per metric: {pixels_per_metric:.2f}")
    except ValueError as e:
        print(f"Calibration error: {e}")
        return
    
    print("Measuring objects in the image...")
    output = find_contours_and_measure(image, pixels_per_metric)
    
    # Display the output
    cv2.imshow("Reference Calibration", image)
    cv2.imshow("Measurements", output)
    
    if output_path:
        cv2.imwrite(output_path, output)
        print(f"Output saved to: {output_path}")
    
    print("Press any key to close...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def process_webcam(reference_width):
    """
    Process webcam feed for real-time object measurement.
    
    Args:
        reference_width: Width of reference object in desired units
    """
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    pixels_per_metric = None
    calibrated = False
    
    print("\n" + "="*60)
    print("WEBCAM MODE - Object Size Measurement")
    print("="*60)
    print("\nInstructions:")
    print("1. Place your reference object in view")
    print("2. Press 'c' to calibrate using the reference object")
    print("3. After calibration, place objects to measure")
    print("4. Press 'r' to recalibrate")
    print("5. Press 'q' to quit")
    print("="*60 + "\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Resize frame
        frame = imutils.resize(frame, width=800)
        display_frame = frame.copy()
        
        # Add status text
        if not calibrated:
            status_text = f"NOT CALIBRATED - Press 'c' to calibrate (Ref width: {reference_width})"
            color = (0, 0, 255)  # Red
        else:
            status_text = "CALIBRATED - Measuring... (Press 'r' to recalibrate)"
            color = (0, 255, 0)  # Green
        
        cv2.putText(display_frame, status_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # If calibrated, perform measurements
        if calibrated and pixels_per_metric is not None:
            display_frame = find_contours_and_measure(frame, pixels_per_metric)
            cv2.putText(display_frame, status_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        cv2.imshow("Object Size Measurement", display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # Press 'c' to calibrate
        if key == ord('c'):
            print("\nCalibrating with current frame...")
            try:
                pixels_per_metric = calibrate_with_reference(frame, reference_width)
                calibrated = True
                print(f"Calibration successful! Pixels per metric: {pixels_per_metric:.2f}")
                print("You can now measure objects.\n")
            except Exception as e:
                print(f"Calibration failed: {e}")
                print("Please ensure reference object is visible and try again.\n")
        
        # Press 'r' to recalibrate
        elif key == ord('r'):
            calibrated = False
            pixels_per_metric = None
            print("\nCalibration reset. Press 'c' to recalibrate.\n")
        
        # Press 'q' to quit
        elif key == ord('q'):
            print("\nExiting...")
            break
    
    cap.release()
    cv2.destroyAllWindows()


def main():
    """Main function to run the object size measurement application."""
    parser = argparse.ArgumentParser(
        description="Measure object sizes using OpenCV with reference object calibration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Measure objects in an image with a 2.5 cm reference object
  python measure_object_size.py --image objects.jpg --width 2.5

  # Use webcam with a 3.0 inch reference object
  python measure_object_size.py --webcam --width 3.0

  # Save output image
  python measure_object_size.py --image objects.jpg --width 2.5 --output result.jpg
        """
    )
    
    parser.add_argument("-i", "--image", type=str,
                        help="Path to input image file")
    parser.add_argument("-w", "--width", type=float, required=True,
                        help="Width of reference object in desired units (e.g., cm, inches)")
    parser.add_argument("-o", "--output", type=str,
                        help="Path to output image (only for image mode)")
    parser.add_argument("--webcam", action="store_true",
                        help="Use webcam for real-time measurement")
    
    args = parser.parse_args()
    
    if args.webcam:
        process_webcam(args.width)
    elif args.image:
        process_image_file(args.image, args.width, args.output)
    else:
        parser.print_help()
        print("\nError: You must specify either --image or --webcam mode")


if __name__ == "__main__":
    main()
