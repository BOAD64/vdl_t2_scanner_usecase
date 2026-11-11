import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from sensor_msgs.msg import Image


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('camera_subscriber')

        self.subscription = self.create_subscription(
            msg_type=Image,
            topic='/boostercamera/head/combine/rgb',
            callback=self.listener_callback,
            qos_profile=1)
        
        self.subscription  # prevent unused variable warning

        self.latest_img_msg: Image | None = None
        self.timer = self.create_timer(0.25, self.timer_callback)


    def listener_callback(self, msg: Image):
        if self.latest_img_msg == None : print("---received!---")
        self.latest_img_msg = msg
        

    def process_image(self):
        if self.latest_img_msg == None: return
        img_msg = self.latest_img_msg

        print("---processing---")
        print(f"frame_id: {img_msg.header.frame_id}")
        print(f"height: {img_msg.height}")
        print(f"width: {img_msg.width}")
        print(f"encoding: {img_msg.encoding}")


    def timer_callback(self):
        self.process_image()


def main(args=None):
    try:
        with rclpy.init(args=args):
            minimal_subscriber = MinimalSubscriber()

            rclpy.spin(minimal_subscriber)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()