from camera_drivers.kinectpublisher import kinect_converter
import rclpy


def main():
    rclpy.init(args=None)
    kinect_conv = kinect_converter()

    while rclpy.ok():
        kinect_conv.spin()
        
    rclpy.shutdown()