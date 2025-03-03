# TODO: Añadir el modo desarrollador en la función del jugador.
# Variables de modo de Juego:
mod = 0  
# 1: Consola  
# 2: Consola+Gráficos  
# 3: Gráficos

from tkinter import *
import tkinter.messagebox
import threading, platform
from random import randrange

# Variable global para llevar la posición en la que finaliza cada jugador
POSICION = 1
OS = platform.system()
imgDados = []
arregloDados = {}
Pan = ""
LB = ""
BTN = ""
desa = False

# Se crea (o limpia) el archivo de u
g = open("u.txt", "w")
g.close()

def registrarDato(dato):
    """
    Registra información en el archivo 'u.txt' para seguimiento o depuración.
    """
    f = open("u.txt", "a")
    f.write(str(dato) + "\n")
    f.close()

def capturarEntradaDados():
    """
    Captura el texto ingresado en la entrada de datos (usada en modo gráfico).
    """
    global caja_entrada_dados, texto_ingresado
    texto_ingresado = caja_entrada_dados.get()

def elegirOpcion():
    """
    Marca que se ha seleccionado una opción (utilizado en modo gráfico para elegir una opción de movimiento).
    """
    global seleccion
    seleccion = True

def iniciarModoGrafico():
    """
    Inicia el modo gráfico del juego.
    Crea la ventana principal, carga imágenes de los dados y fichas, y configura la pantalla de inicio.

    """
    global LB, BTN, Pan  # LB: etiqueta de bienvenida, BTN: botón para iniciar el juego
    Pan = Tk()  # Crea una nueva ventana
    # Carga las imágenes de los dados
    d1 = PhotoImage(file="dado1.gif")
    d2 = PhotoImage(file="dado2.gif")
    d3 = PhotoImage(file="dado3.gif")
    d4 = PhotoImage(file="dado4.gif")
    d5 = PhotoImage(file="dado5.gif")
    d6 = PhotoImage(file="dado6.gif")
    # Carga las imágenes de las fichas de cada color
    fRo = PhotoImage(file="fichaRojo.gif")
    fVe = PhotoImage(file="fichaVer.gif")
    fAm = PhotoImage(file="fichaAma.gif")
    fAz = PhotoImage(file="fichaAzul.gif")
    global imgFichas, arregloDados
    imgFichas = {}
    imgFichas["rojo"] = fRo
    imgFichas["verde"] = fVe
    imgFichas["amarillo"] = fAm
    imgFichas["azul"] = fAz
    # Se asignan las imágenes a cada valor del dado
    arregloDados[1] = d1
    arregloDados[2] = d2
    arregloDados[3] = d3
    arregloDados[4] = d4
    arregloDados[5] = d5
    arregloDados[6] = d6
    Pan.configure(bg="white")
    Pan.geometry("700x500+50+50")
    # Configuración del fondo del juego
    fondo = PhotoImage(file="fondo.gif")
    LF = Label(Pan, image=fondo)
    LF.img = fondo
    LF.pack()
    LB = Label(Pan, text="BIENVENIDOS A NUESTRO JUEGO", font=("Times New Roman", 30))
    LB.place(x=10, y=10)
    # Se crea el botón de inicio, adaptado para Windows y otros sistemas
    if OS == "Windows":
        BTN = Button(Pan, text="INICIAR", command=lambda: threading.Thread(target=comenzarJuego).start(),
                     font=("Algerian", 40))
    else:
        BTN = Button(Pan, text="INICIAR", command=comenzarJuego, font=("Algerian", 40))
    BTN.place(x=100, y=100)
    Pan.mainloop()

# La clase 'jugador' representa a cada participante del juego.
class jugador:
    def __init__(self, nombre, color, fichas, GanoJugador=False, UltimaFicha=None):
        """
        Inicializa un objeto jugador.
        nombre: nombre del jugador.
        color: color del jugador.
        fichas: lista de objetos 'ficha' pertenecientes al jugador.
        return: None.
        """
        self.nombre = nombre
        self.color = color
        self.fichas = fichas
        self.UltimaFicha = UltimaFicha
        self.GanoJugador = False
        self.Posicion = 0

    def establecerUltimaFicha(self, jugadorActual, Ficha):
        """
        Establece la última ficha usada por el jugador.
        """
        self.UltimaFicha = Ficha

    def lanzarUnDado(self, desa):
        """
        Lanza un dado para determinar quién comienza o para realizar movimientos.
        Si el modo desarrollador (desa) está activo, permite ingresar manualmente el valor del dado.
        desa: booleano que indica si se ingresa manualmente el valor del dado.
        return: número aleatorio entre 1 y 6 representando el dado lanzado.
        """
        global mod, texto_ingresado, caja_entrada_dados
        x = 0
        if not desa:
            if mod < 3:
                print("%s presione enter para tirar un dado:" % self.nombre)
                input()
                registrarDato("\n")
                x = randrange(1, 7)
                registrarDato(x)
                print("Su resultado es %d\n" % x)
            else:
                caja_entrada_dados.config(state="normal")
                caja_entrada_dados.delete(0, END)
                caja_entrada_dados.insert(0, "%s presione continuar" % self.nombre)
                caja_entrada_dados.config(state="readonly")
                inp = ""
                texto_ingresado = ""
                while inp == "":
                    inp = texto_ingresado
                x = randrange(1, 7)
        else:
            x = 0
            if mod == 3:
                caja_entrada_dados.config(state="normal")
                caja_entrada_dados.delete(0, END)
                caja_entrada_dados.insert(0, "Digite el valor del dado de " + self.nombre + ":\n")
            texto_ingresado = "7"
            while x <= 0 or x > 6:
                if mod < 3:
                    x = input("Digite el valor del dado de " + self.nombre + ":\n")
                else:
                    x = texto_ingresado
                registrarDato(x)
                try:
                    x = int(x)
                except:
                    x = 0
        # En modo gráfico se actualizan las imágenes de los dados
        if mod > 1:
            global L_DADOS1, L_DADOS2
            L_DADOS1.config(image=arregloDados[x], bg="green")
            L_DADOS1.img = arregloDados[x]
            L_DADOS2.config(image=None, bg="white")
        return x

    def lanzarDosDados(self, desa):
        """
        Lanza dos dados para definir los movimientos.
        Si el modo desarrollador está activo, permite ingresar manualmente el valor de ambos dados.
        desa: booleano que indica si se ingresa manualmente el valor.
        return: tupla con dos números aleatorios entre 1 y 6.
        """
        global mod, texto_ingresado, caja_entrada_dados
        x = 0
        y = 0
        if not desa:
            if mod < 3:
                print("%s presione enter para tirar dos dados:" % self.nombre)
                input()
                registrarDato("\n")
                x = randrange(1, 7)
                y = randrange(1, 7)
                registrarDato([x, y])
                print("Su resultado es %d %d\n" % (x, y))
            else:
                caja_entrada_dados.config(state="normal")
                caja_entrada_dados.delete(0, END)
                caja_entrada_dados.insert(0, "%s presione continuar" % self.nombre)
                caja_entrada_dados.config(state="readonly")
                inp = ""
                texto_ingresado = ""
                while inp == "":
                    inp = texto_ingresado
                x = randrange(1, 7)
                y = randrange(1, 7)
        else:
            if mod == 3:
                caja_entrada_dados.config(state="normal")
                caja_entrada_dados.delete(0, END)
                caja_entrada_dados.insert(0, "Digite el valor de los dados de " + self.nombre + ":\n")
            texto_ingresado = "7"
            lis = []
            while x <= 0 or x > 6 or y <= 0 or y > 6:
                if mod < 3:
                    print("%s digite el valor de los dados separados por un espacio" % self.nombre)
                    lis = input().split()
                else:
                    lis = texto_ingresado.split()
                registrarDato(lis)
                try:
                    x, y = tuple(map(int, lis))
                except:
                    x = 0
                    y = 0
        if mod > 1:
            global L_DADOS1, L_DADOS2
            L_DADOS1.config(image=arregloDados[x], bg="green")
            L_DADOS1.img = arregloDados[x]
            L_DADOS2.config(image=arregloDados[y], bg="green")
            L_DADOS2.img = arregloDados[y]
        return (x, y)

