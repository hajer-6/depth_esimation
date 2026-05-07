from camera_drivers.cameradriver import kinect_v2Driver
from depth_driver.kinect2_depth_driver import kinect_v2_depth
import rclpy

def main():
    rclpy.init(args=None)
    # ---- create object ---- #
    kinect2_subscriber = kinect_v2Driver(mode=2)
    kinect2_depth = kinect_v2_depth(kinect_object=kinect2_subscriber)
    
    while rclpy.ok():
        kinect2_depth.spin(timeout=0.1)

        # get depth frame (not normalized)
        depth_frame = kinect2_depth.get_depth_frame()
        if depth_frame is None:
            continue
        
        ## normalize the frame
        norm = kinect2_depth.normalize(depth_frame)

        h, w = depth_frame.shape

        # get_depth() returns: ( depth frame with a circle around the pixel processed , depth value in mm)
        # normalize determine whether to return real depth frame or normlized
        depth_frame, depth_value = kinect2_depth.get_depth(h//2, w//2, normalize = True) 

        kinect2_depth.display(depth_frame)
        print(depth_value)