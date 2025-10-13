from unittest import result
from flask import (
    Blueprint, render_template, request, send_file, flash, redirect, url_for
)
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from dotenv import load_dotenv
import pandas as pd
#import tempfile
import os
import re

# Inicia un servidor X virtual (Xvfb) para simular entorno gráfico y permitir que Chrome funcione sin modo headless en servidores cloud
#os.system("Xvfb :99 -screen 0 1920x1080x24 &")
#os.environ["DISPLAY"] = ":99"

#Carga las variables de entorno
load_dotenv()

#Definicion del blueprint 
bp = Blueprint('home', __name__)

#Ruta principal del blueprint 
@bp.route('/')
def index():
    return render_template('home/index.html', results=None) 

@bp.route('/searcher', methods=('GET', 'POST'))
def searcher():
    term = request.form['term'].strip()
    
    if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', term):
        flash("Solo se permiten letras en la busqueda", "error")
        return redirect(url_for('home.index'))
    try:
        results = search_x(term)
        if not results:
            flash("No se encontraron tweets para esta palabra clave", "warning")
        return render_template('home/index.html', results=results, term=term)
    except Exception as e:
        flash(f"Ocurrio un error en la busqueda: {str(e)}","error")
        return redirect(url_for('home.index'))
        
def search_x(term):
    results = []
    print(f"[INFO] Iniciando busqueda en X para la palabra :{term}")
    
    USERNAME = os.getenv("TWITTER_USERNAME")
    PASSWORD = os.getenv("TWITTER_PASSWORD")
    
    # Inicializar el controlador de Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Crear un directorio temporal único para el perfil de usuario y evitar errores de sesión
    #user_data_dir = tempfile.mkdtemp()
    #options.add_argument(f"--user-data-dir={user_data_dir}")

    """
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-sync")
    options.add_argument("--enable-unsafe-swiftshader")
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")  # Nivel de verbo para logs (1 es básico)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    """

    # *Agrega esta línea para los logs*
    #options.set_capability('goog:loggingPrefs', {'browser': 'ALL', 'driver': 'ALL'})

    #options.add_argument("--remote-debugging-port=9222")

    # Configura el servicio para usar chromedriver del sistema
    #service = Service("/usr/bin/chromedriver")

    #Filtar logs de chrome
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #solo se filtran errores graves 0=ALL, 3=ERROR
    options.add_argument("--log-level=3",)
    UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument(f"--user-agent={UA}")
    driver = webdriver.Chrome(options=options)

    # Abrir X
    #driver.get("https://x.com/")
    driver.get("https://x.com/i/flow/login")
    driver.maximize_window()
    driver.execute_script("window.focus();")
    print("[INFO] Pagina de inicio de sesion en X cargada.")
    
    
    #En caso de que aparezca la pestaña de bienvenida
    ''''
    buttonCloseWelcome = driver.find_element(By.XPATH, value="//a[@data-testid="loginButton"]")
    buttonCloseWelcome.click()
    
    buttonCloseWelcome = driver.find_element(By.XPATH, value="//button[@data-testid='xMigrationBottomBar']")
    buttonCloseWelcome.click()
    '''  
    
    #Ventana de logueo X    
    """ buttonHome = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-testid="loginButton"]'))
        )
    buttonHome = driver.find_element(By.XPATH, value="//a[@data-testid='loginButton']")
    buttonHome.click()
    print("[OK] Boton de login encontrado y selecionado.") """
    
    # Iniciar sesion
    input_user = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="text"]'))
        )
    #input_user = driver.find_element(By.XPATH, '//input[@name="text"]')
    input_user.click()
    
    #input_user.send_keys(USERNAME)
    escribir_lento_actions(driver, input_user, USERNAME, False)
    print("[OK] Cuenta usuario ingresado.")
    
    #buttonext = driver.find_element (By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]')
    buttonext = driver.find_element (By.XPATH, "//span[contains(text(),'Siguiente')]/ancestor::button")
    time.sleep(random.uniform(*(0.08, 0.18)))
    buttonext.click()

    """
    try:
        buttonext = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Siguiente')]]"))
        )
        buttonext = driver.find_element(By.XPATH, "//button[.//span[contains(text(), 'Siguiente')]]")
        driver.execute_script("arguments[0].scrollIntoView(true);", buttonext)
        time.sleep(0.5)
        buttonext.click()
        print("[OK] Boton de siguiente encontrado y selecionado.")
    except Exception as e:
        print(f"[ERROR] No se pudo hacer clic en 'Siguiente': {e}")
        #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    """
    #Ingresar contraseña
    input_pass = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
    )
    #input_pass = driver.find_element (By.XPATH, '//input[@name="password"]')
    #input_pass.send_keys(PASSWORD)
    escribir_lento_actions(driver, input_pass, PASSWORD, False)

    print("[OK] Contraseña de usuario ingresada.")
    
    #Boton de logueo 
    buttonLogin = driver.find_element(By.XPATH, value="//button[@data-testid='LoginForm_Login_Button']")
    time.sleep(random.uniform(*(0.08, 0.18)))
    buttonLogin.click()
    print("[OK] Sesion iniciada.")


    """
    buttonLogin = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='LoginForm_Login_Button']"))
    )
    #buttonLogin = driver.find_element(By.XPATH, value="//button[@data-testid='LoginForm_Login_Button']")
    buttonLogin.click()
    print("[OK] Sesion iniciada.")

    # Captura y muestra logs de Chrome
    try:
        logs = driver.get_log('browser')
        for entry in logs:
            print(f"[CHROME LOG] {entry['level']}: {entry['message']}")
    except Exception:
        pass
    
    logs_driver = driver.get_log('driver')
    for entry in logs_driver:
        print(f"[CHROME DRIVER LOG] {entry['level']}: {entry['message']}")
    """
    
    #Encontrar el campo de búsqueda
    """ search_box = WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]'))
    )
    search_box = driver.find_element (By.XPATH, value='//input[@data-testid="SearchBox_Search_Input"]')
    
    #Escribir el palabra de búsqueda y presionar Enter
    search_box.send_keys(term)
    search_box.send_keys(Keys.RETURN)
    print(f"[INFO] Realizando busqueda con la palabra:{term}")
    
    #Seleccionar pagina recientes
    latest = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Latest")]/ancestor::a')))
    latest = driver.find_element(By.XPATH, value= '//span[contains(text(),"Latest")]/ancestor::a')
    latest.click()    
    print("[OK] Selección pestaña 'Recientes' abierta.") 
    
    #Seleccionar tweets con la palabra de busqueda
    results = []
    max_tweets = 10 #Cantidad de tweets a seleccionar
        
    try:
        while len(results) < max_tweets:
                #Espera a que aparezcan tweets completos
                tweets = WebDriverWait(driver,20).until(
                EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid="tweet"]'))
                )
                print(f"[INFO] Se encontraron {len(tweets)} tweets en pantalla.")
        
                #Recorre cada tweet
                for tweet in tweets:
                    if len(results) >= max_tweets:
                        break
                    try:
                        user = tweet.find_element(By.XPATH, './/div[@data-testid="User-Name"]').text
                        text = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                        date = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')
                        
                        #Evitar duplicados
                        if not any(r["text"] == text and r["date"] == date for r in results):
                            results.append({'user':user, 'text': text, 'date': date})
                            
                    #Evita los tweets que contengan imagenes, videos o retweets 
                    except (StaleElementReferenceException,NoSuchElementException):
                        print("[WARM] Tweet descartado por stale element")
                        continue
                    except Exception as e:
                        print("[WARN] No se pudo extraer un tweet:", e)
                        continue
                        
                #Se genera un scroll para cargar más tweets
                if len(results) < max_tweets:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    
    except Exception as e:
        print("[ERROR] No se encontraron tweets:", e )
        flash("No se encontraron tweets para esta palabra clave", "warning")
    
    #Guardar - los resultados de la búsqueda en archivo .TXT
    try:
        df = pd.DataFrame(results)
        df.to_csv('tweets_resultados.txt', sep="\t", index=False, encoding="utf-8")
        print (f"[OK]{len(results)} RESULTADOS GUARDADOS EN TWEETS_RESULTADOS.TXT")
    except Exception:
        flash("No fue posible exportar los resultados", "error")

    #finally:
    try:
        driver.quit()
        print("[INFO] Navegador cerrado.")
    except: 
        print("[WARN] No se pudo cerrar el navegador")
    return results """

