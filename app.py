import time
import os

import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# custom package
import auxiliar as aux

# get work folder
workFolder=os.path.abspath(os.getcwd())

# load target projects list
workFile=pd.read_excel(workFolder+'\\concursosList.xlsx')
downloadFolder=workFolder+'\\downloads'

# set browser driver config
chromedriver=r"./assets/drive/chromedriver.exe"
chrome_options = Options()
prefs = {'download.default_directory' : downloadFolder}
chrome_options.add_experimental_option('prefs', prefs)

driver=webdriver.Chrome(executable_path=chromedriver,options=chrome_options)

# minimize browser window
driver.set_window_position(-10000, 0)

# set waiter to wait for webpages to be loaded
seleWaiter = WebDriverWait(driver,10)

# go to APIexplorer webpage
driver.get("https://servicios.conicyt.cl/#/private/panels")

# click and show login form
element = seleWaiter.until(EC.element_to_be_clickable(((By.XPATH,"/html/body/div/conicyt-header/md-content/md-toolbar/div/div[3]/button"))))
element.click()

# show up the browser window
driver.set_window_position(0, 0)
driver.maximize_window()

# wait for the user to login
print("Ingresa tus credenciales y autentifícate...")

# and keep waiting for the log
try:
    while True:
        try:
            # check if the new form is loaded
            element=driver.find_element_by_xpath("/html/body/div/conicyt-header/md-content/md-toolbar/div/div[3]/md-menu/button")
            element.click()

            # if it loaded then hide again
            driver.set_window_position(-10000, 0)
            break
        except:
            time.sleep(1)

    # selecciona la opción de la API con la información de postulación
    # 
    w=WebDriverWait(driver,5)
    element = driver.find_element_by_xpath("//*[@id='menu_container_0']/md-menu-content/md-menu-item[1]/button")
    element.click()

    # selecciona el iframe que contiene el resto de la aplicación
    w.until(EC.frame_to_be_available_and_switch_to_it("output_frame"))

    element = w.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='select_1']")))
    element.click()

    element = w.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='select_option_3']")))
    element.click()

    # necesarios para evitar missclicks
    time.sleep(1)

    # selecciona opción 'Tipo de concurso' (elige opción default)
    element = driver.find_element_by_xpath("//*[@id='input_5']")
    element.clear()
    element.send_keys(2)

    # necesarios para evitar missclicks
    time.sleep(1)

    # selecciona opción 'Datos personales'
    element = driver.find_element_by_xpath("/html/body/ui-view/div/div/md-content/form/ng-form/div/div[6]/md-input-container[1]/md-checkbox")
    element.click()

    # necesarios para evitar missclicks
    time.sleep(1)

    progBarLimit=len(workFile['ID'])
    aux.printProgressBar(0, progBarLimit, prefix = 'Progreso:', suffix = 'Completado', length = 50)

    # aplica iteración sobre la lista de concursos para extraer información
    for idx, concursoId in enumerate(workFile['ID']):
        element = w.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='input_4']")))
        element.clear()
        element.send_keys(concursoId)

        # descarga los datos
        w=WebDriverWait(driver,5)
        element = driver.find_element_by_xpath("/html/body/ui-view/div/div/md-content/form/md-input-container/button")
        element.click()

        aux.printProgressBar(idx, progBarLimit, prefix = 'Progreso:', suffix = 'Completado', length = 50)
        aux.waitToDownloadExcel(downloadFolder)
        
    # cierra el navegador una vez que ya ha terminado
    aux.printProgressBar(idx+1, progBarLimit, prefix = 'Progreso:', suffix = 'Completado', length = 50)

# always close the explorer
finally:
    driver.quit()