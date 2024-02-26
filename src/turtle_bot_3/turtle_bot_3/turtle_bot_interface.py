import tkinter as tk
from tkinter.messagebox import askyesno, showwarning, showinfo
from tkinter.filedialog import asksaveasfile, askopenfilename
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from geometry_msgs.msg import Twist
from custom_interfaces.srv import String
import threading

#Importar ros
import rclpy
from rclpy.node import Node

import inspect




x = []
y = []


class MainFrame(tk.Frame):
    """Clase que contiene la interfaz grafica principal de la aplicacion
        Esta clase extiende de tk.Frame. 

    """
    def __init__(self, root=None, Node=None):
        tk.Frame.__init__(self, master=root)
        self.pack(side='top', fill='both', expand=False, padx=5, pady=5)
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.ani = None
        self.aniFlag = False
        self.Node = Node
        self.setup_gui()
        
        
    def setup_gui(self):
        self.setup_label()
        self.setup_canvas(lim=5)
        self.setup_buttons()
        self.setup_client_buttons()
    

    def setup_label(self):
        label = tk.Label(self, text="Turtle_bot_3 interface", anchor=tk.CENTER, font=("Arial", 20))
        label.pack(side=tk.TOP, fill='both', expand=False)
        txtmsg = "Esta es la interfase de visualización de la posición del robot"
        label1 = tk.Label(self, text=txtmsg, anchor=tk.CENTER, font=("Arial", 11), pady=10)
        label1.pack(side=tk.TOP, fill='both', expand=False)


    
    def setup_canvas(self, lim=1):
        self.setAxes(lim)
        
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill='none', expand=False)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill='none', expand=False)
        
    
    def setup_buttons(self):
        height, width = 2, 10
        frm = tk.Frame(master=self, relief=tk.RAISED)
        frm.pack()
        self.btn1 = tk.Button(frm, text="Start", command=self.startAnimation, height=height, width=width)
        self.btn1.pack(side=tk.LEFT)
        self.btn2 = tk.Button(frm, text="Stop", command=self.stopAnimation, height=height, width=width)
        self.btn2.pack(side=tk.LEFT)
        self.btn3 = tk.Button(frm, text="Clear", command=self.clearPlot, height=height, width=width)
        self.btn3.pack(side=tk.LEFT)
    
    def setup_client_buttons(self):
        height, width = 2, 10
        frm = tk.Frame(master=self, relief=tk.RAISED)
        frm.pack()
        self.btn4 = tk.Button(frm, text="Create client", command=self.createClient, height=height, width=width)
        self.btn4.pack(side=tk.LEFT)
        self.btn5 = tk.Button(frm, text="Send file", command=self.sendFile, height=height, width=width)
        self.btn5.pack(side=tk.LEFT)
    
    
    def startAnimation(self):
        #TODO: invocar FuncAnimation para que empieze a animar
        #tiene que revisar si self.ani ya existe y si esta corriendo
        #Iniciar la animación
        if self.ani is None:
            self.ani = FuncAnimation(self.fig, self.animate, interval=1000, blit=False, cache_frame_data=False)
            self.fig.canvas.draw_idle()
            self.aniFlag = True
            self.Node.get_logger().info("Se inicio la animacion")
        else:
            if not(self.aniFlag):
                self.ani.event_source.start()
                self.aniFlag = True
                self.Node.get_logger().info("Se reanudo la animacion")
            else:
                self.Node.get_logger().info("La animacion ya esta corriendo")
                pass
            
    
    def stopAnimation(self):
        if self.aniFlag and self.ani:
            self.ani.event_source.stop()
            self.aniFlag = False
            self.Node.get_logger().info("Se detuvo la animacion")
        else:
            self.Node.get_logger().info("La animacion ya esta detenida o no se ha iniciado")

    def clearPlot(self):
        self.ax.cla()
        x.clear()
        y.clear()
        self.setAxes(lim = 5)
        self.ax.plot(x,y)
        self.fig.canvas.draw_idle()
        self.Node.get_logger().info("Se limpio el plot")
        
    
    def animate(self,i):
        #Estas lineas de aqui estan para poder hacer debug
        #print(x[-1])
        #print(y[-1])
        self.Node.get_logger().info("Se llamo a la funcion animate")
        self.ax.cla()
        self.ax.plot(x,y)
        self.setAxes(lim = 5)
        #return lines
        
    def createClient(self):
        if self.Node.cli:
            showwarning("Cliente ya creado", "El cliente ya fue creado")
        else:
            self.Node.cli = self.Node.create_client(String, "turtle_bot_player")
            self.Node.req = String.Request()
            showinfo("Cliente creado", "El cliente fue creado correctamente")

    def sendFile(self):
        if self.Node.cli:
            if not self.Node.cli.wait_for_service(timeout_sec=0.2):
                showwarning("Servicio no disponible", "El servicio no esta disponible")
            else:
                file = askopenfilename(filetypes=[("Text files", "*.txt")])
                if file:
                    self.Node.req.data = file
                    self.Node.future = self.Node.cli.call_async(self.Node.req)
                else:
                    showwarning("Archivo no seleccionado", "No se envio ningun archivo")
        else:
            showwarning("Cliente no creado", "Primero debe crear el cliente")
    
    def setAxes(self, lim=1):
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set(xlim=(-lim-lim*0.1, lim+lim*0.1), ylim=(-lim-lim*0.1, lim+lim*0.1))
        self.ax.grid()
        self.ax.set_aspect('equal')
    


