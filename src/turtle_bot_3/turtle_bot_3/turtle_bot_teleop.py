#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from pynput import keyboard
import threading
import tty, termios, sys, os
import time


settings = termios.tcgetattr(sys.stdin)

cont = True
press = {'w': False, 'a': False, 's': False, 'd': False}

msg = """
Controla el TurtleBot
--------------------
Para moverse:
    w
a   s   d
--------------------
IMPORTANTE: para detener el nodo primero debes presionar la tecla ESC y lueco ctrl + c. 
El anterior procedimiento es importante para que la consola en la que estas no explote
CUIDADO: el programa siempre captara las teclas presionadas incluso si no estas en la consola

Al presionar ESC tendras que volver a reinicar el nodo para poder seguir controlando el TurtleBot

"""

def create_Listener(tecla):
    global press
    def on_press(key):
        try:
            if key.char == tecla:
                #print('tecla %s pressionada' % key)
                press[tecla] = True
        except AttributeError:
            pass
    def on_release(key):
        try:
            if key.char == tecla:
                #print('tecla %s soltada' % key)
                press[tecla] = False
        except AttributeError:
            pass
    return keyboard.Listener(on_press=on_press, on_release=on_release)

w = create_Listener('w')
a = create_Listener('a')
s = create_Listener('s')
d = create_Listener('d')

def stopThreads(key):
    global cont
    if key == keyboard.Key.esc:
        print('Deteniendo hilos')
        keyboard.Listener.stop(w)
        keyboard.Listener.stop(a)
        keyboard.Listener.stop(s)
        keyboard.Listener.stop(d)
        print('Hilos detenidos')
        cont = False
        return False

def startListeners():
    print(msg)

    w.start()
    a.start()
    s.start()
    d.start()

    stop = keyboard.Listener(on_press=stopThreads)
    stop.start()


class TurtleBotTeleopNode(Node):


    #global key

    def __init__(self, linearVel, angularVel):
        super().__init__("turtleController")
        self.linearVel = linearVel
        self.angularVel = angularVel
        self.msg = Twist()
        key = 0
        self.turtle_controller = self.create_publisher(Twist, "/turtlebot_cmdVel", 10)
        self.timer_ = self.create_timer(0.05, self.send_velocity_command)
        #self.timerkey_ = self.create_timer(0.05, self.get_keys)
        self.get_logger().info("Nodo turtle_bot_teleop creado correctamente")


    def send_velocity_command(self):
        self.msg.linear.x, self.msg.angular.z = 0.0, 0.0
        if(press['w']): #up
            self.msg.linear.x += 1.0 * self.linearVel
        if(press['s']): #down
            self.msg.linear.x += -1.0 * self.linearVel
        if(press['a']): #left
            self.msg.angular.z += 1.0 * self.angularVel
        if(press['d']): #right
            self.msg.angular.z += -1.0 * self.angularVel

        self.turtle_controller.publish(self.msg)


def getLinealVelocity():
    while True:
        entry = input("ingrese la velocidad lineal: ")
        try:
            entry = float(entry)
            if not(entry > 0 and entry < 5):
                raise Exception
            return entry
        except Exception as e:
            print("Error, el valor ingresado no es valido, vuelva a intentarlo")

def getAngularVelocity():
    while True:
        entry = input("ingrese la velocidad angular: ")
        try:
            entry = float(entry)
            if not(entry > 0 and entry < 5):
                raise Exception
            return entry
        except Exception as e:
            print("Error, el valor ingresado no es valido, vuelva a intentarlo")



def main(args=None):
    linealVel = getLinealVelocity()
    angularVel = getAngularVelocity()
    startListeners()
    rclpy.init(args=args)
    tty.setcbreak(sys.stdin)
    node = TurtleBotTeleopNode(linealVel, angularVel)
    while cont:
        rclpy.spin_once(node)
    rclpy.shutdown()
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    node.get_logger().info('Se termina la ejecucion del nodo')
    sys.exit(0)


if __name__ == '__main__':
    main()

