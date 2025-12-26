#!/usr/bin/env python3
"""
Object Size Measurement using OpenCV
This script measures object dimensions in an image using contour detection
and reference calibration.
"""

# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2


# Constants
# Pixels per metric ratio - needs to be calibrated based on reference object
# This represents the number of pixels per inch in the reference setup
PIXELS_PER_METRIC = 116
# Conversion factor from inches to millimeters
INCH_TO_MM = 25.4

# Standard object size thresholds (in millimeters)
SIZE_25MM_MIN = 23.9
SIZE_25MM_MAX = 26.0
SIZE_21MM_MAX = 21.6
SIZE_17MM_MIN = 16.2
SIZE_8MM_MAX = 8.3
SIZE_8MM_MIN = 7.0

# Text display constants
TEXT_FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_SCALE = 0.60
TEXT_COLOR = (0, 0, 220)
TEXT_THICKNESS = 1
TEXT_OFFSET_X_LEFT = -15
TEXT_OFFSET_Y_TOP = -10
TEXT_OFFSET_X_RIGHT = 10


# For finding midpoint
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def main():
    # cap = cv2.VideoCapture(0)
    cv2.namedWindow("Size Of Object", cv2.WINDOW_NORMAL)
    image = cv2.imread("test.png")
    
    if image is None:
        print("Error: Could not load image 'test.png'. Please provide a test image.")
        return

    while True:
        try:
            # ret, image = cap.read()
            # roi = image1[90:320, 200:420]
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
            # perform edge detection, then perform a dilation + erosion to
            # close gaps in between object edges
            edged = cv2.Canny(gray, 50, 100)
            edged = cv2.dilate(edged, None, iterations=1)
            edged = cv2.erode(edged, None, iterations=1)

            # find contours in the edge map
            cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

            # sort the contours from left-to-right and initialize the reference object
            (cnts, _) = contours.sort_contours(cnts)
            refObj = None
            pixelsPerMetric = None

            # loop over the contours individually
            for c in cnts:
                # if the contour is not sufficiently large, ignore it
                if cv2.contourArea(c) < 100:
                    continue

                # compute the rotated bounding box of the contour
                box = cv2.minAreaRect(c)
                box = cv2.boxPoints(box)
                box = np.array(box, dtype="int")
                box = perspective.order_points(box)

                if refObj is None:
                    box1 = np.zeros(box.shape)
                    rcX = 0
                    rcY = 0
                    refObj = (box1, (rcX, rcY), PIXELS_PER_METRIC)

                # draw the contours on the image
                orig = image.copy()

                cv2.drawContours(image, [box.astype("int")], -1, (0, 255, 0), 1)
                cv2.drawContours(image, [refObj[0].astype("int")], -1, (0, 255, 0), 1)

                # Finding Height and width
                for (x, y) in box:
                    cv2.circle(orig, (int(x), int(y)), 3, (0, 0, 255), -1)

                # unpack the ordered bounding box, then compute the midpoint
                # between the top-left and top-right coordinates, followed by
                # the midpoint between bottom-left and bottom-right coordinates
                (tl, tr, br, bl) = box
                (tltrX, tltrY) = midpoint(tl, tr)
                (blbrX, blbrY) = midpoint(bl, br)

                # compute the midpoint between the top-left and top-right points,
                # followed by the midpoint between the top-righ and bottom-right
                (tlblX, tlblY) = midpoint(tl, bl)
                (trbrX, trbrY) = midpoint(tr, br)

                # draw the midpoints on the image
                cv2.circle(orig, (int(tltrX), int(tltrY)), 3, (255, 0, 0), -1)
                cv2.circle(orig, (int(blbrX), int(blbrY)), 3, (255, 0, 0), -1)
                cv2.circle(orig, (int(tlblX), int(tlblY)), 3, (255, 0, 0), -1)
                cv2.circle(orig, (int(trbrX), int(trbrY)), 3, (255, 0, 0), -1)

                # draw lines between the midpoints
                cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                         (255, 0, 255), 1)
                cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                         (255, 0, 255), 1)

                # compute the Euclidean distance between the midpoints
                dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

                # if the pixels per metric has not been initialized, then
                # compute it as the ratio of pixels to supplied metric
                if pixelsPerMetric is None:
                    pixelsPerMetric = PIXELS_PER_METRIC

                # compute the size of the object
                # Convert from pixels to inches, then to millimeters
                dimA = (dA / pixelsPerMetric) * INCH_TO_MM
                dimB = (dB / pixelsPerMetric) * INCH_TO_MM
                
                # Determine which standard size this object matches and display accordingly
                if SIZE_25MM_MIN <= dimA <= SIZE_25MM_MAX:
                    # 25mm x 25mm object
                    cv2.putText(orig, "{:.1f}mm".format(25),
                                (int(tltrX + TEXT_OFFSET_X_LEFT), int(tltrY + TEXT_OFFSET_Y_TOP)), 
                                TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
                    cv2.putText(orig, "{:.1f}mm".format(25),
                                (int(trbrX + TEXT_OFFSET_X_RIGHT), int(trbrY)), 
                                TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
                elif SIZE_25MM_MIN <= dimB <= SIZE_25MM_MAX:
                    # 25mm x 25mm object (alternate dimension)
                    cv2.putText(orig, "{:.1f}mm".format(25),
                                (int(tltrX + TEXT_OFFSET_X_LEFT), int(tltrY + TEXT_OFFSET_Y_TOP)), 
                                TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
                    cv2.putText(orig, "{:.1f}mm".format(25),
                                (int(trbrX + TEXT_OFFSET_X_RIGHT), int(trbrY)), 
                                TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
                elif dimA <= SIZE_21MM_MAX and dimB >= SIZE_17MM_MIN:
                    # 21mm x 17mm object
                    if dimA > dimB:
                        cv2.putText(orig, "{:.1f}mm".format(21),
                                    (int(tltrX + TEXT_OFFSET_X_LEFT), int(tltrY + TEXT_OFFSET_Y_TOP)), 
                                    TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
                        cv2.putText(orig, "{:.1f}mm".format(17),
                                    (int(trbrX + TEXT_OFFSET_X_RIGHT), int(trbrY)), 
                                    TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
                    else:
                        cv2.putText(orig, "{:.1f}mm".format(17),
                                    (int(tltrX + TEXT_OFFSET_X_LEFT), int(tltrY + TEXT_OFFSET_Y_TOP)), 
                                    TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
                        cv2.putText(orig, "{:.1f}mm".format(21),
                                    (int(trbrX + TEXT_OFFSET_X_RIGHT), int(trbrY)), 
                                    TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
                elif dimA <= SIZE_8MM_MAX and dimB >= SIZE_8MM_MIN:
                    # 8mm x 8mm object
                    cv2.putText(orig, "{:.1f}mm".format(8),
                                (int(tltrX + TEXT_OFFSET_X_LEFT), int(tltrY + TEXT_OFFSET_Y_TOP)), 
                                TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
                    cv2.putText(orig, "{:.1f}mm".format(8),
                                (int(trbrX + TEXT_OFFSET_X_RIGHT), int(trbrY)), 
                                TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
                else:
                    # Unknown size - display calculated dimensions
                    cv2.putText(orig, "{:.1f}mm".format(dimA),
                                (int(tltrX + TEXT_OFFSET_X_LEFT), int(tltrY + TEXT_OFFSET_Y_TOP)), 
                                TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
                    cv2.putText(orig, "{:.1f}mm".format(dimB),
                                (int(trbrX + TEXT_OFFSET_X_RIGHT), int(trbrY)), 
                                TEXT_FONT, TEXT_SCALE, TEXT_COLOR, TEXT_THICKNESS)
                # show the output image

                cv2.imshow("Size Of Object", orig)

            k = cv2.waitKey(2) & 0xFF
            if k == 27:
                break

        except Exception as e:
            print(f"Error: {e}")
            break

    # cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
