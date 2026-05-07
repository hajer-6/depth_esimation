from camera_drivers.cameradriver import kinect_v1Driver
from depth_driver.kinect1_depth_driver import kinect_v1_depth
import rclpy

def main():
    rclpy.init(args=None)
    # ---- create object ---- #
    kinect1_subscriber = kinect_v1Driver(mode=2)
    kinect1_depth = kinect_v1_depth(kinect_object=kinect1_subscriber)
    
    while rclpy.ok():
        kinect1_depth.spin(timeout=0.1)

        # get depth frame (not normalized)
        depth_frame = kinect1_depth.get_depth_frame()
        if depth_frame is None:
            continue
        
        ## normalize the frame
        norm = kinect1_depth.normalize(depth_frame)

        h, w = depth_frame.shape

        # get_depth() returns: ( depth frame with a circle around the pixel processed , depth value in mm)
        # normalize determine whether to return real depth frame or normlized
        depth_frame, depth_value = kinect1_depth.get_depth(h//2, w//2, normalize = True) 

        kinect1_depth.display(depth_frame)
        print(depth_value)