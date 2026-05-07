import cv2
import rclpy
from camera_drivers.cameradriver import kinect_v1Driver
from rclpy.node import Node
from cv_bridge import CvBridge 
from sensor_msgs.msg import CompressedImage, Image
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy


class kinect_converter(Node):

    def __init__(self):
        super().__init__("kinect_converter")

        self.rgb_topic = "/kinect/rgb/compressed"
        self.depth_topic = "/kinect/depth/compressed"
        self.br = CvBridge()
        self.rgb_frame = None
        self.depth_frame = None

        self.msg = None
        self.kinect_rgb = kinect_v1Driver(mode=1)
        self.kinect_depth = kinect_v1Driver(mode=2)
        self.timer = self.create_timer(0.01, self.subscribe)
        self.timer = self.create_timer(1.0 / 30.0, self.publish_frames)

        self.init_publisher()

    def subscribe(self):
        rgb_frame = self.kinect_rgb.get_frame(1)
        depth_frame = self.kinect_depth.get_frame(2)

        if rgb_frame is None or depth_frame is None:
            print("No frame recieved")
            return

        self.rgb_frame = rgb_frame
        self.depth_frame = depth_frame
        

    def spin(self):
        rclpy.spin_once(self)
        rclpy.spin_once(self.kinect_rgb, timeout_sec=0.01)
        rclpy.spin_once(self.kinect_depth, timeout_sec=0.01)


    def init_publisher(self): 
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )
        self.publisher_rgb = self.create_publisher(CompressedImage, self.rgb_topic, qos_profile)
        self.publisher_depth = self.create_publisher(CompressedImage, self.depth_topic, qos_profile)

    def publish_frames(self):
        compressed_frame_rgb = self.compress_frame_jpeg(self.rgb_frame)
        compressed_frame_depth = self.compress_frame_png(self.depth_frame)
        
        if compressed_frame_depth is not None:
            img_msg = CompressedImage()
            img_msg.header.stamp = self.get_clock().now().to_msg()
            img_msg.format = "png"
            img_msg.data = compressed_frame_depth
            self.publisher_depth.publish(img_msg)     
            self.get_logger().info(f"Published compressed depth frame:")
            

        if compressed_frame_rgb is not None:
            img_msg = CompressedImage()
            img_msg.header.stamp = self.get_clock().now().to_msg()
            img_msg.format = "jpeg"
            img_msg.data = compressed_frame_rgb
            self.publisher_rgb.publish(img_msg)     
            self.get_logger().info("Published compressed rgb frame")

    def compress_frame_jpeg(self, frame):
        if frame is not None:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
            result, encimg = cv2.imencode('.jpg', frame, encode_param)
            if result:
                return encimg.tobytes()
            else:
                self.get_logger().warn("Failed to compress frame")

    def compress_frame_png(self, frame):
        if frame is not None:
            result, encimg = cv2.imencode('.png', frame)
            if result:
                return encimg.tobytes()
