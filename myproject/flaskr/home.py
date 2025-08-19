from flask import (
    Blueprint, render_template, request
)

from flaskr.auth import login_required
from flaskr.db import get_db
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
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
    
    "try:"
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
    
    buttonLogin = driver.find_element(By.XPATH, value="//button[@data-testid='LoginForm_Login_Button']")
    buttonLogin.click()
    print("[OK] Sesion iniciada.")
    
    #Campo de Busqueda
    search_box = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]'))
    )
    #Encontrar el campo de búsqueda
    search_box = driver.find_element (By.XPATH, value='//input[@data-testid="SearchBox_Search_Input"]')
    # Escribir el término de búsqueda y presionar Enter
    search_box.send_keys(term)
    search_box.send_keys(Keys.RETURN)
    print(f"[INFO] Realizando busqueda con la palabra:{term}")
    
    ''''
    buttonCloseWelcome = driver.find_element(By.XPATH, value="//a[@data-testid="loginButton"]")
    buttonCloseWelcome.click()
    
    buttonCloseWelcome = driver.find_element(By.XPATH, value="//button[@data-testid='xMigrationBottomBar']")
    buttonCloseWelcome.click()
    '''     ''''
    # Seleccionar pagina recientes
    #latest = WebDriverWait(driver, 20).until(
     #   EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div'))
    #)
    #latest = driver.find_element (By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div')
    #latest.click()
    #print("[OK] Selección pestaña 'Recientes' abierta.") 
     '''
    # Seleccionar pagina recientes
    latest = WebDriverWait(driver, 20).until(
           EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"Latest")]/ancestor::a'))
       )
    latest = driver.find_element(By.XPATH, value= '//span[contains(text(),"Latest")]/ancestor::a')
    latest.click()    
    print("[OK] Selección pestaña 'Recientes' abierta.") 
    
    #Seleccionar usuario
    ''''
    UserTag = WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-testid="User-Name"]//a//span'))
    ).text
    UserTag = driver.find_element(By.XPATH, '//div[@data-testid="User-Name"]//a//span').text
    print("Usuario:", UserTag )
    tweet = driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]').text
    date = driver.find_element(By.XPATH, './/time').get_attribute('datetime')
    '''
    try:
        tweets = WebDriverWait(driver,20).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="tweetText"]'))
    )
        print(f"[INFO] Se encontraron {len(tweets)} tweets.")
    
        for tweet in tweets [:10]:
            try:
                user = driver.find_element(By.XPATH, '//div[@data-testid="User-Name"]').text
                results.append(user)
                text = driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]').text
                results.append(text)
                date = driver.find_element(By.XPATH, './/time').get_attribute('datetime')
                results.append(date)
            
                "results.append({'user':user, 'text': text, 'date': date})"
            
            except Exception as e:
                print("[WARN] No se pudo extraer un tweet:", e)
                
    except Exception as e:
        print("[ERROR] Nose encontraron tweets:", e )
    
    #Guardar
    try:
        with open("tweets_resultados.txt", "w", encoding="utf-8") as f:
            for r in results:
                f.write(f"usuario: {r['user']}\nfecha:{r['date']}\nTweet: {r['text']}\n\n")
            print ("[OK] RESULTADOS GUARDADOS EN TWEETS_RESULTADOS.TXT")
    except Exception as e:
        print ("[ERROR] Ocurrio un problema al guardar:", e)
            
    #################
    users=[]
    texts=[]
    dates=[]
    tweets = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
    print(f"[INFO] Se encontraron {len(tweets)} tweets.")
while True:
    for tweet in tweets :
            user = driver.find_element(By.XPATH, './/div[@data-testid="User-Name"]').text
            users.append(user)
            text = driver.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
            texts.append(text)
            date = driver.find_element(By.XPATH, './/time').get_attribute('datetime')
            dates.append(date)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    tweets = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
    texts2 = list(set(tweets))
    if len(texts2) > 5:
        break
print(len(users),
     len(texts),
     len(dates))

import pandas as pd

df = pd.DataFrame(zip(users, texts, dates)
                  ,columns=['users','texts','dates'])
df.head()

df.to_excel(r"C:\Users\aleja\Documents\PROYECTO GRADO\resultados.txt", index=False)
import os
os.system('start "excel""C:\Users\aleja\Documents\PROYECTO GRADO" ')
       
                
''''
    #Guardar
    try:
        with open("tweets_resultados.txt", "w", encoding="utf-8") as f:
            for r in results:
                f.write(f"usuario: {r['user']}\nfecha:{r['date']}\nTweet: {r['text']}\n\n")
            print ("[OK] RESULTADOS GUARDADOS EN TWEETS_RESULTADOS.TXT")
    except Exception as e:
        print ("[ERROR] Ocurrio un problema al guardar:", e)
'''

    #WebDriverWait(driver, 10).until(
     #       EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweet"]'))
       # )
    
    #WebDriverWait(driver, 10).until(
     #       EC.presence_of_element_located((By.XPATH, '//a[@data-testid=loginButton"]'))
      #  )#
    
    # Recopilar los resultados de la búsqueda
''''
    tweets = driver.find_elements(By.XPATH, '//div[@data-testid="tweet"]')
    for tweet in tweets:
            user = tweet.find_element(By.XPATH, './/span[contains(@class, "css-901oao css-16my406")]').text
            text = tweet.find_element(By.XPATH, './/div[contains(@class, "css-901oao r-18jsvk2 r-1tl8opc r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")]').text
            date = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')
            results.append({'user': user, 'text': text, 'date': date})
    '''
#except NoSuchElementException as e:
    # Manejar excepciones y errores
#    print("Error: Elemento no encontrado:", e)
#finally:
driver.quit() 
    return results