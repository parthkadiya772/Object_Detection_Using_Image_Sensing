import cv2
from cv2 import aruco
import numpy as np
from pypylon import pylon
 # Initialize the aruco dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_50)
parameters = aruco.DetectorParameters_create()

# Connect to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Start grabbing continuously with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()

# Convert to OpenCV BGR format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        # Apply Canny edge detection
        canny = cv2.Canny(blur, 50, 150)
        # Find contours in the thresholded image
        contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Detect ArUco markers
        corners, ids, _ = aruco.detectMarkers(img, aruco_dict, parameters=parameters)
        # If any ArUco marker is detected
        if len(corners) > 0:
            print("Corners: ",len(corners))

            # Draw a box around the detected marker
            aruco.drawDetectedMarkers(img, corners, ids, (0, 0, 255))

            # Draw polygon around the marker
            int_corners = np.int0(corners)
            cv2.polylines(img, int_corners, True, (0, 255, 0), 2)

            # Aruco Perimeter
            aruco_perimeter = cv2.arcLength(corners[0], True)

            # Pixel to cm ratio
            pixel_cm_ratio = aruco_perimeter / 20
            pixel_mm_ratio = pixel_cm_ratio 
            #print("ArUco Marker Size (in mm): ", pixel_mm_ratio)
            # Iterate over the contours and add bounding boxes
            for contour in contours:
                rect = cv2.minAreaRect(contour)
                (x, y), (w, h), angle = rect              
                 # Get Width and Height of the Objects by applying the Ratio pixel to cm
                width= w / pixel_cm_ratio *10
                height = h / pixel_cm_ratio*10
                # Determine clip size based on width
                object_height = max(height,width)
                object_width = min(height,width)



                if (24 <= object_width <= 26 and 7 <= object_height <= 9) or (24 <= object_height <= 26 and 7 <= object_width <= 9):
                    # Display rectangle
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                    cv2.polylines(img, [box], True, (255, 0, 0), 2)
                    #cv2.putText(img, size, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    cv2.putText(img, "size 1  {} X".format(round(object_height, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 20, 250), 2)
                    cv2.putText(img, " {} mm".format(round(object_width, 1)), (int(x + 150), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 20, 250), 2)
                    cv2.putText(img, "Rotation: {} degrees".format(round(angle, 1)), (int(x - 100), int(y + 50)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 20, 250), 2)
                if (31 <= object_width <= 33 and 9 <= object_height <= 11) or (31 <= object_height <= 33 and 9 <= object_width <= 11):
                     # Display rectangle
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                    cv2.polylines(img, [box], True, (255, 0, 0), 2)
                    #cv2.putText(img, size, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    cv2.putText(img, "size 2  {} X".format(round(object_height, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 20, 250), 2)
                    cv2.putText(img, " {} mm".format(round(object_width, 1)), (int(x + 150), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 20, 250), 2)
                    cv2.putText(img, "Rotation: {} degrees".format(round(angle, 1)), (int(x - 100), int(y + 50)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 20, 250), 2)
                    #cv2.putText(img, "size 2"), (int(x - 100), int(y + 15), cv2.FONT_HERSHEY_PLAIN, 2, (100, 20, 250), 2)
                if (44 <= object_width <= 46 and 11 <= object_height <= 13) or (44 <= object_height <= 46 and 11 <= object_width <= 13):
                     # Display rectangle
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                    cv2.polylines(img, [box], True, (255, 0, 0), 2)
                    cv2.putText(img, "size 3  {} X".format(round(object_height, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 20, 250), 2)
                    cv2.putText(img, " {} mm".format(round(object_width, 1)), (int(x + 150), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 20, 250), 2)
                    cv2.putText(img, "Rotation: {} degrees".format(round(angle, 1)), (int(x - 100), int(y + 50)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 20, 250), 2)
                
        # Display the image
        cv2.imshow('title', img)
        k = cv2.waitKey(1)
        if k == 27:
            break

    grabResult.Release()

# Release the resource
camera.StopGrabbing()

cv2.destroyAllWindows()