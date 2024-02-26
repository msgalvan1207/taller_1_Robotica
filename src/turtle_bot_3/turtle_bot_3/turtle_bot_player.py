import traceback
from custom_interfaces.srv import String
from geometry_msgs.msg import Twist
import time

import rclpy
from rclpy.node import Node



class turtleBotPlayer(Node):
    
    def __init__(self):
        super().__init__('turtle_bot_player')
        self.msg = Twist()
        self.turtle_player = self.create_publisher(Twist, "/turtlebot_cmdVel", 10)
        self.srv = self.create_service(String, 'turtle_bot_player', self.service_callback)
        self.get_logger().info('nodo turtle_bot_player creado correctamente')
        self.get_logger().info('Listo para recibir un archivo')
    
    def service_callback(self, request, response):
        self.get_logger().info('Se recibio el archivo: %s' % request.data)
        try:
            file = open(request.data, 'r')
            for line in file:
                data = line.split(',')
                self.msg.linear.x = float(data[0])
                self.msg.angular.z = float(data[1])
                self.turtle_player.publish(self.msg)
                time.sleep(0.05)
            file.close()
            self.get_logger().info('Archivo leido en su totalidad y movimientos publicados correctamente')
            self.get_logger().info('Listo para recibir un archivo')
            return response
        except Exception as e:
            print("fallo el servicio de publicar movimiento")
            print(traceback.format_exc())

def main(args=None):
    rclpy.init(args=args)
    turtle_bot_player = turtleBotPlayer()
    try:
        rclpy.spin(turtle_bot_player)
    except KeyboardInterrupt:
        print("\nFinalización del nodo con exito")
        


if __name__ == '__main__':
    main()