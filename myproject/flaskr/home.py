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
    
    USERNAME = "socialminer035"
    PASSWORD = "Proyecto2025/*"
    
    "try:"
    # Inicializar el controlador de Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    # Abrir Twitter
    driver.get("https://x.com/")
    driver.maximize_window()
    driver.execute_script("window.focus();")
    
    WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-testid="loginButton"]'))
        )
    buttonHome = driver.find_element(By.XPATH, value="//a[@data-testid='loginButton']")
    buttonHome.click()
    
    # Iniciar sesion
    input_user = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, '//input[@name="text"]'))
        )
    input_user = driver.find_element(By.XPATH, '//input[@name="text"]')
    input_user.send_keys(USERNAME)    

    buttonext = driver.find_element (By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]')
    buttonext.click()
    
    #Ingresar contraseña
    
    input_pass = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
    )
    input_pass = driver.find_element (By.XPATH, '//input[@name="password"]')
    input_pass.send_keys(PASSWORD)
    
    buttonLogin = driver.find_element(By.XPATH, value="//button[@data-testid='LoginForm_Login_Button']")
    buttonLogin.click()
    
    #Campo de Busqueda
    search_box = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]'))
    )
    search_box = driver.find_element (By.XPATH, value='//input[@data-testid="SearchBox_Search_Input"]')
    search_box.send_keys(term)
    search_box.send_keys(Keys.RETURN)
    
    
    ''''
    buttonCloseWelcome = driver.find_element(By.XPATH, value="//a[@data-testid="loginButton"]")
    buttonCloseWelcome.click()
    
    buttonCloseWelcome = driver.find_element(By.XPATH, value="//button[@data-testid='xMigrationBottomBar']")
    buttonCloseWelcome.click()
    '''
    
    # Encontrar el campo de búsqueda
    search_box = driver.find_element_by_xpath('//input[@aria-label="Buscar en Twitter"]')

    # Escribir el término de búsqueda y presionar Enter
    search_box.send_keys(term)
    search_box.send_keys(Keys.RETURN)
    
    # Seleccionar pagina recientes
    #sleep (3)
    #latest = driver.find_element(By.XPATH, "//span[contains(text(), 'Latest')]")
    #latest.click()
    
    latest = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Latest"]'))
        )
    latest = driver.find_element(By.XPATH, value= '//span[contains(text(), "Latest"]')
    latest.click()    
    
    user = driver.find_element(By.XPATH, '//div[@data-testid="User-Name"]').text
    tweet = driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]').text
    date = driver.find_element(By.XPATH, './/time').get_attribute('datetime')

    #WebDriverWait(driver, 10).until(
     #       EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweet"]'))
       # )
    
    #WebDriverWait(driver, 10).until(
     #       EC.presence_of_element_located((By.XPATH, '//a[@data-testid=loginButton"]'))
      #  )#
    
    # Recopilar los resultados de la búsqueda
    
    tweets = driver.find_elements(By.XPATH, '//div[@data-testid="tweet"]')
    for tweet in tweets:
            user = tweet.find_element(By.XPATH, './/span[contains(@class, "css-901oao css-16my406")]').text
            text = tweet.find_element(By.XPATH, './/div[contains(@class, "css-901oao r-18jsvk2 r-1tl8opc r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")]').text
            date = tweet.find_element(By.XPATH, './/time').get_attribute('datetime')
            results.append({'user': user, 'text': text, 'date': date})

#except NoSuchElementException as e:
    # Manejar excepciones y errores
#    print("Error: Elemento no encontrado:", e)
#finally:
    driver.quit() 

    return results