# La clase 'espacio' representa cada casilla del tablero, incluyendo las especiales.
class espacio(object):
    """
    Representa cada casilla del tablero.
    Considera todas las casillas, incluyendo las especiales (salida, seguro, llegada, etc.).
    """

    def __init__(self, numeroEspacio, etiqueta, x, y, tipoEspacio="normal", colorCasillaEspecial="ninguno", orientacion="Ninguna"):
        """
        Inicializa la casilla.
        numeroEspacio: número de la casilla.
        etiqueta: widget asociado (para modo gráfico).
        x: coordenada x.
        y: coordenada y.
        tipoEspacio: tipo de casilla (inicio, llegada, especial, seguro, salida).
        colorCasillaEspecial: color si es una casilla especial.
        return: None.
        """
        global mod
        self.colorCasillaEspecial = colorCasillaEspecial
        self.tipoEspacio = tipoEspacio
        self.numeroEspacio = numeroEspacio
        self.etiqueta = etiqueta
        if mod > 1:
            self.etiqueta.bind("<Enter>", self.alEntrar)
            self.etiqueta.bind("<Leave>", self.alSalir)
        self.orientacion = orientacion
        self.NoFichas = 0
        self.PosFicha = ""
        self.x = x
        self.y = y

    def alEntrar(self, event):
        """
        Muestra el número de la casilla cuando el cursor pasa sobre ella.
        """
        global L_NOMBRES
        L_NOMBRES.config(text=str(self.numeroEspacio))

    def alSalir(self, event):
        """
        Restaura el texto por defecto cuando el cursor sale de la casilla.
        """
        global L_NOMBRES
        L_NOMBRES.config(text="NOMBRES")

# La clase 'ficha' representa cada token que se mueve en el tablero.
class ficha:
    """
    Representa cada ficha (token) de un jugador.
    """

    def __init__(self, nombreFicha, colorFicha, espacioActual, estadoJuego="inicio"):
        """
        Inicializa la ficha.
        nombreFicha: identificador único (ej. 'rojo1').
        colorFicha: color de la ficha.
        espacioActual: objeto 'espacio' donde se ubica inicialmente.
        estadoJuego: estado actual (por defecto 'inicio').
        """
        global mod
        self.colorFicha = colorFicha
        self.espacioActual = espacioActual
        self.estadoJuego = estadoJuego
        self.nombreFicha = nombreFicha
        self.espacioActual = espacioActual
        etiqueta = ""
        if mod > 1:
            etiqueta = Label(Pan, image=imgFichas[colorFicha])
            etiqueta.img = imgFichas[colorFicha]
            # Posiciona la ficha según cuántas fichas ya hay en la casilla
            if self.espacioActual.NoFichas == 0:
                etiqueta.place(x=self.espacioActual.x + 40, y=self.espacioActual.y + 40, width=14, height=14)
                self.xI = self.espacioActual.x + 40
                self.yI = self.espacioActual.y + 40
            elif self.espacioActual.NoFichas == 1:
                etiqueta.place(x=self.espacioActual.x + 80, y=self.espacioActual.y + 40, width=14, height=14)
                self.xI = self.espacioActual.x + 80
                self.yI = self.espacioActual.y + 40
            elif self.espacioActual.NoFichas == 2:
                etiqueta.place(x=self.espacioActual.x + 40, y=self.espacioActual.y + 80, width=14, height=14)
                self.xI = self.espacioActual.x + 40
                self.yI = self.espacioActual.y + 80
            elif self.espacioActual.NoFichas == 3:
                etiqueta.place(x=self.espacioActual.x + 80, y=self.espacioActual.y + 80, width=14, height=14)
                self.xI = self.espacioActual.x + 80
                self.yI = self.espacioActual.y + 80
        self.espacioActual.NoFichas += 1
        self.etiqueta = etiqueta
        if mod > 1:
            self.etiqueta.bind("<Enter>", self.alEntrar)
            self.etiqueta.bind("<Leave>", self.alSalir)
        self.PosFicha = ""

    def alEntrar(self, event):
        """
        Muestra el nombre de la ficha cuando el cursor pasa sobre ella.
        """
        global L_NOMBRES
        L_NOMBRES.config(text=self.nombreFicha)

    def alSalir(self, event):
        """
        Restaura el texto por defecto cuando el cursor sale de la ficha.
        """
        global L_NOMBRES
        L_NOMBRES.config(text="NOMBRES")

    def mostrarPropiedades(self):
        """
        Retorna una cadena con las propiedades actuales de la ficha.
        return: String con información de la ficha.
        """
        return "Ficha %s: color= %s espacio=%s estado=%s" % (
            self.nombreFicha, self.colorFicha, self.espacioActual.numeroEspacio, self.estadoJuego)

    def removerFicha(self):
        """
        Elimina la ficha de la interfaz gráfica.
        """
        self.etiqueta.destroy()

    def moverFicha(self, NuevoEspacio):
        """
        Actualiza la posición de la ficha en el tablero.
        NuevoEspacio: objeto 'espacio' a donde se moverá la ficha.
        """
        global mod
        self.espacioActual.NoFichas -= 1
        if self.espacioActual.NoFichas == 1 and self.PosFicha == "A":
            self.espacioActual.PosFicha = "B"
        elif self.espacioActual.NoFichas == 1 and self.PosFicha == "B":
            self.espacioActual.PosFicha = "A"
        self.espacioActual = NuevoEspacio
        if self.espacioActual.tipoEspacio == "inicio":
            if mod > 1:
                self.etiqueta.place(x=self.xI, y=self.yI)
        elif self.espacioActual.NoFichas == 0 and self.espacioActual.orientacion == "vertical":
            if mod > 1:
                self.etiqueta.place(x=self.espacioActual.x, y=self.espacioActual.y + 7)
            self.espacioActual.PosFicha = "A"
            self.PosFicha = "A"
        elif self.espacioActual.NoFichas == 0 and self.espacioActual.orientacion == "horizontal":
            if mod > 1:
                self.etiqueta.place(x=self.espacioActual.x + 7, y=self.espacioActual.y)
            self.espacioActual.PosFicha = "A"
            self.PosFicha = "A"
        elif self.espacioActual.NoFichas == 1:
            if self.espacioActual.orientacion == "vertical" and self.espacioActual.PosFicha == "B":
                if mod > 1:
                    self.etiqueta.place(x=self.espacioActual.x, y=self.espacioActual.y + 7)
                self.PosFicha = "A"
            elif self.espacioActual.orientacion == "vertical" and self.espacioActual.PosFicha == "A":
                if mod > 1:
                    self.etiqueta.place(x=self.espacioActual.x, y=self.espacioActual.y + 33)
                self.PosFicha = "B"
            elif self.espacioActual.orientacion == "horizontal" and self.espacioActual.PosFicha == "B":
                if mod > 1:
                    self.etiqueta.place(x=self.espacioActual.x + 7, y=self.espacioActual.y)
                self.PosFicha = "A"
            elif self.espacioActual.orientacion == "horizontal" and self.espacioActual.PosFicha == "A":
                if mod > 1:
                    self.etiqueta.place(x=self.espacioActual.x + 33, y=self.espacioActual.y)
                self.PosFicha = "B"
        NuevoEspacio.NoFichas += 1

    def obtenerNumeroFicha(self):
        """
        Retorna el identificador de la ficha.
        """
        return self.nombreFicha

