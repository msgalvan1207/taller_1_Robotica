# Taller de Robotica 1

## Cosas necesarias para correr

### Pynput  
Para la operación del nodo turtle_bot_teleop es necesario tener instalado la libreria de pynput.
* usar el comando "pip install pynput"

### Desactivar Wayland
Wayland y X11 se refiere a una configuración de la distro de Linux que termina mediando como el usuario y los programas interactuan con las ventanas y las interfaces. Pynput no funciona correctamente con Wayland, la cual usualmente esta activada por default. Para desactivarlo seguir las siguientes instrucciones:
* Abrir una terminal de comnados
* introducir el comando "sudo nano /etc/gdm3/custom.conf" (puede que en otras distros el mismo archivo que se tiene que modificar este en otro lugar, buscar en donde esta el archivo)
* descomentar la linea "WaylandEnable=false"
* guardar el archivo y salir
* Reiniciar la maquina

### Matplotlib
Para que el nodo de interface pueda graficar la posición del robot, es necesario tener instalado matplotlib
* Usar el comando "pip install pynput"
