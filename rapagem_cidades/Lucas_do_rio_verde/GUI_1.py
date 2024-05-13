import pyautogui
import time

def esperar(tempo):
    time.sleep(tempo)

def abrir_planilha():
    pyautogui.hotkey('win')
    esperar(1)
    pyautogui.write('wps s', interval=0.2)
    pyautogui.press('enter')
    esperar(3)
    pyautogui.moveTo(46, 160)
    pyautogui.click()
    pyautogui.moveTo(962, 91)
    pyautogui.click()
    esperar(1)
    pyautogui.moveTo(352, 369)
    pyautogui.click()

pyautogui.press('win')
esperar(1)
pyautogui.write('firefox', interval=0.02)
pyautogui.press('enter')
esperar(2)
pyautogui.write('https://transparencia.betha.cloud/#/cST4aUw2ylR2Zxh80uoChw==/consulta/28404?esconderCabecalho=S&esconderMenu=S&esconderRodape=S', interval=0.02)
pyautogui.press('enter')
esperar(10)
pyautogui.moveTo(880, 618)
pyautogui.click()
esperar(1)
pyautogui.scroll(-100)
pyautogui.moveTo(174, 934)
pyautogui.click()
pyautogui.moveTo(147, 998)
pyautogui.click()
pyautogui.moveTo(50, 467)
esperar(1)



pyautogui.scroll(500)
pyautogui.mouseDown(50, 467, button='left')
pyautogui.scroll(-300)
pyautogui.mouseUp(1867, 889, button='left', duration=1)
esperar(1)
pyautogui.hotkey('ctrl', 'c')


esperar(1)
abrir_planilha()
esperar(1)
pyautogui.hotkey('ctrl', 'v')


'''
pyautogui.moveTo(82, 244)
pyautogui.rightClick()
pyautogui.moveTo(116, 319)
'''
esperar(3)
pyautogui.moveTo()
pyautogui.mouseDown(1912, 943, button='left', duration=8)
pyautogui.mouseUp(1912, 943, button='left',)