def DiseñarTablero():
    """
    Crea el tablero de juego, que se compone de:
      - 68 casillas comunes.
      - 7 casillas especiales para cada color (28 en total), 4 casillas de inicio y una de llegada.
    return: Lista de objetos de la clase 'espacio'.
    """
    global mod
    tablero = []
    for x in range(68):
        # Las casillas 5, 22, 39, 56 representan las salidas para cada color.
        labelF = ""
        labelI = ""
        orientacion = ""
        xF = 0
        yF = 0
        if mod > 1:
            if x + 1 in [y1 for y1 in range(1, 9)]:
                orientacion = "vertical"
                z = x
                if x + 1 == 5:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=z * 18 + 250, y=252, width=18, height=54)
                    labelI = Label(Pan, bg="#ED0D0D", borderwidth=0)
                    labelI.place(x=z * 18 + 252, y=254, width=14, height=50)
                else:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=z * 18 + 250, y=252, width=18, height=54)
                    labelI = Label(Pan, bg="white", borderwidth=0)
                    labelI.place(x=z * 18 + 252, y=254, width=14, height=50)
                xF = z * 18 + 252
                yF = 254
            elif x + 1 in [y1 for y1 in range(9, 17)]:
                orientacion = "horizontal"
                z = x - 8
                if x + 1 == 12:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=394, y=z * 18 + 306, width=54, height=18)
                    labelI = Label(Pan, bg="#ED0D0D", borderwidth=0)
                    labelI.place(x=396, y=z * 18 + 308, width=50, height=14)
                else:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=394, y=z * 18 + 306, width=54, height=18)
                    labelI = Label(Pan, bg="white", borderwidth=0)
                    labelI.place(x=396, y=z * 18 + 308, width=50, height=14)
                xF = 396
                yF = z * 18 + 308
            elif x + 1 == 17:
                orientacion = "horizontal"
                labelF = Label(Pan, bg="black", borderwidth=0)
                labelF.place(x=448, y=432, width=54, height=18)
                labelI = Label(Pan, bg="#04B112", borderwidth=0)
                labelI.place(x=450, y=434, width=50, height=14)
                xF = 450
                yF = 434
            elif x + 1 in [y1 for y1 in range(18, 26)]:
                orientacion = "horizontal"
                z = x - 17
                if x + 1 == 22:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=502, y=432 - z * 18, width=54, height=18)
                    labelI = Label(Pan, bg="#04B112", borderwidth=0)
                    labelI.place(x=504, y=434 - z * 18, width=50, height=14)
                else:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=502, y=432 - z * 18, width=54, height=18)
                    labelI = Label(Pan, bg="white", borderwidth=0)
                    labelI.place(x=504, y=434 - z * 18, width=50, height=14)
                yF = 434 - z * 18
                xF = 504
            elif x + 1 in [y1 for y1 in range(26, 34)]:
                orientacion = "vertical"
                z = x - 25
                if x + 1 == 29:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=z * 18 + 556, y=252, width=18, height=54)
                    labelI = Label(Pan, bg="#04B112", borderwidth=0)
                    labelI.place(x=z * 18 + 558, y=254, width=14, height=50)
                else:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=z * 18 + 556, y=252, width=18, height=54)
                    labelI = Label(Pan, bg="white", borderwidth=0)
                    labelI.place(x=z * 18 + 558, y=254, width=14, height=50)
                yF = 254
                xF = z * 18 + 558
            elif x + 1 == 34:
                orientacion = "vertical"
                labelF = Label(Pan, bg="black", borderwidth=0)
                labelF.place(x=682, y=198, width=18, height=54)
                labelI = Label(Pan, bg="#ECC811", borderwidth=0)
                labelI.place(x=684, y=200, width=14, height=50)
                yF = 200
                xF = 684
            elif x + 1 in [y1 for y1 in range(35, 43)]:
                orientacion = "vertical"
                z = x - 34
                if x + 1 == 39:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=682 - z * 18, y=144, width=18, height=54)
                    labelI = Label(Pan, bg="#ECC811", borderwidth=0)
                    labelI.place(x=684 - z * 18, y=146, width=14, height=50)
                else:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=682 - z * 18, y=144, width=18, height=54)
                    labelI = Label(Pan, bg="white", borderwidth=0)
                    labelI.place(x=684 - z * 18, y=146, width=14, height=50)
                yF = 146
                xF = 684 - z * 18
            elif x + 1 in [y1 for y1 in range(43, 51)]:
                orientacion = "horizontal"
                z = x - 42
                if x + 1 == 46:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=502, y=126 - z * 18, width=54, height=18)
                    labelI = Label(Pan, bg="#ECC811", borderwidth=0)
                    labelI.place(x=504, y=128 - z * 18, width=50, height=14)
                else:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=502, y=126 - z * 18, width=54, height=18)
                    labelI = Label(Pan, bg="white", borderwidth=0)
                    labelI.place(x=504, y=128 - z * 18, width=50, height=14)
                yF = 128 - z * 18
                xF = 504
            elif x + 1 == 51:
                orientacion = "horizontal"
                labelF = Label(Pan, bg="black", borderwidth=0)
                labelF.place(x=448, y=0, width=54, height=18)
                labelI = Label(Pan, bg="#2926DA", borderwidth=0)
                labelI.place(x=450, y=2, width=50, height=14)
                yF = 2
                xF = 450
            elif x + 1 in [y1 for y1 in range(52, 60)]:
                orientacion = "horizontal"
                z = x - 51
                if x + 1 == 56:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=394, y=z * 18, width=54, height=18)
                    labelI = Label(Pan, bg="#2926DA", borderwidth=0)
                    labelI.place(x=396, y=z * 18 + 2, width=50, height=14)
                else:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=394, y=z * 18, width=54, height=18)
                    labelI = Label(Pan, bg="white", borderwidth=0)
                    labelI.place(x=396, y=z * 18 + 2, width=50, height=14)
                yF = z * 18 + 2
                xF = 396
            elif x + 1 in [y1 for y1 in range(60, 68)]:
                orientacion = "vertical"
                z = x - 59
                if x + 1 == 63:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=376 - z * 18, y=144, width=18, height=54)
                    labelI = Label(Pan, bg="#2926DA", borderwidth=0)
                    labelI.place(x=378 - z * 18, y=146, width=14, height=50)
                else:
                    labelF = Label(Pan, bg="black", borderwidth=0)
                    labelF.place(x=376 - z * 18, y=144, width=18, height=54)
                    labelI = Label(Pan, bg="white", borderwidth=0)
                    labelI.place(x=378 - z * 18, y=146, width=14, height=50)
                yF = 146
                xF = 378 - z * 18
            elif x + 1 == 68:
                orientacion = "vertical"
                labelF = Label(Pan, bg="black", borderwidth=0)
                labelF.place(x=250, y=198, width=18, height=54)
                labelI = Label(Pan, bg="#ED0D0D", borderwidth=0)
                labelI.place(x=252, y=200, width=14, height=50)
                yF = 200
                xF = 252
        # Se asigna el tipo de casilla según su número
        if x + 1 in [5, 22, 39, 56]:
            NuevaCasilla = espacio(x + 1, labelI, xF, yF, "salida", "ninguno", orientacion)
        elif x + 1 in [12, 17, 29, 34, 46, 51, 63, 68]:
            NuevaCasilla = espacio(x + 1, labelI, xF, yF, "seguro", "ninguno", orientacion)
        else:
            NuevaCasilla = espacio(x + 1, labelI, xF, yF, 'normal', "ninguno", orientacion)
        tablero.append(NuevaCasilla)
    label = ""
    if mod > 1:
        label = Label(Pan, bg="#ED0D0D", borderwidth=0)
        label.place(x=250, y=306, height=144, width=144)
        label = Label(Pan, bg="white", borderwidth=0)
        label.place(x=255, y=311, height=134, width=134)
    tablero.append(espacio(69, label, 255, 311, "inicio", "rojo"))
    if mod > 1:
        label = Label(Pan, bg="#04B112", borderwidth=0)
        label.place(x=556, y=306, height=144, width=144)
        label = Label(Pan, bg="white", borderwidth=0)
        label.place(x=561, y=311, height=134, width=134)
    tablero.append(espacio(70, label, 561, 311, "inicio", "verde"))
    if mod > 1:
        label = Label(Pan, bg="#ECC811", borderwidth=0)
        label.place(x=556, y=0, height=144, width=144)
        label = Label(Pan, bg="white", borderwidth=0)
        label.place(x=561, y=5, height=134, width=134)
    tablero.append(espacio(71, label, 561, 5, "inicio", "amarillo"))
    if mod > 1:
        label = Label(Pan, bg="#2926DA", borderwidth=2)
        label.place(x=250, y=0, height=144, width=144)
        label = Label(Pan, bg="white", borderwidth=0)
        label.place(x=255, y=5, height=134, width=134)
    tablero.append(espacio(72, label, 255, 5, "inicio", "azul"))
    for x in range(28):
        if x < 7:
            z = x
            if mod > 1:
                labelF = Label(Pan, bg="black", borderwidth=0)
                labelF.place(x=z * 18 + 268, y=198, width=18, height=54)
                labelF = Label(Pan, bg="#ED0D0D", borderwidth=0)
                labelF.place(x=z * 18 + 270, y=200, width=14, height=50)
            NuevaCasilla = espacio(72 + x + 1, labelF, z * 18 + 270, 200, "especial", "rojo", "vertical")
        elif x < 14:
            z = x - 7
            if mod > 1:
                labelF = Label(Pan, bg="black", borderwidth=0)
                labelF.place(x=448, y=414 - z * 18, width=54, height=18)
                labelF = Label(Pan, bg="#04B112", borderwidth=0)
                labelF.place(x=450, y=416 - z * 18, width=50, height=14)
            NuevaCasilla = espacio(72 + x + 1, labelF, 450, 416 - z * 18, "especial", "verde", "horizontal")
        elif x < 21:
            z = x - 14
            if mod > 1:
                labelF = Label(Pan, bg="black", borderwidth=0)
                labelF.place(x=664 - z * 18, y=198, width=18, height=54)
                labelF = Label(Pan, bg="#ECC811", borderwidth=0)
                labelF.place(x=666 - z * 18, y=200, width=14, height=50)
            NuevaCasilla = espacio(72 + x + 1, labelF, 666 - z * 18, 200, "especial", "amarillo", "vertical")
        else:
            z = x - 21
            if mod > 1:
                labelF = Label(Pan, bg="black", borderwidth=0)
                labelF.place(x=448, y=z * 18 + 18, width=54, height=18)
                labelF = Label(Pan, bg="#2926DA", borderwidth=0)
                labelF.place(x=450, y=z * 18 + 20, width=50, height=14)
            NuevaCasilla = espacio(72 + x + 1, labelF, 450, z * 18 + 20, "especial", "azul", "horizontal")
        tablero.append(NuevaCasilla)
    lab = ""
    if mod > 1:
        imagen = PhotoImage(file="copa.gif")
        lab = Label(Pan, bg="black")
        lab.place(x=394, y=144, width=162, height=162)
        lab = Label(Pan, image=imagen)
        lab.img = imagen
        lab.place(x=399, y=149, width=152, height=152)
    tablero.append(espacio(101, lab, 399, 149, "llegada"))
    return tablero

