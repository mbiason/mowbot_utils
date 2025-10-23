import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion
import math


class FeedForwardMixer(Node):
    def __init__(self):
        super().__init__('feed_forward_mixer')
        
        # --- Parameters ---
        self.declare_parameter('kp_gain', 2.2)
        self.KP = self.get_parameter('kp_gain').get_parameter_value().double_value

        self.declare_parameter('kp_pitch', 0.3)
        self.KP_PITCH = self.get_parameter('kp_pitch').get_parameter_value().double_value
        
        # --- State ---
        self.current_roll = 0.0
        self.current_pitch = 0.0

        # --- ROS Comms ---
        self.odom_sub = self.create_subscription(
            Odometry, '/odometry/filtered', self.odom_callback, 10)
        self.cmd_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel_ff', 10)

    def odom_callback(self, msg):
        # Extract roll angle from the odometry's quaternion
        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
        self.current_roll = roll
        self.current_pitch = pitch

    def cmd_callback(self, msg):
        # Roll correction
        roll = self.current_roll
        if abs(roll) < 0.02:  # deadzone
            roll = 0.0
        omega_ff = self.KP * math.sin(roll)
        omega_ff = max(-0.25, min(0.25, omega_ff))  # clamp

        # Pitch correction
        pitch = self.current_pitch
        if abs(pitch) < 0.02:  # deadzone
            pitch = 0.0
        linear_ff = -self.KP_PITCH * math.sin(pitch)
        linear_ff = max(-0.20, min(0.20, linear_ff))  # clamp

        new_cmd = Twist()
        new_cmd.linear.x = msg.linear.x + linear_ff
        new_cmd.angular.z = msg.angular.z + omega_ff

        self.get_logger().info(
            f"ω_orig: {msg.angular.z:.2f}, ω_ff: {omega_ff:.2f}, ω_final: {new_cmd.angular.z:.2f} | "
            f"v_orig: {msg.linear.x:.2f}, v_ff: {linear_ff:.2f}, v_final: {new_cmd.linear.x:.2f}"
        )

        self.cmd_pub.publish(new_cmd)


def main(args=None):
    rclpy.init(args=args)
    mixer = FeedForwardMixer()
    rclpy.spin(mixer)
    mixer.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
