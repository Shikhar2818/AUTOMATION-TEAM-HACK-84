from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
import pyautogui

chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Sort of works like a proxy server
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

service = Service(executable_path="chromedriver.exe")

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.goibibo.com/")

driver.maximize_window()

WebDriverWait(driver,30).until(
  EC.presence_of_element_located((By.CLASS_NAME , "loginCont__input"))
)

number = driver.find_element(By.CLASS_NAME , "loginCont__input")
number.send_keys("" + Keys.RETURN)# enter the required number!

time.sleep(3)

WebDriverWait(driver,100).until(
  EC.presence_of_element_located((By.XPATH , "//div[@class='sc-hRJfrW hqYPJv']"))
)
button1 = driver.find_element(By.XPATH , "//div[@class='sc-hRJfrW hqYPJv']")
button1.click()



""" time.sleep(15) """

WebDriverWait(driver,100).until(
  EC.presence_of_element_located((By.XPATH , "//span[text()='Bus']"))
)

bus_tag = driver.find_element(By.XPATH , "//span[text()='Bus']")
bus_tag.click()

WebDriverWait(driver,10).until(
  EC.presence_of_element_located((By.NAME , "autosuggestBusSRPSrcHomeName"))
)
from_station = driver.find_element(By.NAME , "autosuggestBusSRPSrcHomeName")
from_station.send_keys("Bangalore" + Keys.RETURN)
WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.XPATH , "//span[text()='Bangalore, Karnataka']"))
)
send_click1 = driver.find_element(By.XPATH , "//span[text()='Bangalore, Karnataka']")
send_click1.click()

to_station = driver.find_element(By.NAME , "autosuggest")
to_station.send_keys("Goa"+ Keys.RETURN)

WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.XPATH , "//span[text()='Goa']"))
)
send_click2 = driver.find_element(By.XPATH , "//span[text()='Goa']")
send_click2.click()
tomorr = driver.find_element(By.XPATH , "//span[text()='Tomorrow']")
tomorr.click()

time.sleep(2)

search_button = driver.find_element(By.XPATH , "//div[@class='SearchWidgetstyles__ButtonWrap-sc-1mr4hwz-7 bXLXuO']")
search_button.click()

time.sleep(2)

ac_icon = pyautogui.locateCenterOnScreen('image_ac.png', confidence=0.5)
pyautogui.click(ac_icon)

time.sleep(2)

sleeper_icon = pyautogui.locateCenterOnScreen('image_sleeper.png', confidence=0.5)
pyautogui.click(sleeper_icon)

time.sleep(1)

select_seat_button = driver.find_element(By.XPATH , "//button[@class='Button-sc-110xfhu-4 jcHJWt']")
select_seat_button.click()

time.sleep(2)

pickup_point = driver.find_element(By.XPATH , "//label[@class='LocationPointsstyles__listItem-sc-4474db-0 imOZgL']")
pickup_point.click()

time.sleep(1)

try:
    gandhimaidan_icon = pyautogui.locateCenterOnScreen('molem.png', confidence=0.5)
    pyautogui.click(gandhimaidan_icon)
except:
    bariya_stand_icon = pyautogui.locateCenterOnScreen('ramnagar.png', confidence=0.5)
    pyautogui.click(bariya_stand_icon)
else:
    mithapur_icon = pyautogui.locateCenterOnScreen('ponda.png', confidence=0.5)
    pyautogui.click(mithapur_icon)
  
time.sleep(3)

WebDriverWait(driver,10).until(
  EC.presence_of_element_located((By.XPATH , "//button[text()='CONTINUE']"))
)

continue_button = driver.find_element(By.XPATH , "//button[text()='CONTINUE']")
continue_button.click()

time.sleep(1)

pyautogui.scroll(-300)

time.sleep(1)

no_icon = pyautogui.locateCenterOnScreen('no_image.png', confidence=0.5)
pyautogui.click(no_icon)

time.sleep(2)
pyautogui.scroll(-700)
time.sleep(2)

enter_name = driver.find_element(By.XPATH , "//input[@placeholder='Enter Full Name']")
enter_name.click()
enter_name.send_keys("Md Amaan Haque")

time.sleep(1)

enter_age = driver.find_element(By.XPATH , "//input[@placeholder='Age']")
enter_age.click()
enter_age.send_keys("19")

time.sleep(1)

male = driver.find_element(By.XPATH , "//span[text()='Male']")
male.click()

time.sleep(1)
pyautogui.scroll(-400)

enter_email = driver.find_element(By.XPATH , "//input[@placeholder='Enter Email Address']")
enter_email.click()
enter_email.send_keys("irshadimam1506@gmail.com")

time.sleep(1)

enter_num = driver.find_element(By.XPATH , "//input[@placeholder='Enter Mobile Number']")
enter_num.click()
enter_num.send_keys("8709773081")

time.sleep(2)

try:
    confirm_icon = pyautogui.locateCenterOnScreen('confirm.png', confidence=0.5)
    pyautogui.click(confirm_icon)
except:
    print("The button was not present!!")





time.sleep(5)

submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Pay ₹')]")
submit_button.click()

time.sleep(10)

WebDriverWait(driver,100).until(
    EC.presence_of_element_located((By.XPATH , "//div[text()='VIEW QR']"))
)

qr = driver.find_element(By.XPATH , "//div[text()='VIEW QR']")
qr.click()

time.sleep(1000)