def GenerarJugadoresYFichas(tablero, numeroJugadores, nombres):
    """
    Crea las fichas de cada jugador en el tablero e inicializa cada objeto de la clase 'jugador'.
    tablero: objeto que representa el tablero.
    numeroJugadores: número total de jugadores.
    nombres: tupla con los nombres de cada jugador.
    return: lista de objetos de la clase 'jugador'.
    """
    jugadores = []
    for x in range(numeroJugadores):
        fichas = []
        if x == 0:
            # Para el primer jugador, se asignan las fichas rojas.
            for z in range(4):
                NuevaFicha = ficha("rojo%d" % (z + 1), "rojo", tablero[68])
                fichas.append(NuevaFicha)
            jugadores.append(jugador(nombres[0], "rojo", fichas))
            jugadores[0].UltimaFicha = jugadores[0].fichas[3]
        elif x == 1:
            for z in range(4):
                NuevaFicha = ficha("verde%d" % (z + 1), "verde", tablero[69])
                fichas.append(NuevaFicha)
            jugadores.append(jugador(nombres[1], "verde", fichas))
            jugadores[1].UltimaFicha = jugadores[1].fichas[3]
        elif x == 2:
            for z in range(4):
                NuevaFicha = ficha("amarillo%d" % (z + 1), "amarillo", tablero[70])
                fichas.append(NuevaFicha)
            jugadores.append(jugador(nombres[2], "amarillo", fichas))
            jugadores[2].UltimaFicha = jugadores[2].fichas[3]
        elif x == 3:
            for z in range(4):
                NuevaFicha = ficha("azul%d" % (z + 1), "azul", tablero[71])
                fichas.append(NuevaFicha)
            jugadores.append(jugador(nombres[3], "azul", fichas))
            jugadores[3].UltimaFicha = jugadores[3].fichas[3]
    return jugadores

def solicitarDatos():
    """
    Solicita al usuario el número total de jugadores y, posteriormente, los nombres de cada uno.
    return: lista de nombres.
    """
    global mod, caja_entrada_dados, boton_entrada_dados, texto_ingresado
    texto_ingresado = ""
    n = 0
    if mod > 1:
        Esp = Label(Pan, text="Esperando Jugadores...", bg="white", fg="black", font=("Times New Roman", 32))
        Esp.place(y=0, x=0)
        if mod < 3:
            Ins = Label(Pan, text="Digite las entradas en su input de consola...", bg="black", fg="white",
                        font=("Times New Roman", 17))
            Ins.place(y=400, x=0)
        if mod == 3:
            caja_entrada_dados = Entry(Pan, font='Helvetica 20', borderwidth=0)
            caja_entrada_dados.place(x=0, y=500, width=550, height=50)
            boton_entrada_dados = Button(Pan, text='Continuar', font=("Times New Roman", 20), fg="white",
                                         command=capturarEntradaDados, bg="blue", borderwidth=0)
            boton_entrada_dados.place(x=550, y=500, width=150, height=50)
            caja_entrada_dados.delete(0, END)
            caja_entrada_dados.insert(0, "¿Cuántos jugadores van a ingresar?")
    while (n <= 0 or n > 4):
        if mod < 3:
            print("¿Cuántos jugadores ingresarán?:")
            n = input()
            registrarDato(n)
        else:
            n = texto_ingresado
        try:
            n = int(n)
        except:
            n = 0
    nombres = []
    Eti = []
    for z in range(n):
        color = ""
        if z == 0: color = "#ED0D0D"
        if z == 1: color = "#04B112"
        if z == 2: color = "#ECC811"
        if z == 3: color = "#2926DA"
        if mod < 3:
            print("Digite el nombre del jugador %d" % (z + 1))
            nombre = ""
        else:
            caja_entrada_dados.delete(0, END)
            caja_entrada_dados.insert(0, "Digite el nombre del jugador %d" % (z + 1))
        nombre = ""
        texto_ingresado = ""
        while (len(nombre) <= 0 or len(nombre) > 10):
            if mod < 3:
                nombre = input()
                registrarDato(n)
            else:
                nombre = texto_ingresado
        if mod > 1:
            Eti.append(Label(Pan, text="Jugador %d: " % (z + 1) + nombre, font=("Times New Roman", 30), bg=color, fg="white"))
            Eti[z].place(y=60 * z + 100)
        nombres.append(nombre)
    x = ""
    if mod == 3:
        caja_entrada_dados.delete(0, END)
        caja_entrada_dados.insert(0, "Presione continuar (ó digite la contraseña para modo desarrollador):")
        texto_ingresado = ""
        while x == "":
            x = texto_ingresado
    else:
        print("Presione enter para continuar (ó digite la contraseña para modo desarrollador):")
        x = input()
    if x == "mazamorra":
        global desa
        desa = True
    registrarDato("\n")
    if mod > 1:
        for x in Eti:
            x.destroy()
        Esp.destroy()
        if mod < 3: Ins.destroy()
    return nombres

