from tkinter.tix import Tree
from graphviz import Digraph
from tkinter import filedialog
import  tkinter as tk
from tkinter import filedialog
import pathlib
import sys
from tkinter import messagebox
from turtle import color, fillcolor, width
import webbrowser
import os
from tkinter import filedialog, Tk
from tkinter import *
from tkinter import ttk

import xml.etree.ElementTree as ET
tree = None
root = None

def leerArchivo(ruta):
    global Contenido,boolCarga
    Contenido = ""
    print('------- Buscando archivo de entrada -------\n')
    try:
        with open(ruta, encoding='utf-8') as file:
            contenido = file.read()
            print("\n----------- Carga completada ----------\n")
            Contenido = contenido
            boolCarga = True
    except:
        print('No se pudo abrir el fichero de la ruta: ' + ruta)
        print("El eror fue : ",sys.exc_info()[0],"\n")
        boolCarga = False
        return False

def cargarArchivo():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    path = pathlib.Path(filename)
    extension = path.suffix
    if True:
        leerArchivo(filename)
    else:
        print("\nEl archivo no es de la extension requerida.")
        return False

# cargarArchivo()

class ciudad():
    def __init__(self,nombre,filas,columnas) -> None:
        self.nombre = nombre
        self.filas = filas
        self.columnas = columnas
        self.matriz = MatrizOrtogonal()

class lista():
    def __init__(self):
        self.size = 0
        self.cabecera = None
    
    def agregar(self,nodo):
        if self.cabecera == None:
            self.cabecera = nodo
            self.size += 1
        else:
            tmp = self.cabecera
            while tmp.siguiente != None:
                tmp = tmp.siguiente 
            tmp.siguiente = nodo
            self.size += 1

    def ordenar(self):
            if self.size > 1:
                while True:
                    actual = self.cabecera
                    i = None  #Esta es anterior
                    j = self.cabecera.siguiente 
                    cambio = False
                    while j != None:
                        if actual.acumulado > j.acumulado:
                            cambio = True
                            if i != None:
                                tmp = j.siguiente
                                i.siguiente = j
                                j.siguiente = actual
                                actual.siguiente = tmp
                            else:
                                tmp2 = j.siguiente
                                self.cabecera = j
                                j.siguiente = actual
                                actual.siguiente = tmp2
                            i = j
                            j = actual.siguiente
                        else:
                            i = actual
                            actual = j
                            j = j.siguiente
                    if not cambio:
                        break


class celda():
    def __init__(self,simbolo):
        self.tipo = None
        if simbolo == "*":
            self.simbolo = "intransitable"
        elif simbolo == " ":
            self.simbolo = "trasitable"
        elif simbolo == "E":
            self.simbolo = "entrada"
        elif simbolo == "C":
            self.simbolo = "civil"
        elif simbolo == "R":
            self.simbolo = "recurso"
        else:
            self.simbolo = None
        self.pV = None
        self.pH = None

class unidadMilitar():
    def __init__(self,fila,columna,capacidad):
        self.fila = fila
        self.columna = columna
        self.capacidad = capacidad

class orden():
    def __init__(self,posH,posV,consumo):
        self.posH = posH
        self.posV = posV
        self.consumo = consumo
        self.acumulado = float('inf')
        self.siguiente = None
        self.anterior = None

class Nodo:
    def __init__(self):
        self.dato = None
        self.posVertical = None
        self.posHorizontal =None
        self.derecha = None
        self.izquierda = None
        self.arriba = None
        self.abajo = None
        #datos adicionales.
        self.siguiente = None
        self.anterior = None
        #datos Dijkstra
        self.visitado = False
        self.padre  = None
        self.vecino_arriba = None
        self.vecino_abajo = None
        self.vecino_derecho = None
        self.vecino_izquierdo = None
        self.Inicial = False
        self.Final = False
        self.pintar = False
        self.acumulado = float('inf')
        self.consumo = 1
        self.fue = False
        self.ir = None
        self.llego = False

