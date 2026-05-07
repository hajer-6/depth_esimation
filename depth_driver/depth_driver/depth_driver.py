from rclpy.node import Node
import rclpy
import cv2
 
class depth_driver(Node):
    def __init__(self, node_name = "depth_node"):
        super().__init__(node_name)

        self.depth_frame = None
        self.depth_timestamp = None

    def normalize(self, frame):
        
        if frame is None:
            self.get_logger().warn("No frame received yet to normalize")
            return
        self.normalized_frame = frame
        (min_val, max_val, _, _) = cv2.minMaxLoc(self.normalized_frame)
        if max_val == 0: max_val = 1
        self.normalized_frame = cv2.convertScaleAbs(self.normalized_frame, alpha=255.0/max_val, beta=- min_val * 255.0/max_val)
        
        return self.normalized_frame

    def get_depth(self, y, x, normalize = True, draw_circle = True):
        if self.depth_frame is None:
            self.get_logger().warn("No depth frame received yet to get depth value")
            return None
        
        depth_estimation = self.depth_frame
        depth_value = depth_estimation[y, x]

        if normalize:
            depth_estimation = self.normalize(self.depth_frame)
        if draw_circle:
            center_coordinates = (x, y)  
            radius = 10
            color = (255, 255, 255)
            thickness = 2                   
            cv2.circle(depth_estimation, center_coordinates, radius, color, thickness)
        
        return depth_estimation, depth_value
    
    def get_depth_frame(self):
        return self.depth_frame
    
    def get_timestamp(self):
        return self.depth_timestamp
    
    def display(self, frame, frame_name = "frame"):
        cv2.imshow(frame_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    
    def spin(self):
        rclpy.spin_once(self)
    
    def get_internsic_values(self) :
        pass