def obtenerMayorValor(listaJugadores):
    """
    Obtiene el valor máximo lanzado por los jugadores.
    listaJugadores: lista de objetos 'jugador'.
    return: el mayor valor obtenido.
    """
    arreglo = []
    for i in range(len(listaJugadores)):
        arreglo.append(listaJugadores[i].valor)
    return max(arreglo)

def determinarOrdenDeJuego(ListaJugadores, modoDesarrollador=False):
    """
    Determina el orden de juego según el lanzamiento de dados.
    Cada jugador lanza un dado y quien obtiene el valor máximo comienza.
    ListaJugadores: lista de objetos 'jugador'.
    modoDesarrollador: para fines de evaluación.
    return: índice del jugador que inicia.
    """
    global desa, mod
    aux = ListaJugadores[:]
    while (len(aux) != 1):
        for x in aux:
            x.valor = x.lanzarUnDado(desa)
        aux2 = []
        for x in aux:
            if not(x.valor != obtenerMayorValor(aux)):
                aux2.append(x)
        aux = aux2
    if mod < 3:
        print(aux[0].nombre + " es el primero en iniciar")
    else:
        tkinter.messagebox.showinfo("Aviso", aux[0].nombre + " es el primero en iniciar")
    return ListaJugadores.index(aux[0])

def juegoTerminado(Jugadores):
    """
    Verifica si el juego ha terminado.
    Jugadores: lista de objetos 'jugador'.
    True si el juego termina (cuando solo queda un jugador sin ganar), False en otro caso.
    """
    numberWonPlayers = 0  # Cuenta el número de jugadores que ya han ganado
    for jugadorActual in Jugadores:
        if jugadorActual.GanoJugador:
            numberWonPlayers += 1
    if (numberWonPlayers == len(Jugadores) - 1 and len(Jugadores) > 1) or (numberWonPlayers == 1 and len(Jugadores) == 1):
        global POSICION
        jugadorFaltante = [jug for jug in Jugadores if not jug.GanoJugador]
        if not len(jugadorFaltante) == 0:
            jugadorFaltante[0].Posicion = POSICION
        return True
    return False

