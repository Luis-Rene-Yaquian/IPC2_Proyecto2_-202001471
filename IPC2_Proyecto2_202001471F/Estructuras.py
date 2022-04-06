from graphviz import Digraph
from tkinter import filedialog
import  tkinter as tk
from tkinter import filedialog
import pathlib
import sys
from tkinter import messagebox
from turtle import width
import webbrowser
import os
from tkinter import filedialog, Tk
from tkinter import *
from tkinter import ttk


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

cargarArchivo()

class Nodo:
    def __init__(self):
        self.dato = None
        self.posVertical = None
        self.posHorizontal =None
        self.derecha = None
        self.izquierda = None
        self.arriba = None
        self.abajo = None

class MatrizOrtogonal:
    def __init__(self):
        self.raiz = Nodo()
        self.raiz.posVertical = 0
        self.raiz.posHorizontal = 0

    def crearIndiceVertical(self, pos):

        tmp = self.raiz
        while tmp != None:

            if tmp.abajo == None and tmp.posVertical < pos:

                nuevo = Nodo()
                nuevo.posHorizontal = 0
                nuevo.posVertical = pos
                nuevo.arriba = tmp
                tmp.abajo = nuevo
                return tmp.abajo
            

            if tmp.posVertical == pos :

                return tmp


            if tmp.posVertical < pos and tmp.abajo.posVertical > pos:

                nuevo = Nodo()
                nuevo.posHorizontal = 0
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
                nuevo.posVertical = 0
                nuevo.izquierda = tmp
                tmp.derecha = nuevo
                return tmp.derecha
            
            if tmp.posHorizontal == pos :

                return tmp


            if tmp.posHorizontal < pos and tmp.derecha.posHorizontal > pos:

                nuevo = Nodo()
                nuevo.posHorizontal = pos
                nuevo.posVertical = 0


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
        grafo.node(id, nodo.dato,group=str(nodo.posHorizontal))
        

    def graficarFlechas(self, grafo, nodoE):
        nodo = nodoE
        id = str(nodo.posVertical)+"_"+str(nodo.posHorizontal)
        if nodo.posVertical != 0 and nodo.posHorizontal != 0:

            idV1 = nodo.arriba.posVertical
            idV2 = nodo.arriba.posHorizontal
            idV = str(idV1)+"_"+str(idV2)
            grafo.edge(idV, id)
            grafo.edge(id, idV)


            idH1 = nodo.izquierda.posVertical
            idH2 = nodo.izquierda.posHorizontal
            idH = str(idH1)+"_"+str(idH2)
            grafo.edge(idH,id)
            grafo.edge(id,idH)
        elif nodo.posVertical == 0 and nodo.posHorizontal != 0:

            idAnterior = str(nodo.izquierda.posVertical)+"_"+str(nodo.izquierda.posHorizontal)
            grafo.edge(idAnterior, id)   
        elif nodo.posHorizontal == 0 and nodo.posVertical != 0:
            idAnterior = str(nodo.arriba.posVertical)+"_"+str(nodo.arriba.posHorizontal)
            grafo.edge(idAnterior, id)
        pass





