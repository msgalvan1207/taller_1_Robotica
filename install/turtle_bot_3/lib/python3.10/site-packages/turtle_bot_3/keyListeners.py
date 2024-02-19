from pynput import keyboard
import threading
import time


#Este archivo se utiliza para captar las teclas presionadas por el usuario
#para asi tambien guardar su estado. 

#Para poder utilizarlo correctamente:
#1. Importa keyListener.py al archivo
#2. Llama a la funcion startListeners() para iniciar los listeners
#3. Cada que requieras saber el estado de las teclas que se estan precionando llama a la función getPress()
#4. Para detener los listeners presiona la tecla ESC

cont = True
press = {'w': False, 'a': False, 's': False, 'd': False}

msg = """
    Controla el TurtleBot
    --------------------
    Para moverse:
        w
    a   s   d
    --------------------
    Para detener la toma de movimientos presiona ESC
    CUIDADO: el programa siempre captara las teclas presionadas incluso si no estas en la consola

    Al presionar ESC tendras que volver a reinicar el nodo para poder seguir controlando el TurtleBot

"""

def getPress():
    global press
    return press

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

# crear un thread que detenga todos los hilos
def printPress():
    global cont
    global press
    while cont:
        time.sleep(1)
        print(press)

printThread = threading.Thread(target=printPress)

def stopThreads(key):
    global cont
    if key == keyboard.Key.esc:
        print('Deteniendo hilos')
        keyboard.Listener.stop(w)
        keyboard.Listener.stop(a)
        keyboard.Listener.stop(s)
        keyboard.Listener.stop(d)
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