class MatrizOrtogonal:
    def __init__(self):
        self.raiz = Nodo()
        self.raiz.posVertical = 1
        self.raiz.posHorizontal = 1
        self.civiles = lista()
        self.entradas = lista()

    def crearIndiceVertical(self, pos):

        tmp = self.raiz
        while tmp != None:

            if tmp.abajo == None and tmp.posVertical < pos:

                nuevo = Nodo()
                nuevo.posHorizontal = 1
                nuevo.posVertical = pos
                nuevo.arriba = tmp
                tmp.abajo = nuevo
                return tmp.abajo
            
            if tmp.posVertical == pos :
                return tmp

            if tmp.posVertical < pos and tmp.abajo.posVertical > pos:
                nuevo = Nodo()
                nuevo.posHorizontal = 1
                nuevo.posVertical = pos

                nuevo.abajo = tmp.abajo
                nuevo.arriba = tmp
                
                tmp.abajo.arriba = nuevo 
                tmp.abajo = nuevo 
                return tmp.abajo


            tmp = tmp.abajo

    def crearIndiceHorizontal(self, pos):
        tmp = self.raiz
        while tmp != None:

            if tmp.derecha == None and tmp.posHorizontal < pos:
                nuevo = Nodo()
                nuevo.posHorizontal = pos
                nuevo.posVertical = 1
                nuevo.izquierda = tmp
                tmp.derecha = nuevo
                return tmp.derecha
            

            if tmp.posHorizontal == pos :
                return tmp

            if tmp.posHorizontal < pos and tmp.derecha.posHorizontal > pos:
                nuevo = Nodo()
                nuevo.posHorizontal = pos
                nuevo.posVertical = 1
                nuevo.derecha = tmp.derecha
                nuevo.izquierda = tmp
                
                tmp.derecha.izquierda = nuevo 
                tmp.derecha = nuevo 
                return tmp.derecha
                
            tmp = tmp.derecha

    def insertarVertical(self, nodo, indiceHorizontal):
        tmp = indiceHorizontal
        while tmp != None:
            if tmp.abajo == None and tmp.posVertical < nodo.posVertical:
                nodo.arriba = tmp
                tmp.abajo = nodo
                return tmp.abajo
            
            if tmp.posVertical == nodo.posVertical :
                tmp.dato = nodo.dato
                return tmp

            if tmp.posVertical < nodo.posVertical and tmp.abajo.posVertical > nodo.posVertical:
                nodo.abajo = tmp.abajo
                nodo.arriba = tmp
                
                tmp.abajo.arriba = nodo 
                tmp.abajo = nodo 
                return tmp.abajo

            tmp = tmp.abajo

    def insertarHorizontal(self, nodo, indiceVertical):
        tmp = indiceVertical
        while tmp != None:
            if tmp.derecha == None and tmp.posHorizontal < nodo.posHorizontal:

                nodo.izquierda  = tmp
                tmp.derecha = nodo
                return tmp.derecha
            
            if tmp.posHorizontal == nodo.posHorizontal :
                tmp.dato = nodo.dato
                return tmp

            if tmp.posHorizontal < nodo.posHorizontal and tmp.derecha.posHorizontal > nodo.posHorizontal:
                nodo.derecho = tmp.derecha
                nodo.izquierda = tmp
                
                tmp.derecha.izquierda = nodo 
                tmp.derecha = nodo 
                return tmp.derecha
                
            tmp = tmp.derecha

    def insertarDato(self,dato,  posVertical, posHorizontal):
        indiceVertical = self.crearIndiceVertical(posVertical)
        indiceHorizontal = self.crearIndiceHorizontal(posHorizontal)

        # crear el nodo valor
        nuevo = Nodo()
        nuevo.posHorizontal = posHorizontal
        nuevo.posVertical = posVertical
        nuevo.dato = dato
        nuevo = self.insertarVertical(nuevo, indiceHorizontal) 
        nuevo = self.insertarHorizontal(nuevo, indiceVertical)
        pass
    
    def recorrerMatriz(self):
        print("Graficando terreno...")
        
        dot = Digraph('G', filename='dot', engine='dot',format='svg')
        dot.node_attr.update(shape="box")
        dot.attr(rankdir = "TB")
        contSubgrap = 1
        
        tmpV = self.raiz

        while tmpV != None:
            tmpH = tmpV
       
            c = Digraph('child'+str(contSubgrap))
            c.attr(rank='same')
            contSubgrap += 1


            while tmpH != None:
                self.graficarNodos(c, tmpH)
                tmpH = tmpH.derecha
            dot.subgraph(c)
            tmpV = tmpV.abajo

        tmpV = self.raiz
        while tmpV != None:
            tmpH = tmpV
            while tmpH != None:
                self.graficarFlechas(dot, tmpH)
                tmpH = tmpH.derecha

            tmpV = tmpV.abajo
        dot.view()
        pass

    def graficarNodos(self, grafo, nodoE):
        nodo = nodoE
        id = str(nodo.posVertical)+"_"+str(nodo.posHorizontal)
        if nodo.dato is not None:
            if isinstance(nodo.dato,celda):
                if nodo.dato.simbolo == "intransitable":
                    grafo.node(id, "",group=str(nodo.posHorizontal),style="filled",fillcolor="black")
                if nodo.dato.simbolo == "trasitable":
                    if nodo.pintar:
                        grafo.node(id, "",group=str(nodo.posHorizontal),style="filled",fillcolor="yellow")
                    else:
                        grafo.node(id, "",group=str(nodo.posHorizontal),style="filled",fillcolor="white")
                if nodo.dato.simbolo == "entrada":
                    grafo.node(id, "",group=str(nodo.posHorizontal),style="filled",fillcolor="green")
                if nodo.dato.simbolo == "civil":
                    grafo.node(id, "",group=str(nodo.posHorizontal),style="filled",fillcolor="blue")
                if nodo.dato.simbolo == "recurso":
                    grafo.node(id, "",group=str(nodo.posHorizontal),style="filled",fillcolor="gray")
                else:
                    grafo.node(id, "",group=str(nodo.posHorizontal))
            else:
                grafo.node(id, "",group=str(nodo.posHorizontal),style="filled",fillcolor="red")
        else:
            grafo.node(id, nodo.dato,group=str(nodo.posHorizontal))

    def graficarFlechas(self, grafo, nodoE):
        nodo = nodoE
        id = str(nodo.posVertical)+"_"+str(nodo.posHorizontal)
        if nodo is not None:
            if nodo.posVertical != 1 and nodo.posHorizontal != 1:
                idV1 = nodo.arriba.posVertical
                idV2 = nodo.arriba.posHorizontal
                idV = str(idV1)+"_"+str(idV2)
                grafo.edge(idV, id,style = "invisible",dir = "none")
                grafo.edge(id, idV,style = "invisible",dir = "none")
                idH1 = nodo.izquierda.posVertical
                idH2 = nodo.izquierda.posHorizontal
                idH = str(idH1)+"_"+str(idH2)
                grafo.edge(idH,id,style = "invisible",dir = "none")
                grafo.edge(id,idH,style = "invisible",dir = "none")
            elif nodo.posVertical == 1 and nodo.posHorizontal != 1:

                idAnterior = str(nodo.izquierda.posVertical)+"_"+str(nodo.izquierda.posHorizontal)
                grafo.edge(idAnterior, id,style = "invisible",dir = "none")   
            elif nodo.posHorizontal == 1 and nodo.posVertical != 1:
                idAnterior = str(nodo.arriba.posVertical)+"_"+str(nodo.arriba.posHorizontal)
                grafo.edge(idAnterior, id,style = "invisible",dir = "none")
            pass

    def recorrerM(self):
        tmpV = self.raiz
        while tmpV is not None:
            tmpH = tmpV
            while tmpH is not None:
                if tmpH.dato is not None and isinstance(tmpH.dato,celda):
                    if tmpH.dato.simbolo == "civil":
                        nuevo = Nodo()
                        nuevo.dato = tmpH.dato
                        self.civiles.agregar(nuevo)
                    elif tmpH.dato.simbolo == "entrada":
                        nuevo = Nodo()
                        nuevo.dato = tmpH.dato
                        self.entradas.agregar(nuevo)
                tmpH = tmpH.derecha
            tmpV = tmpV.abajo

    def reiniciarValores(self):
        tmpV = self.raiz
        while tmpV is not None:
            tmpH = tmpV
            while tmpH is not None:
                tmpH.acumulado = 0
                tmpH.padre = None
                tmpH.visitado = False
                tmpH = tmpH.derecha
            tmpV = tmpV.abajo

    def algoritmo_total(self,posV,posH,FinV,FinH):
        self.vecinos()
        inicio = self.buscarNodo(posV,posH)
        if inicio is not None:
            inicio.Inicial = True
    
            inicio.acumulado = 0
            print("Calculando la mejor ruta...")
            vecinos = (self.lVecinos(inicio))
            vecinos.ordenar()
            tmp = vecinos.cabecera
            if tmp is not None:
                for i in range (vecinos.size):
                    var = tmp.consumo + inicio.consumo
                    if var < tmp.acumulado:
                        tmp.acumulado = var
                        x = self.buscarNodo(tmp.posV,tmp.posH)
                        if x is not None:
                            x.acumulado = var
                            x.padre = inicio
                    tmp = tmp.siguiente
                inicio.visitado = True
                self.analizarNovisitados(vecinos)
                print("Ya casi...")
                fin = self.buscarNodo(FinV,FinH)
                if fin is not None:
                    fin.Final = True
                    return self.imprimirCamino(inicio,fin)
        return False

    def imprimirCamino(self,inicio,fin):
        # try:
            return self.verCamino(inicio,fin)

    def verCamino(self,inicio,fin):
        inicio.pintar = True
        if fin is not None:
            while fin.padre is not None:
                auxiliar = fin
                fin.pintar = True
                fin.llego = True
                idSup = fin
                fin = self.buscarNodo(fin.padre.posVertical,fin.padre.posHorizontal)
                fin.ir = idSup
                if fin.padre is None or auxiliar == fin:
                    break
            if fin == inicio:
                fin.llego = True
                return True
            else:
                return False

            
        else:
            print("")

    def vecinos(self):
        tmpV = self.raiz
        while tmpV is not None:
            tmpH = tmpV
            while tmpH is not None:

                tmpH.vecino_arriba = self.buscarNodo(tmpH.posVertical + 1,tmpH.posHorizontal)
                tmpH.vecino_abajo = self.buscarNodo(tmpH.posVertical - 1,tmpH.posHorizontal)
                tmpH.vecino_derecho = self.buscarNodo(tmpH.posVertical,tmpH.posHorizontal + 1)
                tmpH.vecino_izquierdo = self.buscarNodo(tmpH.posVertical,tmpH.posHorizontal - 1)
                tmpH = tmpH.derecha
            tmpV = tmpV.abajo

    def buscarNodo(self,posV,posH):
        tmpV = self.raiz
        while tmpV is not None:
            tmpH = tmpV
            while tmpH is not None:
                if tmpH.posVertical == posV and tmpH.posHorizontal == posH:
                    if isinstance(tmpH.dato,celda):
                        if tmpH.dato.simbolo == "trasitable" or tmpH.dato.simbolo == "entrada" or tmpH.dato.simbolo == "civil" or tmpH.dato.simbolo == "recurso":
                            return tmpH
                tmpH = tmpH.derecha
            tmpV = tmpV.abajo
        return None

    def lVecinos(self,nodo):
        vecinos = lista()
        if nodo.arriba is not None and nodo.arriba.visitado is False and isinstance(nodo.arriba.dato,unidadMilitar) is False:
            if nodo.arriba.dato.simbolo != "intransitable":
                nuevo = orden(nodo.arriba.posHorizontal,nodo.arriba.posVertical, nodo.arriba.consumo)
                nuevo.acumulado = (nodo.arriba.acumulado)
                vecinos.agregar(nuevo)
        if nodo.abajo is not None and nodo.abajo.visitado is False and isinstance(nodo.abajo.dato,unidadMilitar) is False:
            if nodo.abajo.dato.simbolo != "intransitable":
                nuevo = orden(nodo.abajo.posHorizontal,nodo.abajo.posVertical, nodo.abajo.consumo)
                nuevo.acumulado = (nodo.abajo.acumulado)
                vecinos.agregar(nuevo)
        if nodo.derecha is not None and nodo.derecha.visitado is False and isinstance(nodo.derecha.dato,unidadMilitar) is False:
            if nodo.derecha.dato.simbolo != "intransitable":
                nuevo = orden(nodo.derecha.posHorizontal,nodo.derecha.posVertical,nodo.derecha.consumo)
                nuevo.acumulado = (nodo.derecha.acumulado)
                vecinos.agregar(nuevo)
        if nodo.izquierda is not None and nodo.izquierda.visitado is False and isinstance(nodo.izquierda.dato,unidadMilitar) is False:
            if nodo.izquierda.dato.simbolo != "intransitable":
                nuevo = orden(nodo.izquierda.posHorizontal,nodo.izquierda.posVertical, nodo.izquierda.consumo)
                nuevo.acumulado = (nodo.izquierda.acumulado)
                vecinos.agregar(nuevo)
        vecinos.ordenar()
        return vecinos

    def analizarNovisitados(self,vecinos):
        if vecinos.cabecera is not None:
            vecinos.ordenar()
            tmp = vecinos.cabecera
            for i in range(vecinos.size):
                if tmp is not None:
                    nodoPrincipal = self.buscarNodo(tmp.posV,tmp.posH)
                    if nodoPrincipal is not None:

                        nodoPrincipal.fue = True
                        vecinosNodoPrincipal = (self.lVecinos(nodoPrincipal))
                        temporal = vecinosNodoPrincipal.cabecera
                        if temporal is not None:
                            for i in range(vecinosNodoPrincipal.size):
                                pivote = self.buscarNodo(temporal.posV,temporal.posH)
                                var = 0
                                if pivote is not None:
                                    temporal.acumulado = pivote.acumulado
                                    var = nodoPrincipal.acumulado + temporal.consumo
                                    if var < temporal.acumulado:
                                        temporal.acumulado = var
                                        x = self.buscarNodo(temporal.posV,temporal.posH)
                                        if x is not None:
                                            x.acumulado = var
                                            x.padre = self.buscarNodo(tmp.posV,tmp.posH)
                                        
                                temporal = temporal.siguiente
                            nodoPrincipal.visitado = True
                            vecinosNodoPrincipal.ordenar()
                            self.analizarNovisitados(vecinosNodoPrincipal)

                        else:
                            nodoPrincipal.visitado = True
                tmp = tmp.siguiente

