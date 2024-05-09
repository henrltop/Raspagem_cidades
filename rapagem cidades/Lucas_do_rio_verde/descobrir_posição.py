import time
import pyautogui

time.sleep(5)

posi = pyautogui.position()
print(posi)
pyautogui.alert(posi, 'Posição do mouse', 'OK')