def movimientosPosibles(JugadorActual, resultadoDado, ListaJugadores):
    """
    Retorna una lista con todos los movimientos posibles para un jugador dado el resultado del dado.
    Analiza la posición actual de cada ficha, posibles bloqueos y si se puede capturar alguna ficha contraria.
    JugadorActual: objeto 'jugador' que mueve.
    resultadoDado: número de casillas a avanzar.
    ListaJugadores: lista de todos los jugadores.
    lista de tuplas con los movimientos posibles.
    """
    listaPosiblesMovimientos = []
    # Se definen las casillas de "cárcel" (inicio de juego) para cada color
    listaCasillasCarcel = [69, 70, 71, 72]
    numeros = {}
    numeros2 = {}
    for jugador in ListaJugadores:
        for ficha in jugador.fichas:
            casillaActual = ficha.espacioActual.numeroEspacio
            if casillaActual in numeros and not casillaActual in listaCasillasCarcel:
                numeros[casillaActual][1] += 1
                if numeros[casillaActual][0].colorFicha != ficha.colorFicha and casillaActual in [5, 22, 39, 56]:
                    numeros2[casillaActual] = [numeros[casillaActual][0], ficha]
            elif not casillaActual in listaCasillasCarcel:
                numeros[casillaActual] = [ficha, 1]

    listaBloqueos = [item for item, valor in numeros.items() if valor[1] == 2]
    listaConUnaFicha = [(item, valor[0]) for item, valor in numeros.items() if valor[1] == 1]
    tuplaCasillasUnaFicha = tuple([valor for valor, ficha in listaConUnaFicha])
    dat = {"rojo": 5, "verde": 22, "amarillo": 39, "azul": 56}
    diccionarioSeguros = {"rojo": 68, "verde": 17, "amarillo": 34, "azul": 51}  # Casillas seguras de inicio para cada color
    diccionarioPrimeraEspecial = {"rojo": 73, "verde": 80, "amarillo": 87, "azul": 94}  # Primera casilla especial

    numeroSeguroSalida = diccionarioSeguros[JugadorActual.color]
    numeroPrimeraEspecial = diccionarioPrimeraEspecial[JugadorActual.color]
    numeroDiccionarioSeguros = diccionarioSeguros[JugadorActual.color]

    colorJugador = JugadorActual.color

    for fichaActual in JugadorActual.fichas:
        bloqueo = False
        casillaFicha = fichaActual.espacioActual.numeroEspacio
        nombreFicha = fichaActual.nombreFicha
        posicionFinal = casillaFicha + resultadoDado
        if casillaFicha in listaCasillasCarcel and resultadoDado != 5:
            continue
        if casillaFicha in listaCasillasCarcel and resultadoDado == 5:
            if not (dat[colorJugador] in listaBloqueos and not dat[colorJugador] in numeros2):
                if (dat[colorJugador] in tuplaCasillasUnaFicha and numeros[dat[colorJugador]][0].colorFicha != fichaActual.colorFicha):
                    return ([(nombreFicha + " sale de la carcel a la casilla: %d. Captura a %s." % (dat[colorJugador], numeros[dat[colorJugador]][0].nombreFicha), fichaActual, numeros[dat[colorJugador]][0])])
                elif dat[colorJugador] in numeros2:
                    if numeros2[dat[colorJugador]][0].colorFicha != fichaActual.colorFicha and numeros2[dat[colorJugador]][1].colorFicha == fichaActual.colorFicha:
                        return ([(nombreFicha + " sale de la carcel a la casilla: %d. Captura a %s." % (dat[colorJugador], numeros2[dat[colorJugador]][0].nombreFicha), fichaActual, numeros2[dat[colorJugador]][0])])
                    elif numeros2[dat[colorJugador]][1].colorFicha != fichaActual.colorFicha and numeros2[dat[colorJugador]][0].colorFicha == fichaActual.colorFicha:
                        return ([(nombreFicha + " sale de la carcel a la casilla: %d. Captura a %s." % (dat[colorJugador], numeros2[dat[colorJugador]][1].nombreFicha), fichaActual, numeros2[dat[colorJugador]][1])])
                    else:
                        continue
                else:
                    return ([(nombreFicha + " sale de la carcel a la casilla: %d." % dat[colorJugador], fichaActual)])
            else:
                continue
        else:
            # Se evalúan los bloqueos en el trayecto hacia la posición final.
            for x in range(casillaFicha + 1, posicionFinal + 1):
                if (casillaFicha <= numeroSeguroSalida and x > numeroSeguroSalida) or (colorJugador == "verde" and casillaFicha >= 51 and casillaFicha <= 68 and x > 85):
                    if (colorJugador == "verde" and casillaFicha >= 51 and casillaFicha <= 68 and x > 85):
                        if x % 68 + (numeroPrimeraEspecial - numeroDiccionarioSeguros) - 1 in listaBloqueos:
                            bloqueo = True
                            break
                        elif x % 68 + (numeroPrimeraEspecial - numeroDiccionarioSeguros) - 1 > numeroPrimeraEspecial + 7:
                            bloqueo = True
                            break
                    else:
                        if x + (numeroPrimeraEspecial - numeroDiccionarioSeguros) - 1 in listaBloqueos:
                            bloqueo = True
                            break
                        elif x + (numeroPrimeraEspecial - numeroDiccionarioSeguros) - 1 > numeroPrimeraEspecial + 7:
                            bloqueo = True
                            break
                elif casillaFicha <= 68 and x <= 68 and x in listaBloqueos:
                    bloqueo = True
                    break
                elif x % 68 in listaBloqueos:
                    bloqueo = True
                    break
                elif x in listaBloqueos or x > numeroPrimeraEspecial + 7:
                    bloqueo = True
                    break

        CasillaEspecial = 0
        ListaCasillasSeguro = (12, 17, 29, 34, 46, 51, 63, 68)
        ListaCasillasSalida = (5, 22, 39, 56)
        if (casillaFicha <= numeroSeguroSalida and posicionFinal > numeroSeguroSalida) or (colorJugador == "verde" and casillaFicha >= 51 and casillaFicha <= 68 and posicionFinal > 85):
            if (colorJugador == "verde" and casillaFicha >= 51 and casillaFicha <= 68 and posicionFinal > 85):
                CasillaEspecial = posicionFinal % 68 + (numeroPrimeraEspecial - numeroSeguroSalida - 1)
            else:
                CasillaEspecial = posicionFinal + (numeroPrimeraEspecial - numeroSeguroSalida - 1)
            if CasillaEspecial == numeroPrimeraEspecial + 7:
                CasillaEspecial = 101

        if not bloqueo:
            if CasillaEspecial == 101 or posicionFinal == numeroPrimeraEspecial + 7:
                textoRespuesta = '{} copa'.format(nombreFicha)
                listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

            elif posicionFinal <= 68 and posicionFinal in tuplaCasillasUnaFicha and CasillaEspecial == 0:
                fichaCapturada = numeros[posicionFinal][0]
                if fichaCapturada.colorFicha != colorJugador and not posicionFinal in ListaCasillasSeguro and not posicionFinal in ListaCasillasSalida:
                    textoRespuesta = '{} captura a {} en casilla {}'.format(nombreFicha, fichaCapturada.nombreFicha, posicionFinal)
                    listaPosiblesMovimientos.append((textoRespuesta, fichaActual, fichaCapturada))
                else:
                    textoRespuesta = '{} mueve a casilla {}'.format(nombreFicha, posicionFinal)
                    listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

            elif posicionFinal > 68 and (posicionFinal % 68 in tuplaCasillasUnaFicha) and CasillaEspecial == 0 and casillaFicha <= 68:
                fichaCapturada_2 = numeros[posicionFinal % 68][0]
                if fichaCapturada_2.colorFicha != colorJugador and not posicionFinal % 68 in ListaCasillasSeguro and not posicionFinal % 68 in ListaCasillasSalida:
                    textoRespuesta = '{} captura a {} en casilla {}'.format(nombreFicha, fichaCapturada_2.nombreFicha, posicionFinal % 68)
                    listaPosiblesMovimientos.append((textoRespuesta, fichaActual, fichaCapturada_2))
                else:
                    textoRespuesta = '{} mueve a casilla {}'.format(nombreFicha, posicionFinal % 68)
                    listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

            elif CasillaEspecial != 0:
                textoRespuesta = '{} mueve a casilla {}'.format(nombreFicha, CasillaEspecial)
                listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

            elif posicionFinal <= 68:
                textoRespuesta = '{} mueve a casilla {}'.format(nombreFicha, posicionFinal)
                listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

            elif posicionFinal > 68 and casillaFicha > 68:
                textoRespuesta = '{} mueve a casilla {}'.format(nombreFicha, posicionFinal)
                listaPosiblesMovimientos.append((textoRespuesta, fichaActual))

            elif posicionFinal > 68:
                textoRespuesta = '{} mueve a casilla {}'.format(nombreFicha, posicionFinal % 68)
                listaPosiblesMovimientos.append((textoRespuesta, fichaActual))
    if len(listaPosiblesMovimientos) == 0:
        return None
    return listaPosiblesMovimientos

def ejecutarMovimiento(movimientoRealizar, tablero, jugadorActual, Jugadores):
    """
    Actualiza las posiciones de las fichas en el tablero según el movimiento seleccionado.
    movimientoRealizar: tupla que contiene:
         1. Descripción del movimiento (cadena de texto).
         2. Objeto ficha a mover.
         3. (Opcional) Objeto ficha capturado (cadena vacía si no hay captura).
    tablero: lista de casillas.
    jugadorActual: jugador que realiza el movimiento.
    Jugadores: lista de todos los jugadores.
    """
    global mod
    if movimientoRealizar == None:
        return
    FichaCapturada = None
    listaCasillasCarcel = {'rojo': 69, 'verde': 70, 'amarillo': 71, 'azul': 72}
    listaCasillasSalida = {'rojo': 5, 'verde': 22, 'amarillo': 39, 'azul': 56}
    FichaMover = movimientoRealizar[1]
    descripcionMovimiento = movimientoRealizar[0]

    if len(movimientoRealizar) == 3:
        FichaCapturada = movimientoRealizar[2]
    if 'sale' in descripcionMovimiento:
        if "Captura" in descripcionMovimiento:
            FichaCapturada = movimientoRealizar[2]
            FichaCapturada.estadoJuego = "inicio"
            casillaCarcel = listaCasillasCarcel[FichaCapturada.colorFicha]
            FichaCapturada.moverFicha(tablero[casillaCarcel - 1])
            FichaMover.moverFicha(tablero[listaCasillasSalida[FichaMover.colorFicha] - 1])
            FichaMover.estadoJuego = "activo"
            listaMovi = movimientosPosibles(jugadorActual, 20, Jugadores)
            if mod > 1:
                tkinter.messagebox.showinfo("Captura", FichaMover.nombreFicha + " captura a " + FichaCapturada.nombreFicha)
                tkinter.messagebox.showinfo("Salida", FichaMover.nombreFicha + " sale de la carcel.")
            if listaMovi and len(listaMovi) == 1:
                ejecutarMovimiento(listaMovi[0], tablero, jugadorActual, Jugadores)
            elif listaMovi and len(listaMovi) > 1:
                ejecutarMovimiento(seleccionarOpcionMovimiento(listaMovi, jugadorActual), tablero, jugadorActual, Jugadores)
        else:
            FichaMover.moverFicha(tablero[listaCasillasSalida[FichaMover.colorFicha] - 1])
            FichaMover.estadoJuego = "activo"
            if mod > 1:
                tkinter.messagebox.showinfo("Salida", FichaMover.nombreFicha + " sale de la carcel.")
    elif 'captura' in descripcionMovimiento:
        posicionFinal = int(descripcionMovimiento.split()[-1])
        casillaCarcel = listaCasillasCarcel[FichaCapturada.colorFicha]
        FichaCapturada.moverFicha(tablero[casillaCarcel - 1])
        FichaCapturada.estadoJuego = "inicio"
        FichaMover.moverFicha(tablero[posicionFinal - 1])
        listaMovi = movimientosPosibles(jugadorActual, 20, Jugadores)
        if mod > 1:
            tkinter.messagebox.showinfo("Captura", FichaMover.nombreFicha + " captura a " + FichaCapturada.nombreFicha)
        if listaMovi and len(listaMovi) == 1:
            ejecutarMovimiento(listaMovi[0], tablero, jugadorActual, Jugadores)
        elif listaMovi and len(listaMovi) > 1:
            ejecutarMovimiento(seleccionarOpcionMovimiento(listaMovi, jugadorActual), tablero, jugadorActual, Jugadores)
    elif 'mueve' in descripcionMovimiento:
        posicionFinal = int(descripcionMovimiento.split()[-1])
        FichaMover.moverFicha(tablero[posicionFinal - 1])
    elif 'copa' in descripcionMovimiento:
        if mod > 1:
            FichaMover.removerFicha()
        jugadorActual.fichas.remove(FichaMover)
        if len(jugadorActual.fichas) == 0:
            global POSICION
            jugadorActual.Posicion = POSICION
            POSICION += 1
            jugadorActual.GanoJugador = True
        if mod > 1:
            tkinter.messagebox.showinfo("copa", FichaMover.nombreFicha + " ganó copa.")
        listaMovi = movimientosPosibles(jugadorActual, 10, Jugadores)
        if listaMovi and len(listaMovi) == 1:
            ejecutarMovimiento(listaMovi[0], tablero, jugadorActual, Jugadores)
        elif listaMovi and len(listaMovi) > 1:
            ejecutarMovimiento(seleccionarOpcionMovimiento(listaMovi, jugadorActual), tablero, jugadorActual, Jugadores)
        return
    jugadorActual.establecerUltimaFicha(jugadorActual, FichaMover)

