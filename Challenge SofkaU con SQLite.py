# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:07:25 2022

@author: Andres Amaya Chaves
"""

# Se importan las librerías necesarias
import random
from tabulate import tabulate
import sqlite3 


#----------------
# 0. Conexión con la base de datos
#----------------

# 0.1 CONEXIÓN GLOBAL A BASE DE DATOS
#..............................................
conexion1 = sqlite3.connect('SofkaUniversity.db')





#..............................................
#..............................................


# 0.2 Definificón de las funciones que leen y modifican la base de datos
# Las siguientes funciones permiten leer y modificar las tablas de la base de datos conectada
#..............................................
"""
@PARÁMETROS:
conexionActual            = Conexión para acceder a la base de datos
IngresarTextoPregunta     = Texto de la pregunta (string)
IngresarCategoriaPregunta = Categoría de la pregunta
---
ConjuntoRespuestas        = Lista con los strings de las 4 respuestas posibles (deben ser exactamente 4 strings)
IndresarCorrecta          = {1,2,3,4} índie de la respuesta es correcta
"""
def BDingresarNuevaPreguntaRespuesta(conexionActual, IngresarTextoPregunta, IngresarCategoriaPregunta, ConjuntoRespuestas, IngresarCorrecta):       
    
    SentenciaPregunta = f'INSERT INTO Preguntas (Texto, Categoria) VALUES ("{IngresarTextoPregunta}", "{IngresarCategoriaPregunta}")' 
    conexionActual.execute(SentenciaPregunta)
    conexionActual.commit
    
    idPreguntaIngresada  = conexionActual.execute(f'SELECT id FROM PREGUNTAS WHERE Texto = "{IngresarTextoPregunta}"')
    
    EsLaCorrecta = []
    for i in range(4):
        if IngresarCorrecta-1 == i:
            EsLaCorrecta.append(1)
        else: 
            EsLaCorrecta.append(0)
    
    for j in range(4):
        SentenciaRespuestas = f'INSERT INTO Respuestas (Texto, ID_Pregunta, Correcta) VALUES ("{ConjuntoRespuestas[j]}", {idPreguntaIngresada}, {EsLaCorrecta[j]})'
        conexionActual.execute(SentenciaRespuestas)
        conexionActual.commit
    
    print("Pregunta ingresada, con el conjunto de 4 respuestas. Guardadas en Base de Datos.")
    
# 0.2.1 Función BDingresarNuevoJugador
"""
@PARÁMETROS:
conexionActPremios = Conexión para acceder a la base de datos
IngresarNombre     = Nombre del jugador a ingresar en la base de datos
IngresarEdad       = Edad del jugador a ingresar en la base de datos
"""
def BDingresarNuevoJugador(conexionActual, IngresarNombre, IngresarEdad):       
    
    conexionActual.execute( f'INSERT INTO Jugador (NombreJugador, Edad, CantidadPreguntasRespondidas, VecesJugadas, DineroAcumulado) VALUES ("{IngresarNombre}", {IngresarEdad}, 0, 0, 0)')
    conexionActual.commit


# 0.2.2 Función BDobtenerRegistroJugador
"""
@PARÁMETROS:
conexionActual        = Conexión para acceder a la base de datos
IngresarNombre            = Nombre del jugador a ingresar en la base de datos
IngresarEdad              = Edad del jugador a ingresar en la base de datos


# Se dice que un jugador es el mismo cuando {Nombre, Edad} ingresados coinciden con algún registro en la base de datos.
# Esta función devuelve el id del jugador que concide en Nombre y Edad
"""
def BDobtenerRegistroJugador(conexionActual, IngresarNombre, IngresarEdad):
    
    Sentencia = f'SELECT * FROM Jugador WHERE NombreJugador = "{IngresarNombre}" and Edad = {IngresarEdad}'
    Consulta =  conexionActual.execute(Sentencia)
    RegistroJugador = []
    
    Etiquetas = ["ID Jugador", "Nombre Jugador", "Edad", "Cant. Preguntas Respondidas", "Cant. Preguntas Bien", "Veces Jugadas", "Dinero Acumulado"]
    CC = list(Consulta.fetchone())
    for k in range(7):
        RegistroJugador.append([Etiquetas[k], CC[k]])
        
        
    
    return  tabulate(RegistroJugador, headers=["ID Jugador", "Nombre Jugador", "Edad", "Cant. Preguntas Respondidas", "Cant. Preguntas Bien", "Veces Jugadas", "Dinero Acumulado"])  
    
# 0.2.3 Función BDobtenerIdJugador
"""
@PARÁMETROS:
conexionActual        = Conexión para acceder a la base de datos
IngresarNombre            = Nombre del jugador a ingresar en la base de datos
IngresarEdad              = Edad del jugador a ingresar en la base de datos


