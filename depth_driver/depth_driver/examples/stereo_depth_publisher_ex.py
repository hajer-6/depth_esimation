from depth_driver.stereo_depth_driver import stereoDepthPub
from camera_drivers.cameradriver import stereoDriver
import rclpy

def main():
    rclpy.init(args=None)
    # ---- create object ---- #
    left_stereo_subscriber = stereoDriver(subscriber=True, topic="left_stereo")
    right_stereo_subscriber = stereoDriver(subscriber=True, topic="right_stereo")
    stereo = stereoDepthPub(left_stereo_object=left_stereo_subscriber, right_stereo_object=right_stereo_subscriber, compressed=False) # defualt topic name is "stereo_depth"

    while rclpy.ok():
        left_stereo_subscriber.spin(timeout=0.1)
        right_stereo_subscriber.spin(timeout=0.1)
        stereo.spin()

        # depth frame (not normalized)
        depth_frame = stereo.get_depth_frame()

        if depth_frame is None:
            continue
        
        ## normalize the frame
        norm = stereo.normalize(depth_frame)

        h, w = depth_frame.shape

        ## get_depth() returns: ( depth frame with a circle around the pixel processed , depth value )
        ## normalize determine whether to return real depth frame or normlized
        depth_frame, depth_value = stereo.get_depth(h//2 + 50, w//2 - 50, normalize = True, draw_circle = True) 

        stereo.display(depth_frame)
        print(depth_value)