#Boton Exportar
@bp.route('/export')
def export_file_pd():
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        path = os.path.join(base_dir, 'tweets_resultados.txt')
        
        if not os.path.exists(path):
            flash("No hay resultados disponibles para exportar.")
            return redirect(url_for('home.index(value)'))
        return send_file(path, as_attachment=True, download_name='tweets_resultados.txt', mimetype='text/plain')
    
    except Exception as e:
        flash("No fue posible exportar los resultados","error")
        print("[ERROR] Exportación fallida:", e)
        return redirect(url_for('home.index'))
    

def escribir_lento_actions(driver, elemento, texto, limpiar=True, delay=(0.08, 0.18)):
    actions = ActionChains(driver)
    elemento.click()

    """ if limpiar:
        from selenium.webdriver.common.keys import Keys
        import platform
        is_mac = platform.system() == "Darwin"
        actions.key_down(Keys.COMMAND if is_mac else Keys.CONTROL).send_keys("a").key_up(Keys.COMMAND if is_mac else Keys.CONTROL)
        actions.send_keys(Keys.DELETE) """

    for ch in texto:
        actions.send_keys_to_element(elemento, ch).pause(random.uniform(*delay))
        actions.perform()

# --- Ejemplo de uso ---
# escribir_lento_actions(driver, input_box, "Hola mundo", limpiar=True, delay=(0.06, 0.14))