# Se dice que un jugador es el mismo cuando {Nombre, Edad} ingresados coinciden con algún registro en la base de datos.
# Esta función devuelve el id del jugador que concide en Nombre y Edad
"""
def BDobtenerIdJugador(conexionActual, IngresarNombre, IngresarEdad):
    
    Sentencia = f'SELECT ID_Jugador FROM Jugador WHERE NombreJugador = "{IngresarNombre}" and Edad = {IngresarEdad}'
    Consulta =  conexionActual.execute(Sentencia)
    
    return Consulta
          

# 0.2.4 Función BDJugadorExiste
"""
@PARÁMETROS:
conexionActPremios        = Conexión para acceder a la base de datos
IngresarNombre            = Nombre del jugador a ingresar en la base de datos
IngresarEdad              = Edad del jugador a ingresar en la base de datos
IngresarCantidadPreguntas = Cantidad de preguntas jugadas
DineroAcumulado           = Dinero que se acumuló en el juego

# Se dice que un jugador es el mismo cuando {Nombre, Edad} ingresados coinciden con algún registro en la base de datos.
# Esta función devuelve un booleano que responde si el jugador ya exise o no dentro de la base de datos
"""
def BDJugadorExiste(conexionActual, IngresarNombre, IngresarEdad):
    
    Existe = False
    Sentencia = f'SELECT * FROM Jugador WHERE NombreJugador = "{IngresarNombre}" and Edad = {IngresarEdad}'
    Consulta = conexionActual.execute(Sentencia)
    
    if len(Consulta.fetchall()) > 0:
       Existe = True
    return Existe


# 0.2.5 Función BDActualizarDatosJugador
"""
@PARÁMETROS:
conexionActPremios        = Conexión para acceder a la base de datos
IngresarNombre            = Nombre del jugador a ingresar en la base de datos
IngresarEdad              = Edad del jugador a ingresar en la base de datos
IngresarCantidadPreguntas = Cantidad de preguntas jugadas
DineroAcumulado           = Dinero que se acumuló en el juego

