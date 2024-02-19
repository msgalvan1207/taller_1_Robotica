#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import getch

class TurtleBotTeleopNode(Node):

   #global key

   def get_keys(self): #gets keyboard input
       #key = 0
       k = ord(getch.getch()) #converts keypress to ord value
       if (k==119):
           key = 1 #up
       elif (k==115):
           key = 2 #down
       elif (k==97):
           key = 3 #left
       elif (k==100):
           key = 4 #right
       else:
           key = 0
       return key

   def __init__(self):
       super().__init__("turtleController")
       key = 0
       self.turtle_controller = self.create_publisher(Twist, "/turtlebot_cmdVel", 10)
       self.timer_ = self.create_timer(0.05, self.send_velocity_command)
       #self.timerkey_ = self.create_timer(0.05, self.get_keys)
       self.get_logger().info("Salsa, picante y nos fuimo")

   
       
   def send_velocity_command(self):
       input = self.get_keys()
       #input = key
       msg = Twist()
       if(input == 1): #up
           msg.linear.x = 1.0
           msg.angular.z = 0.0
       elif(input == 2): #down
           msg.linear.x = -1.0
           msg.angular.z = 0.0
       elif(input == 3): #left
           msg.linear.x = 0.0
           msg.angular.z = 1.0
       elif(input == 4): #right
           msg.linear.x = 0.0
           msg.angular.z = -1.0
       else:
           msg.linear.x = 0.0
           msg.angular.z = 0.0

       self.turtle_controller.publish(msg)



def main(args=None):
   rclpy.init(args=args)
   node = TurtleBotTeleopNode()
   rclpy.spin(node)
   rclpy.shutdown()


if __name__ == '__main__':
   main()