class interfaceNode(Node):

    def __init__(self, file):
        super().__init__("interface_node")
        self.file = file
        if file:
            self.get_logger().info("Se Subscribira a el topico /turtlebot_cmdVel")	
            self.VelSub = self.create_subscription(Twist, "/turtlebot_cmdVel", self.velCallback, 10)
        
        self.get_logger().info("Se Subscribira a el topico /turtlebot_position")
        self.PosSub = self.create_subscription(Twist, "/turtlebot_position", self.posCallback, 10)
        #Declaracion del nombre del cliente para que luego no mande error.
        self.cli = None



    def velCallback(self, msg):
        self.file.write("{linearX},{angularZ}".format(linearX=msg.linear.x, angularZ=msg.angular.z))
        self.file.write("\n")

    def posCallback(self, msg):
        #self.get_logger().info('llego un mensaje')
        x.append(float(msg.linear.x))
        y.append(float(msg.linear.y))
        #print(x[-1])
        #print(y[-1])



        


def on_closing(root):
    root.quit()
    

def guardarInputs():
    """Funcion para preguntar si guarda los inputs del teleop en un archivo de texto
        y la ubicación del archivo de texto.
        El archivo lo gaurda como .txt por defecto

    Returns:
        file: un objeto de tipo file, abierto en modo escritura.
            Si el usuario no selecciona un archivo, retorna None
    """
    file = None
    flag = True
    while flag:
        if askyesno("¿Guardar entrada de teleop?", "¿Desea guardar las instrucciones enviadas por teleop?"):
            print("Se guardara la entrada de teleop")
            file = asksaveasfile(mode='w', defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file is None:
                print("No se selecciono un archivo")
            else:
                print("Se selecciono el archivo: ", file.name)
                flag = False
        else:
            print("No se guardara la entrada de teleop")
            flag = False
    return file


def spinNode(Node):
    try:
        rclpy.spin(Node)
    except KeyboardInterrupt:
        pass


def main():
    try:
        rclpy.init(args=None)
        file = guardarInputs()
        
        
        Node = interfaceNode(file)

        thread_spin = threading.Thread(target=lambda: spinNode(Node))
        thread_spin.start()

        root1 = tk.Tk()
        root1.title("Turtle_bot_3")
        root1.protocol("WM_DELETE_WINDOW", lambda: on_closing(root1))
        root1.resizable(False, False)
        app = MainFrame(root1,Node)
        root1.focus_force()
        root1.mainloop()

        Node.destroy_node()
        rclpy.shutdown()
        thread_spin.join()

        if file and not file.closed:
            print("Se cerrara el archivo de texto")
            file.close()
        
        print("se termino la ejecución del programa")
        
    except KeyboardInterrupt:
        print("Se cierra forzosamente el programa")
        Node.destroy_node()
        rclpy.shutdown()
        if file and not file.closed:
            file.close()
        print("se termino la ejecución del programa")

if __name__ == "__main__":
    main()