# Esta función se llamará al finalizar un nuevo juego con el jugador existente especificado, entonces VecesJugadas += 1 siempre que se llame la función.
"""
def BDActualizarDatosJugador(conexionActual, ID_JugadorActual, IngresarNombre, IngresarEdad, IngresarCantidadPreguntas, IngresarCantidadPreguntasBien, DineroAcumuladoActual):       

    """    
    if BDJugadorExiste(conexion1, IngresarNombre, IngresarEdad):
        
        Sentencia = f'SELECT VecesJugadas, DineroAcumulado, CantidadPreguntasRespondidas, CantidadPreguntasBien  FROM Jugador WHERE ID_Jugador = {ID_JugadorActual}'
        consulta = conexionActual.execute(Sentencia)    
        DatosConsulta = consulta.fetchall()
        VecesJugadasBase = DatosConsulta[0]
        DineroAcumuladoBase = DatosConsulta[1]
        CantPreguntasBase  = DatosConsulta[2]
        CantPreguntasBienBase = DatosConsulta[3]
    
    else:
    """
    
    VecesJugadasBase = 0
    DineroAcumuladoBase = 0
    CantPreguntasBase  = 0
    CantPreguntasBienBase = 0
    
    SentenciaPrincipal = f'UPDATE Jugador SET (CantidadPreguntasRespondidas, CantidadPreguntasBien, VecesJugadas, DineroAcumulado) = ({CantPreguntasBase}+{IngresarCantidadPreguntas}, {CantPreguntasBienBase}+{IngresarCantidadPreguntasBien}, {VecesJugadasBase}+1, {DineroAcumuladoBase}+{DineroAcumuladoActual})' 
    conexionActual.execute(SentenciaPrincipal)
    
    conexionActual.commit


# 0.2.7 Función BDleerPremios       
"""
@PARÁMETROS:
conexionPremios = Conexión para acceder a la base de datos
"""    
def BDleerPremios(conexionActPremios):
    
    ListaPremios = []    
    ListaPremiosImprimir = []
    cursor = conexionActPremios.execute('SELECT * FROM Premios ORDER BY RONDA')
    
    for fila in cursor:
     ListaPremios.append(fila[1])
     
    for y in range(5):
        ListaPremiosImprimir.append([y+1,ListaPremios[y]])
     
    return  (ListaPremios, ListaPremiosImprimir)

# 0.2.8 Función actualizarPremios       
"""
@PARÁMETROS:
conexionActPremios = Conexión para acceder a la base de datos
Ronda = Número de Ronda a modificar
NuevoValorPremio = Nuevo valor del premio de la ronda
"""
def BDactualizarPremio(conexionActPremios, Ronda, NuevoValorPremio):       
    
    Sentencia = f'UPDATE Premios SET ValorPremio = {NuevoValorPremio} WHERE RONDA = {Ronda}' 
    conexionActPremios.execute(Sentencia)
    conexionActPremios.commit()
    
def BDactualizarConjuntoPremios():
    for i in range(5):
        
        valorPremioRondaX = mIngresarVariable("Por favor define el premio (en USD) para la ronda " + str(i+1) + ":\n",
                                   "Por favor ingresa un valor numérico para el premio para la ronda # " + str(i+1) + ":\n",int)          
        BDactualizarPremio(conexion1,i,valorPremioRondaX)
    
# 0.2.9 Función BDLeerPregunta
"""
@PARÁMETROS:
conexionActPremios = Conexión para acceder a la base de datos
Ronda = Número de Ronda a modificar
indicePreguntaLeer = índice de la pregunta a leer, dentro de la ronda respectiva
"""
def BDLeerPregunta(conexionActPregunta, Ronda, indicePreguntaLeer):       
    
    cursor = conexionActPregunta.execute(f'SELECT Texto FROM Preguntas WHERE indiceX = {indicePreguntaLeer} AND Categoria = {Ronda} ')
    return cursor.fetchone()[0]


# 0.2.10 Función BDLeerRespuestas
"""
@PARÁMETROS:
conexionActPremios = Conexión para acceder a la base de datos
Ronda = Número de Ronda a modificar
indicePregunta = índice de la pregunta relativa a la respuesta respectiva
"""
def BDLeerRespuestas(conexionActPregunta, Ronda, indicePregunta):       
    
    ListaRespuestas = []
    cursor = list(conexionActPregunta.execute(f'SELECT R.Texto FROM Preguntas as P JOIN Respuestas as R ON P.id = R.ID_Pregunta WHERE indiceX = {indicePregunta} AND Categoria = {Ronda}'))
                                         
    for fila in cursor:
        ListaRespuestas.append(fila[0])
          
    return  ListaRespuestas


#..............................................
#..............................................


# 0.3 Definificón de las funciones MODULARES que efectuan tareas repetitiavs en el código
#..............................................

# 0.3.1 Función mIngresarVariable
""" 
@PARÁMETROS:
TextoIngreso = Texto inicial para pedir el ingreso de la variable
TextoErrorTipo = Texto a mostrar cuando se ingresa el tipo equivocado
TipoVariable = Tipo de variable que se espera recibir
"""
def mIngresarVariable(TextoIngreso, TextoErrorTipo, TipoVariable):
    
    ok = 0
    while ok == 0:
            
        if TipoVariable == str:
            try:
                Variable = str(input(TextoIngreso))
                ok=1
            except:
                Variable = input(TextoErrorTipo)
                while type(Variable) != TipoVariable:                    
                    Variable = str(input(TextoErrorTipo))
                ok=1
        
        elif TipoVariable == int: 
            try:
                Variable = int(input(TextoIngreso))
                ok=1
            except:
                Variable = input(TextoErrorTipo)
                while type(Variable) != TipoVariable:                    
                    Variable = int(input(TextoErrorTipo))
                ok=1

    
    return Variable

#0.3.2 mIngresarVariableOpciones
"""
@PARÁMETROS:
    TextoIngresoOp = Texto inicial para pedir el ingreso de la variable
    TextoErrorTipoOp = Texto a mostrar cuando se ingresa el tipo equivocado
    TextoErrorValorOp = Texto a mostrar cuando se ingresa el valor equivocado
    TipoVariableOp = Tipo de variable que se espera recibir
    Opciones = Lista con las opciones que permite la variable
