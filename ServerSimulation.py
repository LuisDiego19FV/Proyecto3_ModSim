# ServerSimulation.py
import sys
import math
from random import random

# se revisan que esten todos los argumentos
if len(sys.argv) != 5:
    print("Args: [T EJECUCION s] [T LLEGADAS] [T PROCESAMIENTO] [# SERVIDORES]")
    exit(0)

# funcion calculo de tiempo de siguiente entrada
nextTime = lambda s: s - (1/int(sys.argv[2]))*math.log10(random())

# funcion calculo de tiempo de siguiente salida
processTime = lambda s: s - (1/int(sys.argv[3]))*math.log10(random())

T = int(sys.argv[1])            # tiempo total de simulacion
servers = int(sys.argv[4])      # numero de servidores
t = 0                           # tiempo actual de simulacion
n = 0                           # cola
na = 0                          # numero de entradas
nd = 0                          # numero de salidas
nq = 0                          # numero de procesos que estuvieron en cola
ta = nextTime(0)                # siguiente entrada
td = [math.inf] * servers       # siguiente salida por servidor

a = []                          # tiempos de entradas
d = []                          # tiempos de salidas
s = [0] * servers               # numero de request en proceso por servidor

# variables para estadisticas
tiempoDesocupado = 0
tiempoEnCola = 0
tiempoEnColaTa = 0

# nombre del servidor
if servers == 1:
    print("----------------- Gorilla Megacomputing -----------------")
else:
    print("----------------- Ants smart computing -----------------")

# ciclo principal
while (True):

    # llegada antes que salida
    if ta <= min(td) and ta <= T:
        t = ta
        na += 1
        n += 1
        ta = nextTime(t)

        # se ingresa request si hay un server vacio
        if n <= servers:
            for i in range(servers):
                if s[i] == 0:
                    td[i] = processTime(t)
                    s[i] = na
                    break

        a.append(t)

        #calculo de colas
        if n > servers and tiempoEnColaTa == 0:
            tiempoEnColaTa = t
        if n > servers:
            nq += 1

    # salida antes que entrada
    elif min(td) < ta and min(td) <= T:
        iServer = s.index(min(i for i in s if i > 0))
        t = td[iServer]
        n -= 1
        nd += 1

        # se ingresa request a servidor si esta en cola
        if n >= servers:
            td[iServer] = processTime(t)
            s[iServer] = max(s) + 1

        # caso si no hay requests en cola
        elif n < servers:
            td[iServer] = math.inf
            s[iServer] = 0

            # se usa para calcular tiempo desocupado
            if n == 0:
                tiempoDesocupado += ta - t

        d.append(t)

        #calculo de colas
        if n <= servers and tiempoEnColaTa != 0:
            tiempoEnCola += t - tiempoEnColaTa
            tiempoEnColaTa = 0

    # tiempo acabado, con procesos por terminar
    elif min(ta, min(td)) > T and n > 0:
        iServer = s.index(min(i for i in s if i > 0))
        t = td[iServer]
        n -= 1
        nd += 1

        # se ingresa request a servidor si esta en cola
        if n >= servers:
            td[iServer] = processTime(t)
            s[iServer] = max(s) + 1

        # se usa para calcular tiempo desocupado
        elif n < servers:
            td[iServer] = math.inf
            s[iServer] = 0

        d.append(t)

        #calculo de Cola
        if n <= servers and tiempoEnColaTa != 0:
            tiempoEnCola += t - tiempoEnColaTa
            tiempoEnColaTa = 0

    # tiempo acabado
    elif min(ta, min(td)) > T and n == 0:
        break;

# estadisticas
print("Cantidad de Solicitudes: " + str(na))
print("Tiempo de Simulacion: " + str(T))
print("Tiempo Ocupado: " + str(d[len(d)-1] - tiempoDesocupado))
print("Tiempo Desocupado: " + str(tiempoDesocupado))
print("Tiempo en Cola: " + str(tiempoEnCola))
print("Tiempo Promedio en Cola: " + str(tiempoEnCola/na))
print("Promedio de Request en Cola por Segundo: " + str(nq/d[len(d)-1]))
print("Tiempo de Ultima Salida: " + str(d[len(d)-1]))
