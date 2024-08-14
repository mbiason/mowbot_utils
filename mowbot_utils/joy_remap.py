import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy


class JoyRemap(Node):

    def __init__(self):
        super().__init__("joy_remap")
        self.subscription = self.create_subscription(
            Joy, "joy_in", self.listener_callback, 10
        )
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(Joy, "joy_out", 10)

    def listener_callback(self, in_msg):
        out_msg = Joy(header=in_msg.header, axes=in_msg.axes, buttons=in_msg.buttons)

        out_msg.buttons[0] = 1 if out_msg.axes[4] != 1.0 else 0
        out_msg.buttons[1] = 1 if out_msg.axes[5] != 1.0 else 0

        self.publisher_.publish(out_msg)


def main(args=None):
    rclpy.init(args=args)

    remapper = JoyRemap()

    rclpy.spin(remapper)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    remapper.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
