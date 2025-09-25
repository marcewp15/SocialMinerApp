from unittest import result
from flask import (
    Blueprint, render_template, request, send_file
)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from dotenv import load_dotenv
import pandas as pd
import os


#Carga las variables de entorno
load_dotenv()

#Definicion del blueprint 
bp = Blueprint('home', __name__)

#Ruta principal del blueprint 
@bp.route('/')
def index():
    return render_template('home/index.html') 

@bp.route('/searcher', methods=('GET', 'POST'))
def searcher():
    term = request.form['term']
    results = search_x(term)

    return render_template('home/index.html', results=results)

def search_x(term):
    results = []
    print(f"[INFO] Iniciando busqueda en X para la palabra :{term}")
    
    USERNAME = os.getenv("TWITTER_USERNAME")
    PASSWORD = os.getenv("TWITTER_PASSWORD")
    
    # Inicializar el controlador de Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    #Filtar logs de chrome
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #solo se filtran errores graves 0=ALL, 3=ERROR
    options.add_argument("--log-level=3",)
    
    driver = webdriver.Chrome(options=options)

    # Abrir Twitter
    driver.get("https://x.com/")
    driver.maximize_window()
    driver.execute_script("window.focus();")
    print("[INFO] Pagina de inicio de sesion en X cargada.")
    
    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-testid="loginButton"]'))
        )
    buttonHome = driver.find_element(By.XPATH, value="//a[@data-testid='loginButton']")
    buttonHome.click()
    print("[OK] Boton de login encontrado y selecionado.")
    
    #En caso de que aparezca la pestaña de bienvenida
    ''''
    buttonCloseWelcome = driver.find_element(By.XPATH, value="//a[@data-testid="loginButton"]")
    buttonCloseWelcome.click()
    
    buttonCloseWelcome = driver.find_element(By.XPATH, value="//button[@data-testid='xMigrationBottomBar']")
    buttonCloseWelcome.click()
    '''  
    
    # Iniciar sesion
    input_user = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="text"]'))
        )
    input_user = driver.find_element(By.XPATH, '//input[@name="text"]')
    input_user.send_keys(USERNAME)
    print("[OK] Cuenta usuario ingresado.")

    buttonext = driver.find_element (By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]')
    buttonext.click()
    
    #Ingresar contraseña
    input_pass = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
    )
    input_pass = driver.find_element (By.XPATH, '//input[@name="password"]')
    input_pass.send_keys(PASSWORD)
    print("[OK] Contraseña de usuario ingresada.")
    
    #Boton de logueo 
    buttonLogin = driver.find_element(By.XPATH, value="//button[@data-testid='LoginForm_Login_Button']")
    buttonLogin.click()
    print("[OK] Sesion iniciada.")
    
    #Encontrar el campo de búsqueda
    search_box = WebDriverWait(driver,10).until(
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
    max_tweets = 20 #Cantidad de tweets a seleccionar
        
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
    
    #Guardar - los resultados de la búsqueda en archivo .TXT
    df = pd.DataFrame(results)
    
    df.to_csv('tweets_resultados.txt', sep="\t", index=False, encoding="utf-8")
    print (f"[OK]{len(results)} RESULTADOS GUARDADOS EN TWEETS_RESULTADOS.TXT")
    
    #finally:
    try:
        driver.quit()
        print("[INFO] Navegador cerrado.")
    except: 
        print("[WARN] No se pudo cerrar el navegador")
    return results

#Boton Exportar
@bp.route('/download')
def download_file_pd():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    path = os.path.join(base_dir, 'tweets_resultados.txt')
    return send_file(path, as_attachment=True, download_name='tweets_resultados.txt', mimetype='text/plain')