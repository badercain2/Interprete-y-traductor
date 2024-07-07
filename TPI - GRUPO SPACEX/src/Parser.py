import ply.yacc as yacc
from Lexer import tokens

#Esto permite con slice saver el token de p en el que se encuentra
""" for i, token in enumerate(p):
        if p.slice[i].type == 'nombre': """

def p_sigma(p):
    ''' sigma   :   APERT_LISTA empresas COMA version COMA firmaDigital CIERRE_LISTA
                |   APERT_LISTA empresas COMA firmaDigital COMA version CIERRE_LISTA
                |   APERT_LISTA version COMA firmaDigital COMA empresas CIERRE_LISTA
                |   APERT_LISTA firmaDigital COMA version COMA empresas CIERRE_LISTA
                |   APERT_LISTA firmaDigital COMA empresas COMA version CIERRE_LISTA
                |   APERT_LISTA empresas COMA version CIERRE_LISTA
                |   APERT_LISTA empresas COMA firmaDigital CIERRE_LISTA
                |   APERT_LISTA version COMA empresas CIERRE_LISTA
                |   APERT_LISTA firmaDigital COMA empresas CIERRE_LISTA
                |   APERT_LISTA empresas CIERRE_LISTA '''
    for i, token in enumerate(p):
        if p.slice[i].type == 'empresas':
            global traductor
            traductor = (p[i])

def p_version(p):
    ''' version :   VERSION TEXTO
                |   VERSION VACIO '''
                
def p_firmaDigital(p):
    ''' firmaDigital    :   FIRMA_DIGITAL TEXTO
                        |   FIRMA_DIGITAL VACIO '''

def p_empresas(p):
    ''' empresas    :   EMPRESAS APERT_BLOQUE lista_empresas CIERRE_BLOQUE  '''
    p[0] = p[3]
    
def p_lista_empresas(p):
    ''' lista_empresas  :   APERT_LISTA objeto_empresa CIERRE_LISTA
                        |   APERT_LISTA objeto_empresa CIERRE_LISTA COMA lista_empresas ''' 
    if len(p) == 4:                     
        p[0] = (f'<div style="padding: 20px; border: 1px solid gray; background-color: lightgray;">\n\t{p[2]}</div>')    
    else:
        p[0] = (f'<div style="padding: 20px; border: 1px solid gray; background-color: lightgray;">\n\t{p[2]}</div>') + p[5]       
                        
def p_objeto_empresa(p):
    ''' objeto_empresa  :   nombre_empresa COMA fundacion COMA direccion COMA ingresos_anuales COMA pyme COMA link COMA departamentos
                        |   nombre_empresa COMA fundacion COMA ingresos_anuales COMA pyme COMA link COMA departamentos
                        |   nombre_empresa COMA fundacion COMA direccion COMA ingresos_anuales COMA pyme COMA departamentos
                        |   nombre_empresa COMA fundacion COMA ingresos_anuales COMA pyme COMA departamentos '''
    for i, token in enumerate(p):
        if p.slice[i].type == 'departamentos':
            for j, token in enumerate(p):
                if p.slice[j].type == 'link':
                    p[0] = p[1] + p[j] + p[i]
    
def p_nombre_empresa(p):
    ''' nombre_empresa : NOMBRE_EMPRESA TEXTO '''
    p[0] = (f'<h1>{p[2]}</h1>')

def p_fundacion(p):
    ''' fundacion : FUNDACION FECHA '''

def p_pyme(p):
    ''' pyme : PYME BOOLEANO '''

def p_ingresos_anuales(p):
    ''' ingresos_anuales : INGRESOS_ANUALES FLOTANTE'''

def p_link(p):
    ''' link    :  LINK URL
                |  LINK VACIO '''
    p[2].strip('\"')
    p[0] = f"<a href='{p[2]}'>LINK</a>"




             
def p_direccion(p):
    ''' direccion   :   DIRECCION APERT_LISTA objeto_direccion CIERRE_LISTA
                    |   DIRECCION VACIO '''
    
def p_objeto_direccion(p):
    ''' objeto_direccion    :   calle COMA ciudad COMA pais
                            |   calle COMA pais COMA ciudad
                            |   ciudad COMA pais COMA calle
                            |   ciudad COMA calle COMA pais
                            |   pais COMA ciudad COMA calle
                            |   pais COMA calle COMA ciudad '''
                            #|   calle error ciudad error pais'''

