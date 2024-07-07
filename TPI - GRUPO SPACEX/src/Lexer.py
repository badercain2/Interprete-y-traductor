import ply.lex as lex
import tkinter as tk
    
reservadas = ["VERSION","FIRMA_DIGITAL","EMPRESAS","NOMBRE_EMPRESA","FUNDACION","INGRESOS_ANUALES",
              "PYME","DIRECCION","CALLE","CIUDAD","PAIS","DEPARTAMENTOS","SUBDEPARTAMENTOS",
              "JEFE","EMPLEADOS","NOMBRE","EDAD","CARGO","SALARIO","ACTIVO","FECHA_CONTRATACION",
              "PROYECTOS","ESTADO","FECHA_INICIO","FECHA_FIN","LINK","URL"]

simbolos = ["TEXTO", "COMA","APERT_LISTA","CIERRE_LISTA","APERT_BLOQUE","CIERRE_BLOQUE","NUMERO", "FLOTANTE", "BOOLEANO",
          "FECHA", "ERROR", "VACIO", "TEXTO_RESTRINGIDO_CARGO", "TEXTO_RESTRINGIDO_ESTADO"]

ETIQUETAS_obligatorias = ['EMPRESAS','NOMBRE_EMPRESA','FUNDACION','INGRESOS_ANUALES','PYME', 'DEPARTAMENTOS','NOMBRE','SUBDEPARTAMENTOS']

tokens = simbolos + reservadas

diccionario_errores_lexer = []
miListaTokens = []

t_VERSION = r'"version":'
t_FIRMA_DIGITAL = r'"firma_digital":'
t_EMPRESAS = r'"empresas":'
t_NOMBRE_EMPRESA = r'"nombre_empresa":'
t_FUNDACION = r'"fundacion":'
t_INGRESOS_ANUALES = r'"ingresos_anuales":'
t_PYME = r'"pyme":'
t_DIRECCION = r'"direccion":'
t_CALLE = r'"calle":'
t_CIUDAD = r'"ciudad":'
t_PAIS = r'"pais":'
t_DEPARTAMENTOS = r'"departamentos":'
t_SUBDEPARTAMENTOS = r'"subdepartamentos":'
t_JEFE = r'"jefe":'
t_EMPLEADOS = r'"empleados":'
t_NOMBRE = r'"nombre":'
t_EDAD = r'"edad":'
t_CARGO = r'"cargo":'
t_SALARIO = r'"salario":'
t_ACTIVO = r'"activo":'
t_FECHA_CONTRATACION = r'"fecha_contratacion":'
t_PROYECTOS = r'"proyectos":'
t_ESTADO = r'"estado":'
t_FECHA_INICIO = r'"fecha_inicio":'
t_FECHA_FIN = r'"fecha_fin":'
t_LINK = r'"link":'
t_COMA = r','
t_APERT_LISTA = r'[\{]'
t_CIERRE_LISTA = r'[\}]'
t_APERT_BLOQUE = r'[\[]'
t_CIERRE_BLOQUE = r'[\]]'
t_NUMERO = r'[\d]+'
t_BOOLEANO = r'(true|false)'
t_VACIO = r'(null|[[][ ]*[]]|[{][ ]*[}])'
t_TEXTO_RESTRINGIDO_CARGO = r'(PRODUCT ANALYST|PROJECT MANAGER|UX DESIGNER|MARKETING|DEVELOPER|DEVOPS|DB ADMIN)'
t_TEXTO_RESTRINGIDO_ESTADO = r'(TO DO|IN PROGRESS|CANCELED|DONE|ON HOLD)'
t_FLOTANTE = r'[-+]?(\d*\.\d+|\.\d+)'
        
###----- Tokens de salto de linea o especiales que ignoran o muestran error -----###
def t_ignora_espacios(t):
    r'[ \t\r\f\v]'
    
def t_nueva_linea(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    diccionario_errores_lexer[str(t.value[0])] = str(t.lineno)
    t.lexer.skip(1)
    
def t_FECHA(t):
    r'["](\d{4})-(\d{2})-(\d{2})["]'
    year = int(t.value[1:5])
    month = int(t.value[6:8])
    day = int(t.value[9:11])
    if not ((1900 <= year <= 2099) and (1 <= month <= 12) and (1 <= day <= 31)):
        print('Error en fecha')
    else:
        return t
    
def t_URL(t):
    r'["]http[s]?://([a-zA-Z]+\.)?([a-zA-Z]+)+(\.[a-zA-Z]+)*(:[0-9]+)?(/[a-zA-Z]+)*["]'
    return t

def t_TEXTO(t):
    r'\"([^\\\n]|(\\.))*?\"[:]?'
    if t.value[-1] == ':':
        t.value = t.value.strip(':')   
        if t.value.upper().strip('"') in reservadas:
            t.type = t.value.upper().strip('"')
        else:
            t.type = 'ERROR'
            diccionario_errores_lexer[str(t.value)] = str(t.lineno)  # Guarda los errores en un diccionario, para luego mostrarlos
    else:
        if t.value.upper().strip('"') in t_TEXTO_RESTRINGIDO_CARGO:
            t.type = 'TEXTO_RESTRINGIDO_CARGO'
        if t.value.upper().strip('"') in t_TEXTO_RESTRINGIDO_ESTADO:
            t.type = 'TEXTO_RESTRINGIDO_ESTADO'
    return t

# Analiza etiquetas faltantes
def obtener_tipos_tokens(data):
    tipos_tokens = set()  # Utilizamos un conjunto para evitar duplicados
    lexer.input(data)
    for tok in lexer:
        tipos_tokens.add(tok.type) # Carga la lista con los tokens que se escribieron
    return list(tipos_tokens)

# Construccion del lexer
lexer = lex.lex()

# Evalua el texto e imprime los tokens encontrados
def evaluarTexto(Ingreso_de_Texto):
    lexer.lineno = 1    #Inicializa el lineno en 1 siempre que iniciemos un archivo
    
    while True:
        token = lexer.token()
        if not token:
            break
        miListaTokens.append((token.type, token.value))
        # Ingreso_de_Texto.insert(tk.END, "N° Linea: {:4} | Token: {:16} | Valor: {:16}\n".format(str(token.lineno), str(token.type), str(token.value)))
