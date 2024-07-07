import Lexer
import Parser
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os
import sys # para detener la ejecucion de la terminal cuando cierro el thinker


def Buscar_Archivo():
    # Crear una ventana Tkinter oculta
    global texto_ingresado  # Hacemos global a esta variable, para poder ocuparla en el analizador de texto
    
    root = tk.Tk()
    root.withdraw()
    
    # Abrir un cuadro de diálogo para seleccionar el archivo
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("JSON files", ".json"), ("All files", ".*")) # oculta archivos con extensiones que no sea .json
    )
    global file_name
    file_name = os.path.basename(file_path)
    file_name = file_name.strip(".json") + ".html"
    # Eliminamos todo el contenido previo en caso de que quiera analizar otra vez.
    Ingreso_de_Texto.delete(1.0, tk.END)

    # Acá copia toda la info del archivo en la pantalla
    texto_ingresado = leer_archivo(file_path)
    Ingreso_de_Texto.insert(tk.END, texto_ingresado)

    messagebox.showinfo("BUSCAR ARCHIVO", "¡Se ha cargado el archivo con exito!")

def leer_archivo(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Lectura de archivo
def Analizador_Texto():

    band_NO_error_lexer = True  # Si el lexer tiene algo mal escrito o le falta algun token no parsea hasta que se solucionen los errores

    # Tomo el texto de la ventana y se lo paso al lexer
    input_string = Ingreso_de_Texto.get("1.0", tk.END)
    Lexer.lexer.input(input_string)

    # Borra todo lo que hay en pantalla del thinker e imprime los tokens
    Ingreso_de_Texto.delete(1.0, tk.END)
    Lexer.diccionario_errores_lexer = {}
    Lexer.evaluarTexto(Ingreso_de_Texto)
    
    #Verifica si hay un error en el lexer y muestra su posicion
    if (len(Lexer.diccionario_errores_lexer) > 0):
        band_NO_error_lexer = False
        Ingreso_de_Texto.insert(tk.END, "\nError en el Lexer\n")
        for error in Lexer.diccionario_errores_lexer:
            Ingreso_de_Texto.insert(tk.END, "Etiqueta con error: -> {:20} | En la linea {:16}\n".format(error, Lexer.diccionario_errores_lexer[error]))
    
    # Definimos los tokens encontrados en el texto para usarlos en la traduccion
    global tipos_tokens 

    # Esto nos ayuda a cargar la lista con todos los tokens utilizados
    tipos_tokens = Lexer.obtener_tipos_tokens(texto_ingresado)

    set1 = set (tipos_tokens)
    set2 = set (Lexer.ETIQUETAS_obligatorias)
    
    # Encontrar la diferencia de los conjuntos
    palabras_unicas_lista2 = set2 - set1

    # Muestra tokens obligatorios que NO aparecieron
    if palabras_unicas_lista2:
        band_NO_error_lexer = False
        Ingreso_de_Texto.insert(tk.END, "\nEtiquetas faltantes obligatorias no evaluadas: \n-> ")
        Ingreso_de_Texto.insert(tk.END,", ".join(f"{elemento}" for elemento in sorted(palabras_unicas_lista2)))
    
    if band_NO_error_lexer:
        Lexer.lexer.lineno = 1  #Reinicia el contador de lineas para cuando llegue a leer el parser
        Parser.diccionario_errores_parser = {}
        Parser.parser.parse(input_string)
    
        Ingreso_de_Texto.insert(tk.END, "\n###----------------------------------------------###\n")
        if (len(Parser.diccionario_errores_parser) == 0):
            Ingreso_de_Texto.insert(tk.END, "Esta escrito correctamente y se logro analizar")
            # Aca ingresar primero el div incio y cierre
            crearHTML()
        else:

            Ingreso_de_Texto.insert(tk.END, "\nError en el Parser\n\n")
            for error in Parser.diccionario_errores_parser:
                Ingreso_de_Texto.insert(tk.END, "Etiqueta con error: -> {:20} | En la linea {:16}\n".format(error, Parser.diccionario_errores_parser[error]))

def crearHTML():
    # Creamos un archivo con un identificador unico aaaa/mm/dd_horas/minutos/segundos
    """ currentime = datetime.now().strftime("%Y%m%d_%H%M%S") # fecha hora actuales, convertimos a String
    file_name = f"Pagina_{currentime}.html"  """
    # Definir el contenido HTML básico
    print(file_name)
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title> TPI SpaceX </title>
</head>
<body>
    """
    # abrimos el archivo
    with open(file_name, "w") as file:
        file.write(html_content)
        file.write(Parser.traductor)
        file.write("</body></html>")

def cerrarVentana():
    ventana.destroy()
    sys.exit()

if __name__ == "__main__":
    
    ventana = tk.Tk()
    ventana.title("Analizador Léxico / Grupo == SpaceX")
    ventana.geometry("800x630")

    # Cuadro de texto sin imagen (ajusta según tus necesidades)
    Ingreso_de_Texto = tk.Text(ventana, width=95, height=33, borderwidth=1.5, relief="solid")
    Ingreso_de_Texto.pack()

    analyze_input_button = tk.Button(ventana, text="Buscar Archivo", command=Buscar_Archivo)
    analyze_input_button.pack()

    # Boton de analizar texto
    analyze_input_button = tk.Button(ventana, text="Analizar Texto", command=Analizador_Texto)
    analyze_input_button.pack()

    # Boton de Salir del lexer
    analyze_input_button = tk.Button(ventana, text="Salir", command=cerrarVentana)
    analyze_input_button.pack()

    output_text = tk.Label(ventana)
    output_text.pack()

    ventana.mainloop()