"""
def mIngresarVariableOpciones(TextoIngresoOp, TextoErrorTipoOp, TextoErrorValorOp, TipoVariableOp, Opciones):
    
    VariableOp = mIngresarVariable(TextoIngresoOp, TextoErrorTipoOp, TipoVariableOp)
        
    while VariableOp not in Opciones:
         VariableOp = input(TextoErrorValorOp)
        
    return VariableOp



#..............................................
#..............................................


# 0.4 Definificón de las funciones CONFIGURACIONALES que modifican indirectamente las bases de datos
#..............................................


# 0.4.1 Función ConfigurarPremios
"""
@PARÁMETROS: Null

# Modifica el conjunto de valores de los premios de cada ronda    
"""
def ConfigurarPremios():
    
    print("\nActualmente los premios para las 5 rondas están definidos así:\n")        
    print(tabulate(BDleerPremios(conexion1)[1], headers=["Ronda", "Valor del Premio (USD)" ]))
       
    BDactualizarConjuntoPremios()
    conexion1.commit()

    print("\nNueva cpnfiguración de los premios, quedaron definidos así:\n")        
    print(tabulate(BDleerPremios(conexion1)[1], headers=["Ronda", "Valor del Premio (USD)" ]))


# 0.4.2 Función ConfigurarPreguntaX
"""
@PARÁMETROS:
    X = número de pregunta a ingresar dentro de la categoría numCategoria
    numCategoria = categoría en la que se va a modificar la pregunta
# Modifica el conjunto de valores de los premios de cada ronda    
"""   
def ConfigurarPreguntaX(X, numCategoria):
    
    TextoIngreso = "Ingresa la pregunta " + str(X) +" de la categoría " + str(numCategoria) + ":\n "
    TextoErrorTipo = "La pregunta debe ser un texto"            
    TextoPregunta = mIngresarVariable(TextoIngreso, TextoErrorTipo, str)
    
    print("\nAhora ingresarás 4 respuestas a la pregunta recién ingresada. Solamente 1 de ellas debe ser correcta. Después de haber ingresado las 4, podrás indicar cuál de ellas es la correcta.\n")
    ConjuntoRespuestas = []
    for g in range(4):
        TextoIngreso = "Ingresa la respuesta "+ str(g+1) + " de la pregunta " + str(X) + " de la categoría " + str(numCategoria) + ": "
        TextoErrorTipo = "La pregunta debe ser un texto"            
        ConjuntoRespuestas.append(mIngresarVariable(TextoIngreso, TextoErrorTipo, str))                
    
    TextoIngreso = "Ingresa el número de pregunta que es CORRECTA denrto de la categoría " + str(numCategoria) + ": "
    TextoErrorTipo = "Debes ingresar un número entero entre 1 y 4: "            
    TextoErrorValor = "La respuesta correcta debe corresponder a un número entero entre 1 y 4"
    Correcta = mIngresarVariableOpciones(TextoIngreso, TextoErrorTipo, TextoErrorValor, int, [1,2,3,4] )
    
    BDingresarNuevaPreguntaRespuesta(conexion1, TextoPregunta, numCategoria, ConjuntoRespuestas, Correcta)
    
    return [TextoPregunta, ConjuntoRespuestas, Correcta]
  

# 0.4.3 Función ConfigurarCategoriaX
"""
@PARÁMETROS:
numCategoria = Categoría a modificar

# Retorna la lista actual de premios desde la base de datos (lista con solo los valores)
"""                   
def ConfigurarCategoriaX(numCategoria):
    
    print("\nSe agregarán preguntas a la categoría del nivel " + str(numCategoria)) 
    
    for w in range(5):
            (w, numCategoria)        
 
    NuevaPregunta = mIngresarVariableOpciones("¿Deseas ingresar una nueva pregunta a la categoria " + str(numCategoria) + "?\n1: Sí\n2: No", 
                                              "La pregunta debe ser un número.", 
                                              "La respuesta correcta debe corresponder a un número entero entre 1 y 2",
                                              int, [1,2]) 
    pp = 6
    while NuevaPregunta == 1:
        ConfigurarPreguntaX(pp, numCategoria)        
        pp +=1
    

# 0.4.4 Función ConfigurarTodasPreguntas
"""
@PARÁMETROS:

