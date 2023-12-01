from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#unaopcion_para_enviar_msj_al_Wsp_(no usada)
import pywhatkit
#control local
import keyword
import pyautogui as pa
#numero o valor aleatorio
import random
#retraso
import time
#libreria_tiempo y suma de tiempo a la hora actual
from datetime import datetime, timedelta
import pytz
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import hashlib
import random
import string
import re
import pandas as pd
import pyodbc
import sqlalchemy
############################################################################################################################
#### INSTANCIA PRINCIPAL DE CHROME ###
# Crear una instancia de ChromeOptions----------------------
options = Options()
# Agregar la ruta de la extensión a las opciones de Chrome--
options.add_argument("C:\Automatizacion_PYTHON_ENTORNO_IMG\BOT_LLENADO_SQL_VR\CHROME_EXT_EXE\chromedriver.exe")
# Abrir el navegador completo-------------------------------
options.add_argument("--start-maximized")
# Inicializar el controlador de Chrome con las opciones-----
############################################################################################################################
############################################################################################################################
############################################################################################################################

############################################################################################################################
############################################################################################################################
############################################################################################################################
############################################################################################################################
#####################################################ENVIO_WSP###

#################################### INSTANCIA SECUNDARIA DE CHROME PARA WSP__inicio##########################################

# Ruta al perfil de Chrome que deseas utilizar(dependencia_aparte)
profile_path = r"C:\Users\Orlando\AppData\Local\Google\Chrome\User Data\Default"

# Configurar las opciones del navegador para utilizar el perfil
options.add_argument("--user-data-dir=" + profile_path)

# Reutilizar la instancia de Chrome con el perfil seleccionado(Profile 1)
driver = webdriver.Chrome(options=options)
time.sleep(5)

#################################### INSTANCIA SECUNDARIA DE CHROME PARA WSP__fin##########################################

#Seleccion_link
driver.get("https://web.whatsapp.com/")
time.sleep(30)
# ...

# Seleccionar la barra buscadora de wsp y buscar el nombre del grupo
Click_wsp = driver.find_element(By.CSS_SELECTOR, "div._3gYev > div > div._1EUay > div._2vDPL > div > div.to2l77zo.gfz4du6o.ag5g9lrv.bze30y65.kao4egtt.qh0vvdkp > p")
Click_wsp.click()
# Name_grup
Click_wsp.send_keys("equipo")
Click_wsp.send_keys(Keys.ENTER)
time.sleep(20)  # Asegurarse de que el chat se cargue completamente
# Crear una instancia de ActionChains

Click_wsp = driver.find_element(By.XPATH, '//*[@id="main"]')
Click_wsp.click()
time.sleep(3)

actions = ActionChains(driver)

# Desplazar hacia arriba el contenedor del chat
for _ in range(10): # Puedes ajustar el número de veces que quieres hacer scroll
    actions.key_down(Keys.CONTROL).send_keys(Keys.HOME).key_up(Keys.CONTROL).perform()
    time.sleep(2) # Pausa 
time.sleep(15)

#decarga de conversacion
chat_container = driver.find_element(By.XPATH, '//*[@id="main"]')

# Extrae el texto del chat
chat_text = chat_container.text


# Cierra el navegador
driver.quit()

# Guarda el texto del chat en un archivo
with open('chat_whatsapp.txt', 'w', encoding='utf-8') as file:
    file.write(chat_text)

# Nombre del archivo original de WhatsApp
nombre_original = 'chat_whatsapp.txt'

# Nombre del archivo FINAL_DE_WSP
solo_inc = 'INC.TXT'


time.sleep(3)
# Abre el archivo 'solo_inc' en modo lectura para obtener las palabras ya copiadas
palabras_previas = set()
try:
    with open(solo_inc, 'r', encoding='utf-8') as archivo_inc:
        palabras_previas = set(linea.strip() for linea in archivo_inc)
except FileNotFoundError:
    pass

# Abre el nuevo archivo en modo lectura
with open(nombre_original, 'r', encoding='utf-8') as archivo_nuevo:
    # Inicializa un conjunto para almacenar palabras que comienzan con "INC" y no están en palabras_previas
    nuevas_palabras_inc = set()

    # Itera sobre cada línea en el archivo nuevo
    for linea in archivo_nuevo:
    # Busca palabras que comienzan con "INC" en cada línea y que sigan el formato deseado (por ejemplo, INC seguido de números)
        nuevas_palabras_inc.update(palabra.strip('.,!?()[]{}') for palabra in linea.split() if re.match(r'INC\d+', palabra))


# Filtra solo las palabras que no han sido copiadas previamente
nuevas_palabras_inc = nuevas_palabras_inc - palabras_previas

# Abre el archivo 'solo_inc' en modo escritura y agrega las nuevas palabras que comienzan con "INC"
with open(solo_inc, 'a', encoding='utf-8') as archivo_inc:
    for nueva_palabra_inc in nuevas_palabras_inc:
        archivo_inc.write(f'{nueva_palabra_inc}\n')

print(f'Se han extraído y guardado las nuevas palabras que comienzan con "INC" en: {solo_inc}')

time.sleep(3)

# Parámetros de conexión a la base de datos
server = 'conexion_bd-ip'
database = 'name_bd'
username = 'user'
password = 'contra'
driver = '{SQL Server}'

# Crear una conexión a la base de datos
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Leer el contenido de INC.TXT
solo_inc_file = 'INC.TXT'
with open(solo_inc_file, 'r', encoding='utf-8') as file:
    content = file.readlines()

# Eliminar los saltos de línea y espacios adicionales
content = [line.strip() for line in content]

# Definir valores por defecto para las otras columnas
valor_por_defecto1 = 'URGENTE'
valor_por_defecto2 = 'PRIMERA_LINEA'

# Realizar la inserción en la base de datos
table_name = 'ALMACEN_INC_URG'  # Cambia a tu nombre de tabla
column_name_TIPO = 'TIPO'  
column_name_INC = 'TK' ##VIENE DEL TXT
column_name_GRP = 'GRP_REPORTADO'
column_name_HORA = 'HORA_SYS'

hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Iterar sobre las líneas del archivo y realizar la inserción si no existe
for line in content:
    # Asegurarse de que la línea no esté vacía antes de insertar
    if line:
        # Verificar si el valor ya existe en la tabla
        query_exists = f"SELECT 1 FROM {table_name} WHERE {column_name_INC} = ?"
        cursor.execute(query_exists, line)
        row = cursor.fetchone()

        if not row:
            # El valor no existe, realizar la inserción con la hora actual
            query_insert = f"INSERT INTO {table_name} ({column_name_TIPO}, {column_name_INC}, {column_name_GRP}, {column_name_HORA}) VALUES " \
                           f"(?, ?, ?, CONVERT(datetime, ?, 120))"
            cursor.execute(query_insert, valor_por_defecto1, line, valor_por_defecto2, hora_actual)
# Confirmar la transacción
conn.commit()

# Cerrar la conexión
conn.close()

print(f'Se han insertado los datos en la columna {column_name_INC} de la tabla {table_name}.')
