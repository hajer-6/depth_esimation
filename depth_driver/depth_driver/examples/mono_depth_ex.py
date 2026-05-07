from depth_driver.mono_depth_driver import monoDepth
from camera_drivers.cameradriver import monoDriver
import rclpy

WIDTH=15
FOCAL_LENGTH = 227.62354385*3

def main():
    rclpy.init(args=None)

    # ---- create object ---- #
    mono_subscriber = monoDriver()
    mono_depth = monoDepth(mono_object=mono_subscriber)

    mono_depth.set_KNOWNWIDTH(WIDTH) # to set width
    mono_depth.set_FOCAL_LENGTH(FOCAL_LENGTH) # to set focal length

    while rclpy.ok():
        # mono_depth.spin(timeout=0.1) 
        mono_depth.spin()

        frame, depth_value = mono_depth.get_depth() # To get depth of given frame
        mono_depth.display(frame,"black rec")

        print(depth_value)

        
if __name__ == '__main__':
    main()