def mostrarEstado(Jugador):
    """
    Imprime en consola el estado actual de todas las fichas de un jugador.
    Jugador: objeto 'jugador'.
    """
    for ficha in Jugador.fichas:
        print(ficha.mostrarPropiedades())

def seleccionarOpcionMovimiento(Lista, JugadorActual):
    """
    Permite al jugador seleccionar una opción de movimiento de entre una lista de movimientos posibles.
    Lista: lista de tuplas con opciones de movimiento.
    JugadorActual: jugador que debe seleccionar la opción.
    return: la opción de movimiento seleccionada.
    """
    eleccion = 0
    global mod, caja_entrada_dados, boton_entrada_dados, seleccion
    seleccion = False
    if mod == 3:
        clicked = StringVar(Pan)
        caja_entrada_dados.config(state="normal")
        caja_entrada_dados.delete(0, END)
        caja_entrada_dados.insert(0, "%s seleccione una opcion de la lista y oprima continuar." % JugadorActual.nombre)
        caja_entrada_dados.config(state="readonly")
        options = [opcion[0] for opcion in Lista]
        clicked.set("Seleccione una opción")
        drop = OptionMenu(Pan, clicked, clicked.get(), *options)
        drop.place(x=0, y=450, width=700, height=50)
        boton_entrada_dados.config(command=elegirOpcion)
        while not seleccion:
            if clicked.get() == "Seleccione una opción":
                seleccion = False
            pass
        eleccion = options.index(clicked.get()) + 1
        boton_entrada_dados.config(command=capturarEntradaDados)
        drop.destroy()
    if mod < 3:
        while eleccion <= 0 or eleccion > len(Lista):
            x = 1
            for opcion in Lista:
                print(f'{x} -> {opcion[0]}')
                x += 1
            print(f'{x}  ->  Ver estado de Fichas')
            eleccion = input()
            registrarDato(eleccion)
            try:
                eleccion = int(eleccion)
            except:
                eleccion = 0
            if eleccion == len(Lista) + 1:
                mostrarEstado(JugadorActual)
    return Lista[eleccion - 1]

def manejarInteraccionDados(etiqueta, accion):
    """
    Maneja la interacción con los dados en modo gráfico.
    Cambia el color de fondo de la etiqueta del dado para indicar acciones (por ejemplo, selección) y asigna la selección.
    etiqueta: widget de la etiqueta del dado.
    accion: entero que indica la acción (0: mouse entra, 1: mouse sale, 2: dado seleccionado 1, 3: dado seleccionado 2).
    """
    global dadoSeleccionado
    if accion == 0:
        etiqueta.config(bg="red")
    elif accion == 1:
        etiqueta.config(bg="green")
    elif accion == 2:
        dadoSeleccionado = 1
    elif accion == 3:
        dadoSeleccionado = 2