# Lleva al usuario a configurar todas las preguntas de las 5 categorías
"""         
def ConfigurarTodasPreguntas():        
    for i in range(5):
        ConfigurarCategoriaX(i)



#..............................................
#..............................................


# 0.5 Definificón de las funciones DE ACCIÓN
#..............................................


# 0.5.1 Función AumentarNivel
"""
@PARÁMETROS:

# Aumenta el nivel del juego
"""    
def AumentarNivel(Juego1, nivel):
    
    IndicePregunta = random.choice([1,2,3,4])
    
    Pregunta = BDLeerPregunta(conexion1, nivel, IndicePregunta)
    Opciones = BDLeerRespuestas(conexion1, nivel, IndicePregunta)
    
    print(Pregunta)
    print("")

    Op = Opciones.copy()     #Op = Opciones.copy()
    random.shuffle(Opciones)    
    letras = ["A.","B.","C.","D."]
    
    OpcionesFinal = []
    for i in range(4):
        OpcionesFinal.append([letras[i],Opciones[i]])
   
    TablaRespuestas = tabulate(OpcionesFinal, headers=["Opción", "" ])
    
    RespCorrecta = Opciones.index(Op[0])
    
    return [TablaRespuestas, RespCorrecta]


# 0.5.2 Función verificarRespuesta
"""
@PARÁMETROS:

# Verifica si la respuest ingresadaa es correcta o no
"""   
def verificarRespuesta(OpcionEscogida, OpcionCorrecta):
    EsCorrecto = 0
    if OpcionEscogida == OpcionCorrecta:
        EsCorrecto = 1
        print("¡Correcto! Puedes Avanzar a la siguiente ronda.")
    else:
        print("¡Incorrecto! Perdiste el juego, y perdiste el dinero acumulado.")
    
    return EsCorrecto       

# 0.5.3 Función jugar parte 1
"""
@PARÁMETROS:

