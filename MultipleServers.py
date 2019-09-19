import sys
import math
from random import random

if len(sys.argv) != 5:
    print("Args: [T EJECUCION s] [T LLEGADAS] [T PROCESAMIENTO] [# SERVIDORES]")
    exit(0)

# calculo de tiempos
nextTime = lambda s: s - (1/int(sys.argv[2]))*math.log10(random())
processTime = lambda s: s - (1/int(sys.argv[3]))*math.log10(random())

# variables para simulacion
T = int(sys.argv[1])
t = 0
n = 0
na = 0
nd = 0
queue = 0
nextOrder = 1
serviceTime = 1
servers = int(sys.argv[4])
serversTimes = [0] * servers
ta = nextTime(0)
td = [math.inf] * servers
a = []
d = []

# variables para calculos
tiempoDesocupado = 0
tiempoEnCola = 0
tiempoDeQueues = 0
a_cola = []
d_cola = []
queue_in_time = []

if servers == 1:
    print("----------------- Gorilla Megacomputing -----------------")
else:
    print("----------------- Ants smart computing -----------------")

while (True):
    if ta <= min(td) and ta <= T:
        t = ta
        na += 1
        ta = nextTime(t)

        if queue == 0:
            queue = 1
            td[0] = t + processTime(nextOrder)

        elif queue <= servers:
            for i in range(servers):
                if serversTimes[i] == 0:
                    queue += 1
                    serversTimes[i] = na
                    td[i] = t + processTime(serviceTime)
                    break
            print(td)
            break


        elif queue > servers:
            a_cola.append(ta)
            queue += 1

        queue_in_time.append(queue)
        a.append(t)

    elif min(td) < ta and min(td) <= T:
        nd += 1
        lowTdIndex = 0
        for i in range(servers):
            if serversTimes[i] >= serversTimes[lowTdIndex]:
                lowTdIndex = i

        t = td[lowTdIndex]
        queue -= 1

        if queue >= servers:
            d_cola.append(t)
            serversTimes[lowTdIndex] = max(serversTimes) + 1
            td[lowTdIndex] = t + processTime(serviceTime)
        else:
            serversTimes[lowTdIndex] = 0
            td[lowTdIndex] = math.inf

        if td == [math.inf] * servers:
            tiempoDesocupado += ta - t

        queue_in_time.append(queue)
        d.append(t)

    elif min(ta, min(td)) > T and queue > 0:
        nd += 1
        lowTdIndex = 0
        for i in range(servers):
             if serversTimes[i] >= serversTimes[lowTdIndex]:
                 lowTdIndex = i

        t = td[lowTdIndex]
        queue -= 1

        if queue >= servers:
            d_cola.append(t)
            serversTimes[lowTdIndex] = max(serversTimes) + 1
            td[lowTdIndex] = t + processTime(serviceTime)
        else:
            serversTimes[lowTdIndex] = 0
            td[lowTdIndex] = math.inf

        queue_in_time.append(queue)
        if t != math.inf:
            d.append(t)

    elif min(ta, min(td)) > T and queue == 0:
        break

# Calculos para reporte
for i in range(len(a_cola)):
    tiempoEnCola += d_cola[i] - a_cola[i]

for i in range(len(queue_in_time)):
    tiempoDeQueues += queue_in_time[i]


print("Cantidad de Solicitudes: " + str(na))
print("Tiempo de Simulacion: " + str(T))
print("Tiempo Ocupado: " + str(T - tiempoDesocupado))
print("Tiempo Desocupado: " + str(tiempoDesocupado))
print("Tiempo Promedio en Cola " + str(tiempoEnCola/len(a_cola)))
print("Cantidad Promedio de Cola " + str(tiempoDeQueues/len(queue_in_time)))
print("Tiempo de Ultima Salida: " + str(d[len(d) - 1]))
