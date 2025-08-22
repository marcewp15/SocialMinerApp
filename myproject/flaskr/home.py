from unittest import result
from flask import (
    Blueprint, render_template, request
)

from .auth import login_required
from .db import get_db
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import pandas as pd
import os

#Carga las variables de entorno
load_dotenv()

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return render_template('home/index.html') 

@bp.route('/searcher', methods=('GET', 'POST'))
@login_required
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
    driver = webdriver.Chrome(options=options)

    # Abrir Twitter
    driver.get("https://x.com/")
    driver.maximize_window()
    driver.execute_script("window.focus();")
    print("[INFO] Pagina de inicio de sesion en X cargada.")
    
    WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-testid="loginButton"]'))
        )
    buttonHome = driver.find_element(By.XPATH, value="//a[@data-testid='loginButton']")
    buttonHome.click()
    print("[OK] Boton de login encontrado y selecionado.")
    
    # Iniciar sesion
    input_user = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="text"]'))
        )
    input_user = driver.find_element(By.XPATH, '//input[@name="text"]')
    input_user.send_keys(USERNAME)
    print("[OK] Cuenta usuario ingresado.")

    buttonext = driver.find_element (By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]')
    buttonext.click()
    
    #Ingresar contraseña
    input_pass = WebDriverWait(driver, 50).until(
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
    
    #Escribir el término de búsqueda y presionar Enter
    search_box.send_keys(term)
    search_box.send_keys(Keys.RETURN)
    print(f"[INFO] Realizando busqueda con la palabra:{term}")
    
    ''''
    buttonCloseWelcome = driver.find_element(By.XPATH, value="//a[@data-testid="loginButton"]")
    buttonCloseWelcome.click()
    
    buttonCloseWelcome = driver.find_element(By.XPATH, value="//button[@data-testid='xMigrationBottomBar']")
    buttonCloseWelcome.click()
    '''  
    
    #Seleccionar pagina recientes
    latest = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Latest")]/ancestor::a')))
    latest = driver.find_element(By.XPATH, value= '//span[contains(text(),"Latest")]/ancestor::a')
    latest.click()    
    print("[OK] Selección pestaña 'Recientes' abierta.") 
    
    #Seleccionar usuario
    try:
        tweets = WebDriverWait(driver,20).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="tweetText"]'))
    )
        print(f"[INFO] Se encontraron {len(tweets)} tweets.")
        
        tweets = driver.find_element(By.XPATH, '//article[@data-testid="tweetText"]')
    #Recorre cada tweet
        for tweet in tweets [:10]:
            try:
                user = tweet.find_element(By.XPATH, './/div[@data-testid="User-Name"]').text
                text = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                date = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')
        
                results.append({'user':user, 'text': text, 'date': date})
            
            except Exception as e:
                print("[WARN] No se pudo extraer un tweet:", e)
                
    except Exception as e:
        print("[ERROR] No se encontraron tweets:", e )
    
    
    #Guardar - Recopilar los resultados de la búsqueda
    try:
        with open("tweets_resultados.txt", "w", encoding="utf-8") as f:
            for r in results:
                f.write(f"usuario: {r['user']}\nfecha:{r['date']}\nTweet: {r['text']}\n\n")
            print ("[OK] RESULTADOS GUARDADOS EN TWEETS_RESULTADOS.TXT")
    except Exception as e:
        print ("[ERROR] Ocurrio un problema al guardar:", e)
            
    #finally:
        driver.quit()
        print("[INFO] Navegador cerrado.")
    return results