class robot():
    def __init__(self,nombre,tipo):
        self.nombre = nombre
        self.tipo = tipo 
        self.capacidad = None

l_ciudades = lista()
l_robots_rescate = lista()
l_robots_pelea = lista()

def lecturaXML():
    global tree, root,l_ciudades
    root = tk.Tk()
    root.withdraw()
    ruta = filedialog.askopenfilename()
    tree = ET.parse(ruta)
    root = tree.getroot()
    listaCiudades = root[0]
    for i in range(len(listaCiudades)):
        ciudad_ = listaCiudades[i]
        nombre = ciudad_[0].text
        filas = int(ciudad_[0].attrib.get('filas'))
        columnas = int(ciudad_[0].attrib.get('columnas'))
        ciudad_temporal = ciudad(nombre,filas,columnas)
        for j in range(filas):
            pos_Vertical = int(ciudad_[j+1].attrib.get('numero'))
            contenido = ciudad_[j+1].text
            contenido = contenido.replace("\"","")
            contador = 1
            for elemento in contenido:
                celdatmp = celda(elemento)
                celdatmp.pV = pos_Vertical
                celdatmp.pH = contador
                ciudad_temporal.matriz.insertarDato(celdatmp,pos_Vertical,contador)
                contador += 1
        indice = filas+1
        while indice < len(ciudad_):
            capacidad = int(ciudad_[indice].text)
            fila = int(ciudad_[indice].attrib.get("fila"))
            columna = int(ciudad_[indice].attrib.get("columna"))
            unidadTemporal = unidadMilitar(fila,columna,capacidad)
            ciudad_temporal.matriz.insertarDato(unidadTemporal,fila,columna)
            indice += 1
        nodoTemporal = Nodo()
        nodoTemporal.dato = ciudad_temporal
        l_ciudades.agregar(nodoTemporal)
    listaRobots = root[1]
    for i in range(len(listaRobots)):
        robot_ = listaRobots[i]
        nombre = robot_[0].text
        tipo = robot_[0].attrib.get('tipo') 
        if tipo == "ChapinFighter":
            capacidad = int(robot_[0].attrib.get('capacidad'))
            r_temporal = robot(nombre,tipo)
            r_temporal.capacidad = capacidad
            nodoTMP = Nodo()
            nodoTMP.dato = r_temporal
            l_robots_pelea.agregar(nodoTMP)
            # print("ROBOT AGREGADO")
        else:
            r_temporal = robot(nombre,tipo)
            nodoTMP = Nodo()
            nodoTMP.dato = r_temporal
            l_robots_rescate.agregar(nodoTMP)