def p_calle(p):
    ''' calle   :   CALLE TEXTO '''

def p_ciudad(p):
    ''' ciudad  :   CIUDAD TEXTO '''

def p_pais(p):
    ''' pais    :   PAIS TEXTO '''
                      
def p_departamentos(p):
    ''' departamentos   :   DEPARTAMENTOS APERT_BLOQUE lista_dpto CIERRE_BLOQUE '''
    p[0] = p[3]
    
def p_lista_dpto(p):
    ''' lista_dpto  :   APERT_LISTA objeto_dpto CIERRE_LISTA
                    |   APERT_LISTA objeto_dpto CIERRE_LISTA COMA lista_dpto '''
    if len(p) == 4:
        p[0] = p[2]    
    else:
        p[0] = p[2] + p[5]
                    
def p_objeto_dpto(p):
    ''' objeto_dpto :   nombre COMA jefe COMA sub_dptos
                    |   nombre COMA sub_dptos COMA jefe
                    |   jefe COMA sub_dptos COMA nombre
                    |   jefe COMA nombre COMA sub_dptos
                    |   sub_dptos COMA nombre COMA jefe
                    |   sub_dptos COMA jefe COMA nombre
                    |   nombre COMA sub_dptos
                    |   sub_dptos COMA nombre '''
    for i, token in enumerate(p):
        if p.slice[i].type == 'nombre':
            for j, token in enumerate(p):
                if p.slice[j].type == 'sub_dptos':
                    if i < j:
                        p[0] = (f'<h2>{p[i]}</h2>{p[j]}')
                    else:
                        p[0] = (f'{p[j]}<h2>{p[i]}</h2>')
            

def p_sub_dptos(p):
    ''' sub_dptos   :   SUBDEPARTAMENTOS APERT_BLOQUE lista_sub_dpto CIERRE_BLOQUE '''
    p[0] = p[3]
    
def p_lista_sub_dpto(p):
    ''' lista_sub_dpto  :   APERT_LISTA objeto_sub_dpto CIERRE_LISTA 
                        |   APERT_LISTA objeto_sub_dpto CIERRE_LISTA COMA lista_sub_dpto '''
    if len(p) == 4:
        p[0] = p[2]    
    else:                               
        p[0] = p[2] + p[5]

def p_objeto_sub_dpto(p):
    ''' objeto_sub_dpto :   nombre COMA jefe COMA empleados
                        |   nombre COMA jefe
                        |   nombre COMA empleados
                        |   nombre
                        |   jefe COMA nombre COMA empleados
                        |   jefe COMA empleados COMA nombre
                        |   empleados COMA jefe COMA nombre
                        |   empleados COMA nombre COMA jefe
                        |   jefe COMA nombre
                        |   empleados COMA nombre '''
    pos_emple = 0
    for i, token in enumerate(p):       #Este bucle verifica que venga empleados y a su vez marca las posiciones en las que se encuentran
        if p.slice[i].type == 'nombre':
            pos_nom = i
        if p.slice[i].type == 'empleados':
            pos_emple = i
            
    if pos_emple != 0:
        if pos_nom < pos_emple:
            p[0] = (f'<h3>{p[pos_nom]}</h3>{p[pos_emple]}')
        else:
            p[0] = (f'{p[pos_emple]}<h3>{p[pos_nom]}</h3>')
    else:
        p[0] = (f'<h3>{p[pos_nom]}</h3>')
                        
def p_empleados(p):
    ''' empleados   :   EMPLEADOS APERT_BLOQUE lista_empleados CIERRE_BLOQUE
                    |   EMPLEADOS VACIO '''
    if len(p) == 5:
        p[0] = (f'<ul>{p[3]}</ul>')
    else:
        p[0] = ('<ul></ul>')

def p_lista_empleados(p):
    ''' lista_empleados :   APERT_LISTA objeto_empleados CIERRE_LISTA
                        |   APERT_LISTA objeto_empleados CIERRE_LISTA COMA lista_empleados '''
    if len(p) == 4:
        p[0] = p[2]    
    else:
        p[0] = p[2] + p[5]
    
