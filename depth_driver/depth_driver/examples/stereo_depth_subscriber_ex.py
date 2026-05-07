from depth_driver.stereo_depth_driver import StereoDepthDriver
import rclpy

def main():
    rclpy.init(args=None)

    # ---- create object ---- #
    stereo_depth_sub = StereoDepthDriver(subscriber=True, topic="stereo_depth") # defualt topic name is "stereo_depth"

    
    while rclpy.ok():
        stereo_depth_sub.spin(timeout=0.1)

        depth_frame = stereo_depth_sub.get_frame(normalize=False)

        if depth_frame is None:
            continue

        h, w = depth_frame.shape[:2]
        ## get_depth() returns: ( depth frame with a circle around the pixel processed , depth value )
        ## normalize determine whether to return real depth frame or normlized
        depth_frame, depth_value = stereo_depth_sub.get_depth(h//2 + 50, w//2 - 50, normalize = False, draw_circle = True) 

        stereo_depth_sub.display(frame_name="depth_frame", frame=depth_frame)
        print(depth_value)
        
    rclpy.shutdown() 