def rescate():
    print("\nDigite el numero de la ciudad")
    contador = 0
    nodo_tmp = l_ciudades.cabecera
    while nodo_tmp is not None:
        contador += 1
        print(f"{contador}.{nodo_tmp.dato.nombre}")

        nodo_tmp.dato.matriz.civiles = lista()
        nodo_tmp.dato.matriz.entradas = lista()
        nodo_tmp = nodo_tmp.siguiente
    repuesta = input(">")
    c_tmp = None
    if int(repuesta) <= contador:
        contador = 0
        nodo_tmp = l_ciudades.cabecera
        while nodo_tmp is not None:
            contador += 1
            if contador == int(repuesta):
                c_tmp = nodo_tmp
                break
            nodo_tmp = nodo_tmp.siguiente
        if c_tmp is not None:
            robotUtilizado = None
            print(f"\nEl nombre de la ciudad selecciona es {c_tmp.dato.nombre}")
            c_tmp.dato.matriz.recorrerM()

            if l_robots_rescate.size >1:
                print("\nDigite el numero del robot que quiere utilizar:\n")
                tmp = l_robots_rescate.cabecera
                cont = 0
                while tmp is not None:
                    cont += 1
                    robot_ = tmp.dato
                    print(f"{cont}. {robot_.nombre}")
                    tmp = tmp.siguiente
                repuesta = input(">")
                if int(repuesta) <= cont:
                    cont = 0
                    nodo_tmp = l_robots_rescate.cabecera
                    while nodo_tmp is not None:
                        cont += 1
                        if cont == int(repuesta):
                            robotUtilizado = nodo_tmp.dato
                            break
                        nodo_tmp = nodo_tmp.siguiente
            else:
                robotUtilizado = l_robots_rescate.cabecera.dato

            if robotUtilizado is not None:
                if c_tmp.dato.matriz.civiles.size == 1 :
                    civil = c_tmp.dato.matriz.civiles.cabecera
                    if civil is not None:
                            metaV = civil.dato.pV
                            metaH = civil.dato.pH
                            entradaTmp = c_tmp.dato.matriz.entradas.cabecera
                            while entradaTmp is not None:
                                entrada = entradaTmp.dato
                                entV = entrada.pV
                                entH = entrada.pH
                                if c_tmp.dato.matriz.algoritmo_total(entV,entH,metaV,metaH):
                                    print("\n==================MISION==================\n")
                                    print("Tipo de mision: RESCATE")
                                    print("Unidad civil rescatada:",metaV,metaH)
                                    print("Robot utilizado:",robotUtilizado.nombre,"\n")
                                    print("================================================")
                                    c_tmp.dato.matriz.recorrerMatriz()
                                    return
                                c_tmp.dato.matriz.reiniciarValores()
                                entradaTmp = entradaTmp.siguiente
                            print("\nNo se puede rescatar al civil solicitado\n")
                            c_tmp.dato.matriz.recorrerMatriz()

                elif c_tmp.dato.matriz.civiles.size > 1 :
                    print("\nSi existen civiles a los cuales rescatar")
                    tmp = c_tmp.dato.matriz.civiles.cabecera
                    cont = 0 
                    print("\nDigite el numero del civil que quiere rescatar:\n")
                    while tmp is not None:
                        cont += 1
                        civil = tmp.dato
                        print(f"{cont}. posV = {civil.pV} y en posH = {civil.pH}")
                        tmp = tmp.siguiente
                    repuesta = input(">")
                    civil = None
                    if int(repuesta) <= cont:
                        cont = 0
                        nodo_tmp = c_tmp.dato.matriz.civiles.cabecera
                        while nodo_tmp is not None:
                            cont += 1
                            if cont == int(repuesta):
                                civil = nodo_tmp
                                break
                            nodo_tmp = nodo_tmp.siguiente


                        # verificar si el civil fue encontrado
                        if civil is not None:
                            metaV = civil.dato.pV
                            metaH = civil.dato.pH
                            entradaTmp = c_tmp.dato.matriz.entradas.cabecera
                            while entradaTmp is not None:
                                entrada = entradaTmp.dato
                                entV = entrada.pV
                                entH = entrada.pH
                                if c_tmp.dato.matriz.algoritmo_total(entV,entH,metaV,metaH):
                                    print("\n==================MISION==================\n")
                                    print("Tipo de mision: RESCATE")
                                    print("Unidad civil rescatada:",metaV,metaH)
                                    print("Robot utilizado:",robotUtilizado.nombre,"\n")
                                    print("================================================")
                                    c_tmp.dato.matriz.recorrerMatriz()
                                    return
                                c_tmp.dato.matriz.reiniciarValores()
                                entradaTmp = entradaTmp.siguiente
                            print("\nNo se puede rescatar al civil solicitado\n")
                            c_tmp.dato.matriz.recorrerMatriz()
                else:
                    print("No existen civiles a los cuales rescatar")
            else:
                print("\nOpcion no valida\n")
            


        else:
            print(f"No se encontro la ciudad")
    else:
        print("Respuesta no valida")
        rescate()

def menu():
    print("\n\nSELECCIONE EL TIPO DE MISION")
    print("1.Rescate")
    print("2.Extraccion")
    print("3.Terminar ejecucion")
    resp = input(">")
    print(resp)
    if resp == "1":
        try:
            rescate()
            menu()
        except:
            print("Error")
            menu()
    elif resp == "2":
        pass
    elif resp == "3":
        exit(0)
    else:
        print("Opcion incorrecta\n")
        menu()

if __name__ == '__main__':
    lecturaXML()
    print("\nArchivo cargado exitosamente!\n")
    menu()



