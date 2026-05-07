from depth_driver.depth_driver import depth_driver
import numpy as np
import cv2
import imutils
import math

FOCAL_LENGTH = 227.62354385*3
Fx = Fy = FOCAL_LENGTH
Cx = 178.53
Cy = 187.09
# --- Calibration constants ---


# --- Target detection area ---
TARGET_POINT = (320, 240)   # (x, y)
MAX_DISTANCE_PX = 200       # how far (in pixels) a contour's center can be from target
AREA_THRESHOLD = 500

# --- HSV range for BLACK color ---
# Black has low saturation and low value (brightness)
LOWER_COLOR = np.array([0, 0, 0])
UPPER_COLOR = np.array([180, 255, 50])  # Increase 50 -> 70 if your lighting is bright

class monoDepth(depth_driver):
    def __init__(self, node_name = "mono_depth_node", mono_object = None):
        self.mono_subscriber = mono_object
        self.depth = 0
        self.width=0
        self.focal=0
        self.pixel_width=0
        self.fov = 0

        super().__init__(node_name)
        self.timer = self.create_timer(0.01, self.__process)
       

    def set_KNOWNWIDTH(self,width):
        self.width=width
        return self.width
    
    def set_FOCAL_LENGTH(self,focal):
        self.focal=focal
        return self.focal
    
    def distance_to_camera(knownWidth, focalLength, perWidth):
        """Compute and return the distance from the marker to the camera."""
        return (knownWidth * focalLength) / perWidth
    
    def distance_to_camera(self, knownWidth, focalLength, perWidth):
        return (knownWidth * focalLength) / perWidth
    
    def sensorWidth(self, object_width, focal, pixel_width):
        distance = self.distance_to_camera(object_width, focal, pixel_width)
        sensor = object_width * focal / distance
        return sensor

    def FOV(self, sensor_width, focal):
        fov = 2 * math.atan(sensor_width / (2 * focal))
        return math.degrees(fov)

    
    def __process(self):
        frame = self.mono_subscriber.get_frame()
        
        if frame is None:
            print("no frame")
            return

        marker = self.find_marker(frame)
        if marker is not None:
            self.pixel_width = max(marker[1])
            dist = self.width * self.focal / self.pixel_width
            self.depth = dist
            sensor_width = self.sensorWidth(self.width, self.focal, self.pixel_width)
            self.fov = self.FOV(sensor_width, self.focal)

            box = cv2.boxPoints(marker)
            box = np.intp(box)
            cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)

            cv2.putText(frame, f"{dist:.2f} units", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            
        else:
            cv2.putText(frame, "No black object near target", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            
        cv2.putText(frame, f"FOV: {self.fov:.2f} deg", (50, 100),
                  cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)

        self.depth_frame= frame


    def get_depth(self):
        while self.depth_frame  is None:
            super().spin()
            
        return self.depth_frame , self.depth


    def find_marker(self, image):
        """Detects black contour nearest to TARGET_POINT and returns its rotated bounding box."""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Mask for black color
        mask = cv2.inRange(hsv, LOWER_COLOR, UPPER_COLOR)
        
        # Optional noise removal
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        if len(cnts) == 0:
            return None

        best_c = None
        best_dist = float("inf")

        for c in cnts:
            area = cv2.contourArea(c)
            if area < AREA_THRESHOLD:
                continue

            M = cv2.moments(c)
            if M["m00"] == 0:
                continue

            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            dist = np.sqrt((cx - TARGET_POINT[0])**2 + (cy - TARGET_POINT[1])**2)

            if dist < best_dist and dist < MAX_DISTANCE_PX:
                best_dist = dist
                best_c = c

        if best_c is None:
            return None

        rect = cv2.minAreaRect(best_c)
        return rect

    def get_internsic_values(self) :
        return Fx , Fy, Cx , Cy