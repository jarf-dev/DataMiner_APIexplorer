import os
import time

# función que revisa si se ha completado la descarga (basado en revisar si hay un archivo nuevo en la carpeta objetivo)
def waitToDownloadExcel(pathFolder,timeOutMins=3):
    # will check until a new xlsx is added to a folder
    path, dirs, files = next(os.walk(pathFolder))
    initFiles = len(files)
    currFiles = initFiles

    iniTime=time.time()
    while initFiles==currFiles:
        path, dirs, files = next(os.walk(pathFolder))
        initFiles = len(files)

        curTime=time.time()
        timePassed = curTime-iniTime
        # check the timeout
        if timePassed>(timeOutMins*60000):
            break

        # delay 1 second
        time.sleep(1)

# Función para mostrar una barra de progreso
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Imprime la nueva línea al terminar
    if iteration == total: 
        print()