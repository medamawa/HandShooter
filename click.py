import pyautogui

while True:
    pyautogui.FAILSAFE = False

    print(pyautogui.position())
    pyautogui.sleep(2)

    pyautogui.click(x=1710, y=1060, button='left')