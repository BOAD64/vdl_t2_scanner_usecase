import cv2
import numpy as np
import rclpy

from cv2 import Mat
from numpy.typing import NDArray
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage


# TOPIC = '/boostercamera/head/combine/rgb'
TOPIC = '/booster_video_stream'
FPS = 30

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')

        type = Image
        if TOPIC == '/booster_video_stream':
            type = CompressedImage


        self.subscription = self.create_subscription(
            msg_type=type,
            topic=TOPIC,
            callback=self.listener_callback,
            qos_profile=1)
        
        self.subscription  # prevent unused variable warning

        self.latest_img_msg: Image | CompressedImage | None = None
        self.processed_image: Image | CompressedImage | None = None
        self.timer = self.create_timer(1.0/FPS, self.timer_callback)


    def listener_callback(self, msg: Image | CompressedImage):
        if self.latest_img_msg == None : print("---received!---")
        self.latest_img_msg = msg
        

    def process_msg(self):
        if self.latest_img_msg == None: return # No image found yet
        if self.latest_img_msg == self.processed_image: return # image already processed

        cv_img = None
        if type(self.latest_img_msg) is Image:
            img_msg = self.latest_img_msg
            cv_img = self.process_image(img_msg)
        elif type(self.latest_img_msg) is CompressedImage:
            img_msg = self.latest_img_msg
            cv_img = self.process_compressed_image(img_msg)

        if cv_img is not None:
            cv2.imshow(TOPIC, cv_img)
            cv2.waitKey(1)
        else:
            print("could not process image")


    def process_image(self, img_msg: Image):
        print("---processing---")
        print(f"frame_id: {img_msg.header.frame_id}")
        print(f"encoding: {img_msg.encoding}")
        print(f"height: {img_msg.height}")
        print(f"width: {img_msg.width}")
        
        yuv_height = int(img_msg.height * 1.5)
        yuv_img = np.frombuffer(img_msg.data, dtype=np.uint8).reshape((yuv_height, img_msg.step))[:, : img_msg.width]
        return cv2.cvtColor(yuv_img, cv2.COLOR_YUV2BGR_NV12)


    def process_compressed_image(self, img_msg: CompressedImage):
        print("---processing---")
        print(f"frame_id: {img_msg.header.frame_id}")
        print(f"format: {img_msg.format}")
        
        np_arr = np.frombuffer(img_msg.data, dtype=np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        

    def timer_callback(self):
        self.process_msg()


def main(args=None):
    try:
        with rclpy.init(args=args):
            minimal_subscriber = MinimalSubscriber()

            rclpy.spin(minimal_subscriber)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()