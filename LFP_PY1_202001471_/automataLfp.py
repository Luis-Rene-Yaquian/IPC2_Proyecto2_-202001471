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

from matplotlib.pyplot import text


"""""
ventana=Tk()
ventana.geometry('650x650')
ventana.config(bg='green')
ventana.title('Ventana Principal')
ventana.resizable(width=False,height=False)

ventana.mainloop()



"""









Contenido = ""
boolCarga = False
tokensGlobal = []
erroresGlobal = []

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


class Token():
    def __init__(self,Tipo,Lexema,linea,columna) -> None:
        self.tipo = Tipo
        self.lexema = Lexema
        self.linea = linea
        self.columna = columna

class Error():
    def __init__(self,Tipo,Descripcion,linea,columna) -> None:
        self.tipo = Tipo
        self.Descripcion = Descripcion
        self.linea = linea
        self.columna = columna

class automataLexico():
    def __init__(self,contenido) -> None:
        self.contenido = contenido
        self.estado = 0
    
    def analizar(self):
        self.listaTokens = []
        self.listaErrores = []

        #inicializar atributos
        linea = 1
        columna = 1
        buffer = ''
        centinela = '#' 
        estado = 0
        codigo_fuente =self.contenido + centinela

        i = 0
        while i< len(codigo_fuente):
            c = codigo_fuente[i]
            #Claves
            if estado == 0:
                if c == "\"":
                    estado = 1
                    columna += 1
                elif c == "\'":
                    estado = 2
                    columna += 1
                elif c == " " or c =="\t":
                    columna += 1
                elif c == "f":
                    buffer += c
                    estado = 3
                    columna += 1
                elif c == "~":
                    buffer += c
                    estado = 4
                    columna += 1
                elif c == "t":
                    buffer += c
                    estado = 5
                    columna += 1
                elif c == "v" or c == "e" or c == "i":
                    buffer += c
                    estado = 6
                    columna += 1
                elif c == ",":
                    self.listaTokens.append(Token("Tcoma",c,linea,columna))
                    columna += 1
                elif c == "[":
                    self.listaTokens.append(Token("corcheteA",c,linea,columna))
                    columna += 1
                elif c == "]":
                    self.listaTokens.append(Token("corcheteC",c,linea,columna))
                    columna += 1
                elif c == "<":
                    self.listaTokens.append(Token("menor",c,linea,columna))
                    columna += 1
                elif c == ":":
                    self.listaTokens.append(Token("Dpuntos",c,linea,columna))
                    columna += 1
                elif c == ">":
                    self.listaTokens.append(Token("mayor",c,linea,columna))
                    columna += 1
                elif c == "\n":
                    columna = 1
                    linea += 1
                elif c == centinela and i == len(codigo_fuente)-1:
                    self.listaTokens.append(Token("EOF","Se lee el fin del archivo",linea,columna))
                    break
                else:
                    self.listaErrores.append(Error("Lexico","No se reconoce el simbolo "+c,linea,columna))
                    columna += 1
            elif estado == 1:
                if c == "\"":
                    auxiliar = buffer
                    if auxiliar == "etiqueta":
                        self.listaTokens.append(Token(f"Tetiqueta",auxiliar,linea,columna))
                        columna += 1
                        buffer = ""
                        estado = 0
                    elif auxiliar == "texto":
                        self.listaTokens.append(Token("Ttexto",auxiliar,linea,columna))
                        columna += 1
                        buffer = ""
                        estado = 0
                    elif auxiliar == "grupo-radio":
                        self.listaTokens.append(Token("TgrupoRadio",auxiliar,linea,columna))
                        columna += 1
                        buffer = ""
                        estado = 0
                    elif auxiliar == "grupo-option":
                        self.listaTokens.append(Token("TgrupoOption",auxiliar,linea,columna))
                        columna += 1
                        buffer = ""
                        estado = 0
                    elif auxiliar == "boton":
                        self.listaTokens.append(Token("Tboton",auxiliar,linea,columna))
                        columna += 1
                        buffer = ""
                        estado = 0
                    else:
                        buffer = f"{buffer}"
                        self.listaTokens.append(Token("Tcadena",buffer,linea,columna))
                        columna += 1
                        buffer = ""
                        estado = 0
                else:
                    buffer += c
                    columna += 1
            elif estado == 2:
                if c == "\'":
                    auxiliar = buffer
                    if auxiliar == "etiqueta":
                        self.listaTokens.append(Token(f"Tetiqueta",auxiliar,linea,columna))
                        columna += 1
                        buffer = ""
                        estado = 0
                    elif auxiliar == "texto":
                        self.listaTokens.append(Token("Ttexto",auxiliar,linea,columna))
                        columna += 1
                        buffer = ""
                        estado = 0
                    elif auxiliar == "grupo-radio":
                        self.listaTokens.append(Token("TgrupoRadio",auxiliar,linea,columna))
                        columna += 1
                        buffer = ""
                        estado = 0
                    elif auxiliar == "grupo-option":
                        self.listaTokens.append(Token("TgrupoOption",auxiliar,linea,columna))
                        columna += 1
                        buffer = ""
                        estado = 0
                    elif auxiliar == "boton":
                        self.listaTokens.append(Token("Tboton",auxiliar,linea,columna))
                        columna += 1
                        buffer = ""
                        estado = 0
                    else:
                        buffer = f"{buffer}"
                        self.listaTokens.append(Token("Tcadena",buffer,linea,columna))
                        columna += 1
                        buffer = ""
                        estado = 0
                else:
                    buffer += c
                    columna += 1
            elif estado == 3:

                if c in "formulario" or c in "fondo":
                    buffer += c
                    columna += 1
                else:
                    if buffer == "formulario":
                        self.listaTokens.append(Token("Tformulario",buffer,linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0
                    elif buffer == "fondo":
                        self.listaTokens.append(Token("Tfondo",buffer,linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0
                    else:
                        self.listaErrores.append(Error("Lexico","Se esperaba la palabra formulario.",linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0
            elif estado == 4:
                if c in "~>>":
                    buffer += c
                    columna += 1
                else:
                    if buffer == "~>>":
                        self.listaTokens.append(Token("Tflecha",buffer,linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0
                    else:
                        self.listaErrores.append(Error("Lexico","Se esperaba la flecha.",linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0

            elif estado == 5:
                if c in "tipo":
                    buffer += c
                    columna += 1
                else:
                    if buffer == "tipo":
                        self.listaTokens.append(Token("TTipo",buffer,linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0
                    else:
                        print("encontró un error")
                        self.listaErrores.append(Error("Lexico","Se esperaba la palabra tipo.",linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0
            
            # Otras palabras reservadas.
            elif estado == 6:
                if c in "valor" or c in "valores" or c in "evento" or c in "entrada" or c in "info":
                    buffer += c
                    columna += 1
                else:
                    if buffer == "valor":
                        self.listaTokens.append(Token("Tvalor",buffer,linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0
                    elif buffer == "valores":
                        self.listaTokens.append(Token("Tvalores",buffer,linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0
                    elif buffer == "evento":
                        self.listaTokens.append(Token("Tevento",buffer,linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0
                    elif buffer == "entrada":
                        self.listaTokens.append(Token("Tentrada",buffer,linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0
                    elif buffer == "info":
                        self.listaTokens.append(Token("Tinfo",buffer,linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0
                    else:
                        print("encontró un error")
                        self.listaErrores.append(Error("Lexico","Se esperaba la palabra tipo.",linea,columna))
                        buffer = ""
                        i = i - 1
                        estado = 0
            i += 1


class analizadorSintactico():
    def __init__(self) -> None:
        self.contenido = '''<HTML>
<head>
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">
</head>
<style>
div {
  padding-left: 50px;
}
</style>
<body>
<br><br>
<div >'''
        self.ListaTokens = []
        self.temporal = []
        self.contador = 0

    def Tipos(self):
        if self.ListaTokens[self.contador].tipo == "Tetiqueta":
            self.contador += 1
            if self.ListaTokens[self.contador].tipo == "Tcoma":
                self.contador += 1
                if self.ListaTokens[self.contador].tipo == "Tvalor":
                    self.contador += 1
                    if self.ListaTokens[self.contador].tipo == "Dpuntos":
                        self.contador += 1
                        if self.ListaTokens[self.contador].tipo == "Tcadena":
                            self.contenido += f"\n<br><br>\n<label>{self.ListaTokens[self.contador].lexema}</label>\n"
                            self.contador += 1

        if self.ListaTokens[self.contador].tipo == "Ttexto":
            self.contador += 1
            if self.ListaTokens[self.contador].tipo == "Tcoma":
                self.contador += 1
                if self.ListaTokens[self.contador].tipo == "Tvalor":
                    self.contador += 1
                    if self.ListaTokens[self.contador].tipo == "Dpuntos":
                        self.contador += 1
                        if self.ListaTokens[self.contador].tipo == "Tcadena":
                            
                            cadena = self.ListaTokens[self.contador].lexema
                            self.contador += 1
                            if self.ListaTokens[self.contador].tipo == "Tcoma":
                                self.contador += 1
                                if self.ListaTokens[self.contador].tipo == "Tfondo":
                                    self.contador += 1
                                    if self.ListaTokens[self.contador].tipo == "Dpuntos":
                                        self.contador += 1
                                        if self.ListaTokens[self.contador].tipo == "Tcadena":
                                            textoFondo = self.ListaTokens[self.contador].lexema
                                            self.contenido += f"\n<br><br>\n<input placeholder={textoFondo} value = {cadena}></input>"
                                            self.contador += 1

        if self.ListaTokens[self.contador].tipo == "TgrupoRadio":
            self.contador += 1
            if self.ListaTokens[self.contador].tipo == "Tcoma":
                self.contador += 1
                if self.ListaTokens[self.contador].tipo == "Tvalor":
                    self.contador += 1
                    if self.ListaTokens[self.contador].tipo == "Dpuntos":
                        self.contador += 1
                        if self.ListaTokens[self.contador].tipo == "Tcadena":
                            cadena = self.ListaTokens[self.contador].lexema
                            self.contador += 1
                            if self.ListaTokens[self.contador].tipo == "Tcoma":
                                self.contador += 1
                                if self.ListaTokens[self.contador].tipo == "Tvalores":
                                    self.contador += 1
                                    if self.ListaTokens[self.contador].tipo == "Dpuntos":
                                        self.contador += 1
                                        if self.ListaTokens[self.contador].tipo == "corcheteA":
                                            self.contador += 1
                                            self.contenido += f"<br><br>\n<label>{cadena}</label><br><br>\n"
                                            self.arreglo(cadena)
                                            if self.ListaTokens[self.contador].tipo == "corcheteC":
                                                self.contador += 1

        if self.ListaTokens[self.contador].tipo == "TgrupoOption":
            self.contador += 1
            if self.ListaTokens[self.contador].tipo == "Tcoma":
                self.contador += 1
                if self.ListaTokens[self.contador].tipo == "Tvalor":
                    self.contador += 1
                    if self.ListaTokens[self.contador].tipo == "Dpuntos":
                        self.contador += 1
                        if self.ListaTokens[self.contador].tipo == "Tcadena":
                            cadena = self.ListaTokens[self.contador].lexema
                            self.contador += 1
                            if self.ListaTokens[self.contador].tipo == "Tcoma":
                                self.contador += 1
                                if self.ListaTokens[self.contador].tipo == "Tvalores":
                                    self.contador += 1
                                    if self.ListaTokens[self.contador].tipo == "Dpuntos":
                                        self.contador += 1
                                        if self.ListaTokens[self.contador].tipo == "corcheteA":
                                            self.contador += 1
                                            self.contenido += f"<br><br>\n<label>{cadena}</label>\n"
                                            self.contenido += f"<select name=\"select\" value = \"opciones\">"
                                            self.arregloOption()
                                            self.contenido += "\n</select>\n\n"
                                            if self.ListaTokens[self.contador].tipo == "corcheteC":
                                                self.contador += 1

        if self.ListaTokens[self.contador].tipo == "Tboton":
            self.contador += 1
            if self.ListaTokens[self.contador].tipo == "Tcoma":
                self.contador += 1
                if self.ListaTokens[self.contador].tipo == "Tvalor":
                        self.contador += 1
                        if self.ListaTokens[self.contador].tipo == "Dpuntos":
                            self.contador += 1
                            if self.ListaTokens[self.contador].tipo == "Tcadena":
                                cadena = self.ListaTokens[self.contador].lexema
                                self.contador += 1 
                                if self.ListaTokens[self.contador].tipo == "Tcoma":
                                    self.contador += 1
                                    if self.ListaTokens[self.contador].tipo == "Tevento":
                                        self.contador += 1
                                        if self.ListaTokens[self.contador].tipo == "Dpuntos":
                                            self.contenido += f"\n<br><br>\n<button type=\"button\">{cadena}</button>\n"
                                            self.contador += 1

                                            if self.ListaTokens[self.contador].tipo == "Tentrada":


                                                self.contador += 1
                                            elif self.ListaTokens[self.contador].tipo == "Tinfo":



                                                self.contador += 1

    def arreglo(self,nombre):
        if self.ListaTokens[self.contador].tipo == "Tcadena":
            self.contenido += f"\n<input type=\"radio\" name={nombre} value=\"{self.ListaTokens[self.contador].lexema}\"> {self.ListaTokens[self.contador].lexema}<br>"
            self.contador += 1
            self.arreglo(nombre)
        if self.ListaTokens[self.contador].tipo == "Tcoma":
            self.contador += 1
            self.arreglo(nombre)

    def arregloOption(self):
        if self.ListaTokens[self.contador].tipo == "Tcadena":
            self.contenido += f"\n<option value=\"{self.ListaTokens[self.contador].lexema}\">{self.ListaTokens[self.contador].lexema}</option>"
            self.contador += 1
            self.arregloOption()
        if self.ListaTokens[self.contador].tipo == "Tcoma":
            self.contador += 1
            self.arregloOption()

    def listaInstrucciones(self):
        if self.ListaTokens[self.contador].tipo == "menor":
            self.contador += 1
            self.listaInstrucciones()
        if self.ListaTokens[self.contador].tipo == "TTipo":
            self.contador += 1
            if self.ListaTokens[self.contador].tipo == "Dpuntos":
                self.contador += 1
                self.Tipos()
                if self.ListaTokens[self.contador].tipo == "mayor":
                    self.contador += 1
                    self.listaInstrucciones()
        if self.ListaTokens[self.contador].tipo == "Tcoma":
            self.contador += 1
            self.listaInstrucciones()

    def insCuerpo(self):
        if self.ListaTokens[self.contador].tipo == "menor":
            self.contador += 1
            self.listaInstrucciones()

    def analizar(self):
        if self.ListaTokens[0].tipo == "Tformulario":
            if self.ListaTokens[1].tipo == "Tflecha":
                if self.ListaTokens[2].tipo == "corcheteA":
                    if self.ListaTokens[-2].tipo == "corcheteC":
                        self.contador = 3
                        self.insCuerpo()
                        self.contenido += '''\n</div>
                                            </body>
                                            </HTML>'''
                        escribirArchivo("salida_Progama",self.contenido)

def escribirArchivo(titulo,contenido):
        ruta = titulo+".html"
        try:
            with open(ruta, 'w', encoding='utf-8') as file:
                file.write(contenido)
                print('\nSe genero el archivo correctamente\n')

        except:
            print('\nNo se pudo generar el archivo',titulo+".html","\n")



cargarArchivo()

def generarReporte(titulo,listado,primerColumna):
        contenido = ""
        contenido += "<HTML>"
        contenido += f"\n<title align=\"center\"  > {titulo} </title>"
        contenido += "\n<head>"
        contenido += "<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU\" crossorigin=\"anonymous\">"
            
        contenido += "\n<body>"
        contenido += "\n<table class=\"table table-success table-striped\" >"
        contenido += "\n"
        contenido += f'''
        <thead>
        <tr>
        <th scope="col">#</th>
        <th scope="col">{primerColumna}</th>
        <th scope="col">Tipo</th>
        <th scope="col">Linea</th>
        <th scope="col">columna</th>
        </tr>
        </thead>
        '''
        numero = 1
        for i in listado:
                try:
                    contenido += "<tr>"
                    contenido += f"<td>{numero}</td>"
                    numero += 1
                    if primerColumna == "Lexema":
                        contenido += f"\n<td >{i.lexema}</td>" 
                    else:
                        contenido += f"\n<td >{i.Descripcion}</td>" 
                    contenido += f"\n<td>{i.tipo}</td>"
                    contenido += f"\n<td>{i.linea}</td>"
                    contenido += f"\n<td>{i.columna}</td>"
                    contenido += "\n</tr>"
                except:
                    pass
        contenido +="\n</table>"
        contenido += "\n</body>"
        contenido += "\n</html>"
        try:
            escribirArchivo(titulo,contenido)
        except:
            print("NO se pudo capo :c")



def crearRepoTokens():
    generarReporte("Tokens",tokensGlobal,"Lexema")

def crearRepoErrores():
    generarReporte("Errores",erroresGlobal,"Descripcion")
#Carga info bien
if boolCarga:
    analizador = automataLexico(Contenido)
    analizador.analizar()
    tokensGlobal = analizador.listaTokens
    erroresGlobal = analizador.listaErrores
    con = 0

    if len(analizador.listaErrores) < 1:
        print("Analisis lexico exitoso!")
        sintacticoAna = analizadorSintactico()
        sintacticoAna.ListaTokens = analizador.listaTokens
        sintacticoAna.analizar()
    else:
        try:
            sintacticoAna = analizadorSintactico()
            sintacticoAna.ListaTokens = analizador.listaTokens
            sintacticoAna.analizar()
        except:
            print("Error")
        print("Se encontraron errores lexicos")
        crearRepoTokens()
        crearRepoErrores()