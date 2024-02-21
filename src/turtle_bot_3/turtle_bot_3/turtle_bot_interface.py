import tkinter as tk
from tkinter.messagebox import askyesno
from tkinter.filedialog import asksaveasfilename, asksaveasfile
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from geometry_msgs.msg import Twist
import threading

#Importar ros
import rclpy
from rclpy.node import Node




x = []
y = []


class MainFrame(tk.Frame):
    """Clase que contiene la interfaz grafica principal de la aplicacion
        Esta clase extiende de tk.Frame. 

    """
    def __init__(self, root=None):
        tk.Frame.__init__(self, master=root)
        self.pack(side='top', fill='both', expand=False, padx=5, pady=5)
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        self.ani = None
        self.setup_gui()
        
        
    def setup_gui(self):
        self.setup_label()
        self.setup_canvas(lim=5)
        self.setup_buttons()
    

    def setup_label(self):
        label = tk.Label(self, text="Turtle_bot_3 interface", anchor=tk.CENTER, font=("Arial", 20))
        label.pack(side=tk.TOP, fill='both', expand=False)
        txtmsg = "Esta es la interfase de visualización de la posición del robot"
        label1 = tk.Label(self, text=txtmsg, anchor=tk.CENTER, font=("Arial", 11), pady=10)
        label1.pack(side=tk.TOP, fill='both', expand=False)


    
    def setup_canvas(self, lim=1):
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set(xlim=(-lim-lim*0.1, lim+lim*0.1), ylim=(-lim-lim*0.1, lim+lim*0.1))
        self.ax.grid()
        self.ax.set_aspect('equal')
        
        
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
    
    
    def startAnimation(self):
        #TODO: invocar FuncAnimation para que empieze a animar
        #tiene que revisar si self.ani ya existe y si esta corriendo
        #Iniciar la animación
        print("se inicia la animacion")
        #self.ani = FuncAnimation(self.fig, self.animate, interval=1000)
    
    def stopAnimation(self):
        #TODO: invocar ani.event_source.stop() para detener la animación
        #Detener la animación
        print("se detiene la animacion")
        #self.ani.event_source.stop()

    def clearPlot(self):
        #TODO: invocar una funcion para que limpie la grafica
        #Limpiar la grafica (no se como lmao)
        print("se limpia la grafica wow")


class interfaceNode(Node):

    def __init__(self, file):
        super().__init__("interface_node")
        self.file = file
        if file:
            self.get_logger().info("Se Subscribira a el topico /turtlebot_cmdVel")	
            self.VelSub = self.create_subscription(Twist, "/turtlebot_cmdVel", self.velCallback, 10)
        
        self.get_logger().info("Se Subscribira a el topico /turtlebot_position")
        self.PosSub = self.create_subscription(Twist, "/turtlebot_position", self.posCallback, 10)



        def velCallback(self, msg):
            #TODO: logica para escribir en archivo de texto
            self.file.write("{linearX},{angularZ}".format(linearX=msg.linear.x, angularZ=msg.angular.z))
            self.file.write("\n")

        def posCallback(self, msg):
            #TODO: logica para actualizar el vector de posiciones
            x.append(msg.linear.x)
            y.append(msg.linear.y)

        


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

#TODO: escribir la clase del nodo de interface



def writeShitpost(**kwargs):
    #TODO: pasar la definicion de esta funcion en la clase del nodo
    #TODO: que esta funcion sea el callback del subscriptor que recibe los inputs del teleop
    #TODO: que esta funcion reciba el mensaje del subscriptor y que lo escriba en el archivo de texto
    #TODO: URGENTE: cambiar el nombre de esta funcion
    """Esta función contiene la logica para escribir dentro de un archivo de texto
        La idea seria pasar esta función al callback del subscriptor que recibe los inputs
        del teleop para que los escriba en un archivo de texto.
        
        Args:
            **kwargs: diccionario con los argumentos de la función
                file: archivo de texto en el que se escribira
            Estoy utilizando **kwargs para que la función sea mas flexible y pueda recibir
            mas o menos argumentos en el futuro
    """
    try:
        file = kwargs.get("file", None)
        msg = kwargs.get("msg", None)
        if file and not file.closed:
            file.write("La persona que lo lea es de indusplay :v")
            file.write("\n")
            file.write("But el que lo escribio tambien lo leyo")
            file.write("\n")
            file.write("Oh no papu")
            file.write("\n")
            file.close()
            print("se cerro el archivo")
        else:
            print("No se escribio nada")
    except KeyboardInterrupt:
        print("Se cierra forzosamente el programa")
        if file and not file.closed:
            file.close()    

def main():
    try:
        #rclpy.init(args=None)
        file = guardarInputs()
        
        
        Node = interfaceNode(file)
        thread_spin = threading.Thread(target=rclpy.spin, args=(Node,))
        thread_spin.start()
        
        #Estas lineas estan para probar escritura con asincronismo
        #Funciona correctamente
        #TODO: borrar estas lineas
        #thread_shitpost = threading.Thread(target=lambda: writeShitpost(file=file))
        #thread_shitpost.start()
    
        root1 = tk.Tk()
        root1.title("Turtle_bot_3")
        root1.geometry("1000x650")
        root1.protocol("WM_DELETE_WINDOW", lambda: on_closing(root1))
        root1.resizable(False, False)
        app = MainFrame(root1)
        root1.focus_force()
        root1.mainloop()
        
        rclpy.shutdown()
    except KeyboardInterrupt:
        print("Se cierra forzosamente el programa")
        if file and not file.closed:
            file.close()
        rclpy.shutdown()
        #sys.exit(0)

if __name__ == "__main__":
    main()