# Ejecuta la opción 'B' del MENU PRINCIPAL
"""      

def jugarParte1(nom1, ed1):
    
    parar = 0
    while parar == 0:        
        
        if BDJugadorExiste(conexion1,nom1,ed1):
            opcionNombre = mIngresarVariableOpciones("\n1:¿Quieres usar otro nombre? o\n2:Usar el nombre ya ingresado\n",
                                             "ERROR. Ingresa un valor numérico. 1:¿Quieres usar otro nombre? o\n2:Usar el nombre ya ingresado\n",
                                             "ERROR. Ingresa 1 o 2.\n 1:¿Quieres usar otro nombre? o\n2:Usar el nombre ya ingresado\n",int,
                                             [1,2])    
            if opcionNombre == 1:
                NuevoNom = mIngresarVariable("Ingresa el nombre con el que quieres jugar", "Ingresa el nombre como un texto por favor: ",str)
                nom1 = NuevoNom
        else: 
            parar = 1
            

def jugarParte2(JugadorActualP2, JuegoPrincipalP2):
    
    nivelJuego = 1
    DineroAcumulado = 0
    CantidadPreguntasRespondidas = 0
    CantidadPreguntasBien = 0
    
    salir = 0    
    while salir == 0:
        
        print("\n..............\nRONDA # " + str(nivelJuego) + "\n")
        
        Ronda = AumentarNivel(JuegoPrincipalP2, nivelJuego)        
        
        print(Ronda[0],"")
        respuestaActual = mIngresarVariableOpciones("Tu respuesta es: ", 
                                                    "\nIngresa un valor de texto", 
                                                    "ERROR. Ingresa A, B, C ó D según desees. ", str,
                                                    ["A","B","C","D","a","b","c","d","A.","B.","C.","D.","a.","b.","c.","d."])
        
        
        if respuestaActual in ["A", "a", "A.", "a."]: respuestaActual = 0
        elif respuestaActual in ["B", "b", "B.", "b."]: respuestaActual = 1
        elif respuestaActual in ["C", "c", "C.", "c."]: respuestaActual = 2
        else:   respuestaActual = 3
          
        CantidadPreguntasRespondidas += 1
        if verificarRespuesta(respuestaActual, Ronda[1]) == 1:              # Llama a la función 'verificarRespeuesta' para verificar si la respuestaActual es la respuestaCorrecta
            JugadorActualP2.preguntasBien += 1                  
            DineroAcumulado += JuegoPrincipalP2.premios[nivelJuego-1][1]    # Acumula el premio correspondiente a la ronda actual            
            
            CantidadPreguntasBien += 1
            
            if nivelJuego < 5:
                
                print("En este momento tienes un acumulado de " + str(DineroAcumulado) + " USD. Puedes retirarte con lo que tienes o avanzar a la sigueinte ronda.")
                               
                JugadorContinua = mIngresarVariableOpciones("¿Deseas continuar a la siguiente ronda?\nIngresa...\n1: para SÍ, o \n0: para NO:\n",
                                                    "ERROR. Ingresa...\n1: para SÍ, o \n0: para NO:\n",
                                                    "ERROR. Ingresa 0 o 1, según desees.",
                                                    int, [0,1])
                                                        
                if JugadorContinua == 1:
                    nivelJuego += 1                
                    
                else:
                    print("Fin del juego. Te vas con " + str(DineroAcumulado) + " USD!")
                    JugadorActualP2.vecesJugadas += 1
                    salir = 1
                    
            else:
                print("¡FELICITACIONES, GANASTE EL JUEGO!", 
                      "¡Ganaste el premio mayor: " + str(sum(JuegoPrincipalP2.premiosRaw)) + " USD!")
                JugadorActualP2.vecesJugadas += 1           
                salir = 1
                
        else:
            DineroAcumulado = 0
            salir = 1        
            
    return [JugadorActualP2.nombre, JugadorActualP2.edad, CantidadPreguntasRespondidas, CantidadPreguntasBien, DineroAcumulado]
  

def Menu_A(J_A):
    
    print("\n\n*********************\nMENÚ DE CONFIGURACIÓN\n*********************\n\n\nElige una de las siguientes opciones.")
        
    config1 = mIngresarVariableOpciones("¿Que deseas configurar?\n\n1: Configurar valor de los premios\n2: Configurar preguntas\n\n3: Volver al MENU PRINCIPAL\n\n", 
                                        "ERROR. Ingresa un valor numérico: ", 
                                        "ERROR. Ingresa 1,2, o 3 según desees: ",
                                        int, [1,2,3])
    if config1 == 1:
        BDactualizarConjuntoPremios()        
        
    elif config1 == 2:
        
        config2 = mIngresarVariableOpciones("Elige, ¿Deseas modificar las preguntas de...\n1: una sola categoría? o\n2: todas las categorías?\n\n",
                                            "ERROR. Ingresa un valor numérico: ",
                                            "ERROR. Ingresa 1,2 según desees.",
                                            int, [1,2])
 
        if config2 == 1:
            cat = mIngresarVariableOpciones("¿Cuál categoría deseas modificar?\nElige un número entero entre 1 y 5: ",
                                            "ERROR. Ingresa un valor numérico: ",
                                            "ERROR. Ingresa 1,2 según desees.",
                                            int, [1,2,3,4,5])            
            ConfigurarCategoriaX(cat)
        else:
            ConfigurarTodasPreguntas()


def Menu_B(juegoPrincipal):
    
     
    TablaPremios = tabulate(juegoPrincipal.premios, headers=["Ronda", "Premio Acumulable (USD)"], tablefmt='orgtbl')
    print("¡BIENVENIDO AL JUEGO! \n")
    print("El juego tiene 5 rondas, en cada una de ellas deberás responder una pregunta de cultura general.\n")
    print("Antes de iniciar cada ronda se te dera la opción de retirarte del juego CON el dinero acumulado hasta el momento.")
    print("Una vez veas la pregunta ya no hay opción de salir voluntariamente \n")
    print("Responder bien una pregunta te permitirá pasar a la siguiente ronda y acumularás el dinero correspondiente según la siguiente tabla.\n")
    print(TablaPremios)
    print("\nSi respondes mal a cualquiera de las preguntas el juego finalizará tempranamente y saldrás del juego SIN el dinero acumulado hasta el momento.")
    
    
    nom = mIngresarVariable("Conozcámonos antes de empezar.\nEscribe tu nombre: ", 
                            "Ingresa tu nombre como un texto por favor: ",
                            str)
    
    ed = mIngresarVariableOpciones("Ingresa tu edad en años:", 
                                    "ERROR. Ingresa un valor numérico\n",
                                    "ERROR. Ingresa un número entero entre 0 y 200.\n", 
                                    int, range(200))  
    
    
    jugadorActual = Jugador(nom, ed)
    
    jugarParte1(nom, ed)
    print("\n¡Empecemos!\n")     
    DATOS_JUEGO = jugarParte2(jugadorActual, juegoPrincipal)           
            
    jugadorActual.acumularJuegoActual(DATOS_JUEGO[2], DATOS_JUEGO[3], DATOS_JUEGO[4])
    jugadorActual.guardarNuevoJugador()


def Menu_C():
    
    nombreJugador = mIngresarVariable("Ingresa el nombre del jugador a consultar: ", 
                                      "El nombre debe ser un texto", str)
    
    edadJugador = mIngresarVariableOpciones("\nIngresa la edad del jugador en años: ",
                              "ERROR. Ingresa un valor numérico\n",
                              "ERROR. Ingresa un número entero entre 0 y 200.\n", 
                              int, range(200)) 
    
    print("\nREGISTRO\n")

    if BDJugadorExiste(conexion1,nombreJugador, edadJugador) == False :
        print("El jugador buscado no está en la base de datos.\n")
        
   
    else:
        
        print(BDobtenerRegistroJugador(conexion1, nombreJugador, edadJugador))
 


def MENU_PRINCIPAL():
        
    
    menuP = []
    
    print("")
    print("¡BIENVENIDO! \n\n**************\nMENU PRINCIPAL\n**************\n\n¿Qué deseas hacer?\n")
    print("A: CONFIGURAR\nB: JUGAR\nC: Consultar Jugador")
    opcionInicio = input("Ingresa tu opción (A / B / C): ")
    
    J = Juego()    
    
    while opcionInicio not in ["A","B", "C", "a","b","c"]:
        opcionInicio= input("ERROR. Ingresa A, B ó C según desees.\nA: CONFIGURAR\nB: JUGAR\nC: Consultar Jugador...:\n")
    
    if opcionInicio in ["A","a"]:        
        Menu_A(J)
        
    elif opcionInicio in ["B","b"]:        
        menuP = Menu_B(J)          
        
    else:
        Menu_C()
                    
    return menuP  



#----------------
# 1. Definición de Clases
#----------------



# 1.1 DEFINE LA CLASE 'Jugador'
#..............................................

class Jugador:
        def __init__(self, nombreJugador, edadJugador):     # Constructor de la clase jugador
            self.id = -1                                    # id = -1 quiere ecir que el jugador es nuevo y mantendrá ese id hasta que sus datos se guarden en la BD
            self.nombre = nombreJugador
            self.edad = int(edadJugador)
            self.preguntasRespondidas = 0
            self.preguntasBien = 0
            self.vecesJugadas = 0
            self.dineroGanado = 0
        
        def guardarNuevoJugador(self):                           # Guarda el nuevo jugador en la base de datos
            BDingresarNuevoJugador(conexion1, self.nombre, self.edad)            
            
        def acumularJuegoActual(self, cantPreguntas, cantPreguntasBien, premioActual):     #  Guarda los datos del jugador en la base de datos
            self.guardarNuevoJugador()
            idJugador = BDobtenerIdJugador(conexion1, self.nombre, self.edad)
            BDActualizarDatosJugador(conexion1, idJugador,self.nombre, self.edad, cantPreguntas, cantPreguntasBien, premioActual)




        
# 1.2 DEFINE LA CLASE 'Juego'
#..............................................
class Juego:
    def __init__(self):
        self.nivel = 1
        self.premiosRaw = BDleerPremios(conexion1)[0]
        self.premios = BDleerPremios(conexion1)[1]
        
        
        
"""
==========================================================
"""

####    
### Ejecución del Programa    
####

OtroJuego = 1
while OtroJuego == 1:    
    
    MENU_PRINCIPAL()
    
    OtroJuego = mIngresarVariableOpciones("¿Deseas volver al MENÚ PRINCIPAL?\n\n1: Sí\n2: No\n\n",
                                          "ERROR. Ingresa un valor numérico, por favor.\n\n1: Sí\n2: No\n\n",
                                          "ERROR. Por favor ingresa...\n\n1: Sí\n2: No\n\n", int, [1,2])
conexion1.close()
print("Gracias por jugar. ¡Hasta Luego!")                               
  





"""
MENU PRINCIPAL

A: CONFIGURAR
    1. Configurar valor de los premios
    2. Configurar Preguntas
        1. una sola categoría
        2. todas las categorías
        
B: JUGAR

C: Consultar Jugador

"""