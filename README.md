# Taller de Robotica 1

## Cosas necesarias para correr

### Pynput  
Para la operación del nodo turtle_bot_teleop es necesario tener instalado la libreria de pynput.
* usar el comando "pip install pynput"

### Matplotlib
Para que el nodo de interface pueda graficar la posición del robot, es necesario tener instalado matplotlib
* Usar el comando "pip install pynput"


### Desactivar Wayland
Wayland y X11 se refiere a una configuración de la distro de Linux que termina mediando como el usuario y los programas interactuan con las ventanas y las interfaces. Pynput no funciona correctamente con Wayland, la cual usualmente esta activada por default. Para desactivarlo seguir las siguientes instrucciones:
* Abrir una terminal de comnados
* introducir el comando "sudo nano /etc/gdm3/custom.conf" (puede que en otras distros el mismo archivo que se tiene que modificar este en otro lugar, buscar en donde esta el archivo)
* descomentar la linea "WaylandEnable=false"
* guardar el archivo y salir
* Reiniciar la maquina



## Ejecución de cada nodo

### turtle_bot_teleop
Este nodo requiere de la librearia "pynput" para poder funcionar correctamente, se invoca con el comando "ros2 run turtle_bot_3 turtle_bot_teleop".  
Al iniciar el nodo, este primero pregunta por consola sobre las velocidades lineares y angulares para mandar al robot. Posteriormente, imprime en la consola un mensaje que explica como operar el robot.  
Especificamente, hay que presionar las teclas wasd para operar, y presionar la tecla Esc para salir


### turtle_bot_interface
Este nodo utiliza matplotlib para poder mostrar la grafica de posición del nodo.
[poner aqui una foto de la interface]
Se inicia con el comando "ros2 run turtle_bot_3 turtle_bot_interface". Y al iniciar, aparece una ventana preguntando si se quiere guardar la entrada de teleop. En caso de que si, otra ventana va abrirse pidiendo que guardemos un archivo .txt. Despues, se seguira con aparecer la interface.  
Para comenzar a graficar, se presiona el boton "Start". En caso de querer detener la grafica por cualquier motivo "Stop". Y tambien se puede limpiar el contenido de la grafica con "Clear". Para guardar la grafica, basta con pulsar el botn de guardar en la interfaz de matplotlib.  
Los demas botones se utilizan para llamar al servicio de player. El primero, crea un cliente, el cual es el que va a realizar las llamadas al servicio. Despues, se puede llamar al boton de "Send file" para elegir un archivo .txt que halla sido creado por la interface, y enviar el nombre del archivo al player".
Para terminar la ejecución, solo hay que cerrar la interface.

*Advertencia*
No hacer lo siguiente cuando se ejecuta la interface
* Enviar mensajes al player mientras que el nodo teleop esta ejecutando.
* No enviar mensajes cuando no hay cliente creado
* No intentar crear un cliente cuando un cliente ya halla sido creado.


### turtle_bot_player
Este nodo no depende de liberias. Pero su funcionamiento, y la del cliente en la interface depende del servicio personalizado que se crea en el paquete custom_interfaces.  
Se inicia con "ros2 run turtle_bot_3 turtle_bot_player". Y al iniciarlo, mostrara por consola cuando puede empezar a recibir peticiones. Cuando recibe una petición del cliente, mostrara el consola el archivo que le llego, y empezara a publicar su contenido en el topico de velocidad.  
De igual manera, avisara cuando halla terminado.  

## Entregables  

### Diagramas  
Los diagramas explicando el funcionamiento de los nodos se puede encontrar en la carpeta Docs, se hizo de esta manera ya que los diagramas eran tan grandes que extendian el informe a más de 6 paginas.

### Videos
Los videos generados para prueba del funcionamiento de todo eran demasiado grande para el repositorio. Se decidio incluir un link a OneDrive. Este se encuentra en la sección de anexos del informe.