def comenzarJuego():
    """
    Función principal del juego.
    Inicializa los datos, el tablero, los jugadores y controla el ciclo principal de juego.
    """
    global desa, mod
    if mod > 1:
        global LB, BTN
        LB.destroy()
        BTN.destroy()
    nom = tuple(solicitarDatos())  # Obtiene los nombres de los jugadores
    if mod > 1:
        global L_DADOS1, L_DADOS2, L_NOMBRES, L_TABLERO, L_OPCIONES, L_TEXTO, caja_entrada_dados, boton_entrada_dados
        L_DADOS1 = Label(Pan, bg="white", font=("Times New Roman", 20))
        L_DADOS1.place(x=37, y=20, width=175, height=175)
        L_DADOS2 = Label(Pan, bg="white", font=("Times New Roman", 20))
        L_DADOS2.place(x=37, y=210, width=175, height=175)
        L_NOMBRES = Label(Pan, bg="orange", fg="white", text="NOMBRES", font=("Times New Roman", 20))
        L_NOMBRES.place(x=0, y=400, width=250, height=50)
        L_TABLERO = Label(Pan, bg="white", fg="white", font=("Times New Roman", 20))
        L_TABLERO.place(x=250, y=0, width=450, height=450)
    Tablero = DiseñarTablero()  # Se crea el tablero
    Jugadores = GenerarJugadoresYFichas(Tablero, len(nom), nom)  # Se crean los jugadores y sus fichas
    indicePrimerJugador = determinarOrdenDeJuego(Jugadores)
    while not juegoTerminado(Jugadores):
        repetirLanzamiento = True
        contadorParesSeguidos = 0  # Contador para detectar tres pares consecutivos
        jugadorActual = Jugadores[indicePrimerJugador % len(Jugadores)]
        if jugadorActual.GanoJugador:
            continue
        while repetirLanzamiento:
            resultadoDado1, resultadoDado2 = jugadorActual.lanzarDosDados(desa)
            # Si los dos dados muestran el mismo número, se permite lanzar nuevamente,
            # a menos que sea la tercera vez consecutiva (en cuyo caso se penaliza)
            if resultadoDado1 == resultadoDado2:
                repetirLanzamiento = True
                contadorParesSeguidos += 1
                if contadorParesSeguidos == 3:
                    listaCasillasCarcel = {'rojo': 69, 'verde': 70, 'amarillo': 71, 'azul': 72}
                    UltimaFichaJugador = jugadorActual.UltimaFicha  # Se usa la última ficha del jugador
                    nombreFicha = UltimaFichaJugador.nombreFicha
                    posicionFinal = listaCasillasCarcel[UltimaFichaJugador.colorFicha]
                    ejecutarMovimiento(['{} mueve a casilla {}'.format(nombreFicha, posicionFinal), UltimaFichaJugador], Tablero, jugadorActual, Jugadores)
                    UltimaFichaJugador.estadoJuego = 'inicio'
                    repetirLanzamiento = False
                    contadorParesSeguidos = 0
                    mostrarEstado(jugadorActual)
                    continue
            else:
                contadorParesSeguidos = 0
                repetirLanzamiento = False
            if resultadoDado1 + resultadoDado2 == 5:
                ListaMovi = movimientosPosibles(jugadorActual, 5, Jugadores)
                if ListaMovi and len(ListaMovi) == 1 and "sale" in ListaMovi[0][0]:
                    ejecutarMovimiento(ListaMovi[0], Tablero, jugadorActual, Jugadores)
                    continue
            ListaMovi1 = movimientosPosibles(jugadorActual, resultadoDado1, Jugadores)
            ListaMovi2 = movimientosPosibles(jugadorActual, resultadoDado2, Jugadores)
            ListaMoviF = ""
            if ListaMovi1 and 'sale' in ListaMovi1[0][0]:
                ejecutarMovimiento(ListaMovi1[0], Tablero, jugadorActual, Jugadores)
                ListaMovi2 = movimientosPosibles(jugadorActual, resultadoDado2, Jugadores)
                ListaMoviF = ListaMovi2
            elif ListaMovi2 and "sale" in ListaMovi2[0][0]:
                ejecutarMovimiento(ListaMovi2[0], Tablero, jugadorActual, Jugadores)
                ListaMovi1 = movimientosPosibles(jugadorActual, resultadoDado1, Jugadores)
                ListaMoviF = ListaMovi1
            if type(ListaMoviF) != list:
                if ListaMovi1 and ListaMovi2:
                    global dadoSeleccionado
                    dadoSeleccionado = 0
                    if mod < 3:
                        while dadoSeleccionado <= 0 or dadoSeleccionado > 2:
                            print("¿Qué dado desea mover? :\n1. %d\n2. %d" % (resultadoDado1, resultadoDado2))
                            dadoSeleccionado = input()
                            registrarDato(dadoSeleccionado)
                            try:
                                dadoSeleccionado = int(dadoSeleccionado)
                            except:
                                dadoSeleccionado = 0
                    else:
                        caja_entrada_dados.config(state="normal")
                        caja_entrada_dados.delete(0, END)
                        caja_entrada_dados.insert(0, "%s seleccione uno de los dados" % jugadorActual.nombre)
                        caja_entrada_dados.config(state="readonly")
                        L_DADOS1.bind("<Enter>", lambda x: manejarInteraccionDados(L_DADOS1, 0))
                        L_DADOS2.bind("<Enter>", lambda x: manejarInteraccionDados(L_DADOS2, 0))
                        L_DADOS1.bind("<Button-1>", lambda x: manejarInteraccionDados(L_DADOS1, 2))
                        L_DADOS1.bind("<Leave>", lambda x: manejarInteraccionDados(L_DADOS1, 1))
                        L_DADOS2.bind("<Leave>", lambda x: manejarInteraccionDados(L_DADOS2, 1))
                        L_DADOS2.bind("<Button-1>", lambda x: manejarInteraccionDados(L_DADOS2, 3))
                        while dadoSeleccionado == 0:
                            pass
                        L_DADOS1.config(bg="green")
                        L_DADOS2.config(bg="green")
                        L_DADOS1.unbind("<Enter>")
                        L_DADOS2.unbind("<Enter>")
                        L_DADOS1.unbind("<Button-1>")
                        L_DADOS1.unbind("<Leave>")
                        L_DADOS2.unbind("<Leave>")
                        L_DADOS2.unbind("<Button-1>")
                    for x in range(2):
                        if dadoSeleccionado == 1 and not ListaMovi1:
                            continue
                        elif dadoSeleccionado == 2 and not ListaMovi2:
                            continue
                        elif dadoSeleccionado == 1 and len(ListaMovi1) == 1:
                            ejecutarMovimiento(ListaMovi1[0], Tablero, jugadorActual, Jugadores)
                            ListaMovi2 = movimientosPosibles(jugadorActual, resultadoDado2, Jugadores)
                            dadoSeleccionado = 2
                        elif dadoSeleccionado == 1 and len(ListaMovi1) > 1:
                            ejecutarMovimiento(seleccionarOpcionMovimiento(ListaMovi1, jugadorActual), Tablero, jugadorActual, Jugadores)
                            ListaMovi2 = movimientosPosibles(jugadorActual, resultadoDado2, Jugadores)
                            dadoSeleccionado = 2
                        elif dadoSeleccionado == 2 and len(ListaMovi2) == 1:
                            ejecutarMovimiento(ListaMovi2[0], Tablero, jugadorActual, Jugadores)
                            ListaMovi1 = movimientosPosibles(jugadorActual, resultadoDado1, Jugadores)
                            dadoSeleccionado = 1
                        elif dadoSeleccionado == 2 and len(ListaMovi2) > 1:
                            ejecutarMovimiento(seleccionarOpcionMovimiento(ListaMovi2, jugadorActual), Tablero, jugadorActual, Jugadores)
                            ListaMovi1 = movimientosPosibles(jugadorActual, resultadoDado1, Jugadores)
                            dadoSeleccionado = 1
                        mostrarEstado(jugadorActual)
                elif ListaMovi1:
                    if len(ListaMovi1) == 1:
                        ejecutarMovimiento(ListaMovi1[0], Tablero, jugadorActual, Jugadores)
                        mostrarEstado(jugadorActual)
                    else:
                        ejecutarMovimiento(seleccionarOpcionMovimiento(ListaMovi1, jugadorActual), Tablero, jugadorActual, Jugadores)
                        mostrarEstado(jugadorActual)
                elif ListaMovi2:
                    if len(ListaMovi2) == 1:
                        ejecutarMovimiento(ListaMovi2[0], Tablero, jugadorActual, Jugadores)
                    else:
                        ejecutarMovimiento(seleccionarOpcionMovimiento(ListaMovi2, jugadorActual), Tablero, jugadorActual, Jugadores)
            elif ListaMoviF and len(ListaMoviF) == 1:
                ejecutarMovimiento(ListaMoviF[0], Tablero, jugadorActual, Jugadores)
                mostrarEstado(jugadorActual)
            elif ListaMoviF and len(ListaMoviF) > 1:
                ejecutarMovimiento(seleccionarOpcionMovimiento(ListaMoviF, jugadorActual), Tablero, jugadorActual, Jugadores)
                mostrarEstado(jugadorActual)

        indicePrimerJugador += 1  # Avanza al siguiente jugador en forma cíclica
    if mod > 1:
        Pan.quit()
    # Ordena los jugadores según la posición final para determinar el ranking
    Jugadores.sort(key=lambda x: x.Posicion)
    for x in Jugadores:
        print(x.nombre + " terminó en posición: %d" % x.Posicion)

ele = 0
while (ele <= 0 or ele > 3):
    print("Bienvenidos a Nuestro Juego:\nSeleccione una de las siguientes:\n1. Modo Consola\n2. Modo Consola+Gráficos\n3. Modo Gráficos\n")
    ele = input()
    try:
        ele = int(ele)
    except:
        ele = 0
mod = ele
if mod > 1:
    if OS == "Windows":
        threading.Thread(target=iniciarModoGrafico).start()
    else:
        iniciarModoGrafico()
else:
    comenzarJuego()