def p_objeto_empleados(p):
    ''' objeto_empleados    :   nombre COMA edad COMA cargo COMA salario COMA activo COMA fecha_contratacion COMA proyectos
                            |   nombre COMA edad COMA cargo COMA salario COMA activo COMA fecha_contratacion
                            |   nombre COMA cargo COMA salario COMA activo COMA fecha_contratacion COMA proyectos
                            |   nombre COMA cargo COMA salario COMA activo COMA fecha_contratacion '''
    pos_proye = 0
    for i, token in enumerate(p):
        if p.slice[i].type == 'proyectos':
            pos_proye = i
    
    if pos_proye != 0:
        p[0] = (f'<li>{p[1]}</li>{p[pos_proye]}')
    else:
        p[0] = (f'<li>{p[1]}</li>')
    
def p_proyectos(p):
    ''' proyectos   :   PROYECTOS APERT_BLOQUE lista_proyectos CIERRE_BLOQUE
                    |   PROYECTOS VACIO '''
    if len(p) == 5:
        p[0] = p[3]
    else:
        p[0] = p[2]

def p_lista_proyectos(p):
    ''' lista_proyectos :   APERT_LISTA objeto_proyecto CIERRE_LISTA
                        |   APERT_LISTA objeto_proyecto CIERRE_LISTA COMA lista_proyectos '''
    if len(p) == 4:
        titulo = (f'<table><thead><tr><th> NOMBRE </th><th> ESTADO </th><th> FECHA INICIO </th><th> FECHA FIN </th></tr></thead><tbody>')
        p[0] = (f'{titulo}{p[2]}</tbody></table>')    
    else:
        p[0] = p[2] + p[5]

def p_objeto_proyecto(p):
    ''' objeto_proyecto :   nombre COMA estado COMA fecha_inicio COMA fecha_fin
                        |   nombre COMA fecha_inicio COMA fecha_fin
                        |   nombre COMA estado COMA fecha_inicio
                        |   nombre COMA fecha_inicio '''
    if len(p) == 8:
        p[0] = (f'<tr><td>{p[1]}</td><td>{p[3]}</td><td>{p[5]}</td><td>{p[7]}</td></tr>\n')
    elif len(p) == 6:
        p[0] = (f'<tr><td>{p[1]}</td><td>{p[3]}</td><td>{p[5]}</td></tr>\n')
    elif len(p) == 4:
        p[0] = (f'<tr><td>{p[1]}</td><td>{p[3]}</td></tr>\n')
    
def p_nombre(p):
    ''' nombre  :   NOMBRE TEXTO '''
    p[2] = p[2].strip("\"")
    p[0] = (f'{p[2]}')

    
def p_jefe(p):
    ''' jefe    :   JEFE TEXTO
                |   JEFE VACIO '''

def p_edad(p):
    ''' edad    :   EDAD NUMERO 
                |   EDAD VACIO '''

def p_cargo(p):
    ''' cargo   :   CARGO TEXTO_RESTRINGIDO_CARGO '''

def p_salario(p):
    ''' salario :   SALARIO FLOTANTE '''

def p_activo(p):
    ''' activo  :   ACTIVO BOOLEANO '''

def p_fecha_contratacion(p):
    ''' fecha_contratacion :   FECHA_CONTRATACION FECHA '''

def p_estado(p):
    ''' estado  :   ESTADO TEXTO_RESTRINGIDO_ESTADO
                |   ESTADO VACIO '''
    p[2] = p[2].strip('\"')
    p[0] = (f'{p[2]}')

def p_fecha_inicio(p):
    ''' fecha_inicio    :   FECHA_INICIO FECHA '''
    p[2] = p[2].strip('\"')
    p[0] = (f'{p[2]}')

def p_fecha_fin(p):
    ''' fecha_fin   :   FECHA_FIN FECHA
                    |   FECHA_FIN VACIO '''
    p[2] = p[2].strip('\"')
    p[0] = (f'{p[2]}')

diccionario_errores_parser = {}

def p_error(p):
    if p:
        diccionario_errores_parser[str(p.value)] = str(p.lineno)

parser = yacc.yacc(start='sigma') # empieza a evaluar