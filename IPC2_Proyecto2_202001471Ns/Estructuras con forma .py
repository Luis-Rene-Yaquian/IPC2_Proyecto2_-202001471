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


        nuevo = Nodo()
        nuevo.posHorizontal = posHorizontal
        nuevo.posVertical = posVertical
        nuevo.dato = dato


        nuevo = self.insertarVertical(nuevo, indiceHorizontal) 
        nuevo = self.insertarHorizontal(nuevo, indiceVertical)
        print("Nodo insertado...")
        pass
    
    def recorrerMatriz(self):
        print("Graficando lista...")
        
        dot = Digraph('G', filename='dot', engine='dot',format='svg')
        dot.node_attr.update(shape="box")
        dot.attr(rankdir = "TB")
        contSubgrap = 1
        
        #iniciamos en el nodo raiz
        tmpV = self.raiz

        #vamos bajando en vertical
        while tmpV != None:
            tmpH = tmpV

            #creamos subgrafos para alinearlos            
            c = Digraph('child'+str(contSubgrap))
            c.attr(rank='same')
            contSubgrap += 1

            #nos vamos a la derecha 
            while tmpH != None:
                self.graficarNodos(c, tmpH)
                tmpH = tmpH.derecha

            #se termino una fila, agregamos el subgrafo
            dot.subgraph(c)
            tmpV = tmpV.abajo

        #vuelvo a recorrer para mostrar las flechas
        tmpV = self.raiz
        #vamos bajando en vertical
        while tmpV != None:
            tmpH = tmpV

            #nos vamos a la derecha 
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
        if nodo.posVertical != 0 and nodo.posHorizontal != 0:
            #Graficamos la flecha vertical
            idV1 = nodo.arriba.posVertical
            idV2 = nodo.arriba.posHorizontal
            idV = str(idV1)+"_"+str(idV2)
            grafo.edge(idV, id,style = "invisible",dir = "none")
            grafo.edge(id, idV,style = "invisible",dir = "none")

            #Ahora graficamos la flecha horizontal
            idH1 = nodo.izquierda.posVertical
            idH2 = nodo.izquierda.posHorizontal
            idH = str(idH1)+"_"+str(idH2)
            grafo.edge(idH,id,style = "invisible",dir = "none")
            grafo.edge(id,idH,style = "invisible",dir = "none")
        elif nodo.posVertical == 0 and nodo.posHorizontal != 0:
            #es una cabecera horizontal
            idAnterior = str(nodo.izquierda.posVertical)+"_"+str(nodo.izquierda.posHorizontal)
            grafo.edge(idAnterior, id,style = "invisible",dir = "none")   
        elif nodo.posHorizontal == 0 and nodo.posVertical != 0:
            #es una cabecera vertical
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
                        # agregar a la lista de civiles de la matriz
                        nuevo = Nodo()
                        nuevo.dato = tmpH.dato
                        self.civiles.agregar(nuevo)
                    elif tmpH.dato.simbolo == "entrada":
                        # agregar a la lista de entradas de la matriz
                        nuevo = Nodo()
                        nuevo.dato = tmpH.dato
                        self.entradas.agregar(nuevo)
                tmpH = tmpH.derecha
            tmpV = tmpV.abajo

class robot():
    def __init__(self,nombre,tipo):
        self.nombre = nombre
        self.tipo = tipo 
        self.capacidad = None

l_ciudades = lista()
l_robots = lista()

def lecturaXML():
    global tree, root,l_ciudades
    root = tk.Tk()
    root.withdraw()
    ruta = filedialog.askopenfilename()
    tree = ET.parse(ruta)
    root = tree.getroot()
    #posicioon cero jala la lista de ciudades.
    listaCiudades = root[0]
    for i in range(len(listaCiudades)):
        #ciudad representa la nueva matriz.
        ciudad_ = listaCiudades[i]
        nombre = ciudad_[0].text
        filas = int(ciudad_[0].attrib.get('filas'))
        columnas = int(ciudad_[0].attrib.get('columnas'))
        ciudad_temporal = ciudad(nombre,filas,columnas)
        for j in range(filas):
            pos_Vertical = int(ciudad_[j+1].attrib.get('numero'))
            print(pos_Vertical)
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
            print(ciudad_[indice].text)
            capacidad = int(ciudad_[indice].text)
            fila = int(ciudad_[indice].attrib.get("fila"))
            columna = int(ciudad_[indice].attrib.get("columna"))
            #fila,columna,capacidad
            unidadTemporal = unidadMilitar(fila,columna,capacidad)
            print(fila,columna)
            ciudad_temporal.matriz.insertarDato(unidadTemporal,fila,columna)
            indice += 1
        nodoTemporal = Nodo()
        nodoTemporal.dato = ciudad_temporal
        l_ciudades.agregar(nodoTemporal)
    listaRobots = root[1]
    print(len(listaRobots),"LONGITUD")
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
            l_robots.agregar(nodoTMP)
            print("ROBOT AGREGADO")
        else:
            r_temporal = robot(nombre,tipo)
            nodoTMP = Nodo()
            nodoTMP.dato = r_temporal
            l_robots.agregar(nodoTMP)
            print("ROBOT AGREGADO")

def rescate():
    print("\nDigite el numero de la ciudad")
    contador = 0
    nodo_tmp = l_ciudades.cabecera
    while nodo_tmp is not None:
        contador += 1
        print(f"{contador}.{nodo_tmp.dato.nombre}")
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
            print(f"El nombre de la ciudad selecciona es {c_tmp.dato.nombre}")
            c_tmp.dato.matriz.recorrerM()
            if c_tmp.dato.matriz.civiles.size > 1 :
                print("Si existen civiles a los cuales rescatar")
                tmp = c_tmp.dato.matriz.civiles.cabecera
                cont = 0 
                print("Digite el numero del civil que quiere rescatar")
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
                        

            elif c_tmp.dato.matriz.civiles.size == 1:
                print("Existe un civil el cual puede ser rescatado")
                # civil es una celda
                civil = c_tmp.dato.matriz.civiles.cabecera.dato
                print(f"El civil a rescatar esta en v = {civil.pV} y en h = {civil.pH}")
            else:
                print("No existen civiles a los cuales rescatar")
            


        else:
            print(f"No se encontro la ciudad")
    else:
        print("Respuesta no valida")
        rescate()

def menu():
    print("\n\nSELECCIONE EL TIPO DE MISION")
    print("1.Rescate")
    print("2.Extraccion")
    resp = input(">")
    print(resp)
    if resp == "1":
        rescate()
    elif resp == "2":
        pass
    else:
        print("Opcion incorrecta\n")
        menu()

if __name__ == '__main__':
    lecturaXML()
    #l_ciudades.cabecera.dato.matriz.recorrerMatriz()
    menu()

    # matrizOrtogonal = MatrizOrtogonal()
    # matrizOrtogonal.insertarDato("juan.1-1",1,1)
    # matrizOrtogonal.insertarDato("juan.5-5",5,5)
    # matrizOrtogonal.insertarDato("juan.10-10",10,10)
    # matrizOrtogonal.insertarDato("juan.1-13",1,13)
    # matrizOrtogonal.insertarDato("juan.5-4",5,4)
    # matrizOrtogonal.insertarDato("juan.4-5",4,5)
    # matrizOrtogonal.insertarDato("juan.2-2",2,2)
    # matrizOrtogonal.insertarDato("juan.2-2",1,2)
    # matrizOrtogonal.insertarDato("juan.2-2",1,3)
    # matrizOrtogonal.insertarDato("juan.2-2",1,4)
    # matrizOrtogonal.recorrerMatriz()



