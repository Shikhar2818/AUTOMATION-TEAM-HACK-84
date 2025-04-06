from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Ensure correct path
service = Service(executable_path="chromedriver.exe")  
driver = webdriver.Chrome(service=service)


def open_irctc(driver, username, password):
    driver.get("https://www.irctc.co.in/nget/train-search")
    wait = WebDriverWait(driver, 20)

    # Login process
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'loginText')))
    login_button.click()
    
    username_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="userid"]')))
    password_input = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]')
    
    username_input.send_keys(username)
    password_input.send_keys(password)

    def solve_captcha():
        captcha_input = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="captcha"]')
        captcha_input.click()

        # ✅ Capture CAPTCHA Image
        captcha_image = driver.find_element(By.XPATH, "//img[contains(@class,'captcha-img')]")
        captcha_image.screenshot("captcha.png")

        # ✅ Use OCR to Read CAPTCHA Text
        captcha_text = pytesseract.image_to_string(Image.open("captcha.png")).strip()
        print("Detected CAPTCHA:", captcha_text)

        captcha_input.send_keys(captcha_text)
        time.sleep(2)

        sign_in_button = driver.find_element(By.XPATH, "//button[contains(text(), 'SIGN IN')]")
        sign_in_button.click()

    # First attempt to solve CAPTCHA
    solve_captcha()

    # Check if login is successful or needs retry
    attempts = 0
    while attempts < 3:  # Max 3 attempts
        time.sleep(5)  # Wait for page to load

        try:
            # Check if login was successful
            if driver.find_element(By.XPATH, "//span[contains(text(), 'Logout')]").is_displayed():
                print("Login successful!")
                return True
        except:
            pass

        try:
            # Check if an error message appears (indicating CAPTCHA failure)
            error_message = driver.find_element(By.XPATH, "//div[contains(text(), 'Invalid Captcha....')]").text
            if error_message:
                print("Login failed due to incorrect CAPTCHA. Retrying...")
                solve_captcha()
                attempts += 1
        except:
            pass

    print("Login failed after multiple attempts.")
    return False



#TRAVEL STATION AND DATE
def input_station_details(driver, journey_date,source_station,destination_station):
    wait = WebDriverWait(driver, 10)
    
    # Enter source station name and select the first suggestion
    source_station_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-autocomplete="list"].ng-tns-c57-8')))
    source_station_input.send_keys(source_station)
    # Wait for the autocomplete options to appear and select the first option
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.ng-tns-c57-8[role="option"]'))).click()

    # Enter destination station name and select the first suggestion
    destination_station_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-autocomplete="list"].ng-tns-c57-9')))
    destination_station_input.send_keys(destination_station)
    # Wait for the autocomplete options to appear and select the first option
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.ng-tns-c57-9[role="option"]'))).click()

    # Enter the journey date
    date_input = wait.until(EC.visibility_of_element_located((By.ID, 'jDate')))
    ActionChains(driver).move_to_element(date_input).click(date_input).double_click().click_and_hold().send_keys(Keys.CLEAR).send_keys(journey_date).perform()
    # Select 'Tatkal' from the dropdown
    dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.ng-tns-c65-12.ui-dropdown')))
    dropdown.click()
   # tatkal_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='TATKAL']")))
   # tatkal_option.click()
    #For General
    

    g_o= wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='GENERAL']")))
    g_o.click()
   
  
    # Click the 'Search' button
    search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.search_btn.train_Search')))
    search_button.click()



def wait_for_url(driver, target_url):
    WebDriverWait(driver, 300).until(EC.url_to_be(target_url))
    print(f"Page redirected to {target_url} successfully.")



def select_train_and_class(driver, train_name, class_type, travel_date):
    wait = WebDriverWait(driver, 15)

    try:
        # Locate the train list container
        train_list_xpath = "//*[@id='divMain']/div/app-train-list/div[4]"
        train_list = wait.until(EC.presence_of_element_located((By.XPATH, train_list_xpath)))

        # Find the specific train inside the container
        train_xpath = f".//div[contains(@class, 'train-heading')]/strong[contains(text(), '{train_name}')]"
        train_element = train_list.find_element(By.XPATH, train_xpath)
        print(f"Train found: {train_name}")

        # Get the parent container (specific train block)
        train_container = train_element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'form-group')]")
        print("Train container located.")

        # Find the class selection button **inside this train only**
        class_xpath = f".//div[contains(@class, 'pre-avl')]//strong[contains(text(), '{class_type}')]"
        class_elements = train_container.find_elements(By.XPATH, class_xpath)

        if not class_elements:
            print(f"Error: Class {class_type} not found for {train_name}!")
            return

        button = class_elements[0]
        time.sleep(3)
        # Scroll and click using JavaScript to avoid interception issues
        driver.execute_script("arguments[0].scrollIntoView();", button)
        driver.execute_script("arguments[0].click();", button)
        print(f"Successfully selected {class_type} for {train_name}")

        time.sleep(2)

        # Select the correct date (only if it's available)
        date_xpath = f"//td[contains(@class, 'link')]/div[contains(@class, 'pre-avl')]/div/strong[contains(text(), '{travel_date}')]"
        date_elements = driver.find_elements(By.XPATH, date_xpath)

        if not date_elements:
            print(f"Error: Travel date {travel_date} not found or not available!")
            return
        
        date_element = date_elements[0]

        # Scroll and click using JavaScript
        driver.execute_script("arguments[0].scrollIntoView();", date_element)
        #time.sleep(1)
        driver.execute_script("arguments[0].click();", date_element)
        print(f"Selected travel date: {travel_date}")
        time.sleep(1)
        driver.execute_script("arguments[0].click();", date_element)
        time.sleep(1)

        book_now_button = train_container.find_element(By.XPATH, ".//button[contains(@class, 'btnDefault') and contains(text(), 'Book Now')]")

        # Scroll into view and click
        driver.execute_script("arguments[0].scrollIntoView();", book_now_button)
        time.sleep(2)
        driver.execute_script("arguments[0].click();", book_now_button)
        time.sleep(1)
    
    except Exception as e:
        print(f"Error: {e}")
       



def add_passengers(driver, passenger_data):
    """
    Function to add multiple passengers dynamically on the IRCTC booking page.
    
    Parameters:
    - driver: Selenium WebDriver instance
    - passenger_data: List of dictionaries containing passenger details
    """
    wait = WebDriverWait(driver, 30)

    for i in range(len(passenger_data)):
        # Click "+ Add Passenger" button for multiple passengers
        if i > 0:
            add_passenger_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "+ Add Passenger")]')))
            add_passenger_btn.click()
        
        # Wait for input fields to appear
        name_inputs = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//input[@placeholder="Name"]')))
        age_inputs = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//input[@formcontrolname="passengerAge"]')))
        gender_dropdowns = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//select[@formcontrolname="passengerGender"]')))
        nationality_dropdowns = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//select[@formcontrolname="passengerNationality"]')))
        berth_dropdowns = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//select[@formcontrolname="passengerBerthChoice"]')))
            
         
        # Fill passenger details
        if i < len(name_inputs):
            name_inputs[i].send_keys(passenger_data[i]["name"])
        if i < len(age_inputs):
            age_inputs[i].send_keys(passenger_data[i]["age"])
        if i < len(gender_dropdowns):
            Select(gender_dropdowns[i]).select_by_visible_text(passenger_data[i]["gender"])
        if i < len(nationality_dropdowns):
            Select(nationality_dropdowns[i]).select_by_visible_text(passenger_data[i]["nationality"])
        if i < len(berth_dropdowns):
            Select(berth_dropdowns[i]).select_by_visible_text(passenger_data[i]["berth"])

    print("Passenger details filled successfully!")

time.sleep(2)

def finalize_booking_details(driver):
    wait = WebDriverWait(driver, 2)
    
    # Click on 'Consider for Auto Upgradation' checkbox
    auto_upgrade_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Consider for Auto Upgradation')]")))
    time.sleep(1)  # Avoid if possible
    auto_upgrade_checkbox_id = auto_upgrade_label.get_attribute("for")
    auto_upgrade_checkbox = driver.find_element(By.ID, auto_upgrade_checkbox_id)
    if not auto_upgrade_checkbox.is_selected():
        driver.execute_script("arguments[0].click();", auto_upgrade_checkbox)
    time.sleep(1)

    # Click on 'Book only if confirm berths are allotted' checkbox
    try:
        confirm_berths_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Book only if confirm berths are allotted')]")))
        confirm_berths_checkbox_id = confirm_berths_label.get_attribute("for")
        confirm_berths_checkbox = driver.find_element(By.ID, confirm_berths_checkbox_id)
        if not confirm_berths_checkbox.is_selected():
            driver.execute_script("arguments[0].click();", confirm_berths_checkbox)
    except Exception as e:
        print("Confirm berth checkbox not found:")

    # Click on radio button 'No, I don't want travel insurance'
    try:
        time.sleep(1)  # Avoid if possible
        no_insurance_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), \"No, I don't want travel insurance\")]")))
        no_insurance_radio_id = no_insurance_label.get_attribute("for")
        no_insurance_radio = driver.find_element(By.ID, no_insurance_radio_id)
        no_insurance_radio.click()
    except Exception as e:
        print("Travel insurance radio button not found:")
     # Click on radio button 'Pay through BHIM/UPI'
    upi_payment_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Pay through BHIM')]")))
    upi_payment_radio_id = upi_payment_label.get_attribute("for")
    upi_payment_radio = driver.find_element(By.ID, upi_payment_radio_id)
    upi_payment_radio.click()
    time.sleep(1)
    # Click on the 'Continue' button
    continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]")))
    continue_button.click()
    time.sleep(5)

    def last_captcha():
        captcha_ = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="captcha"]')))
        captcha_.click()
        # Wait for the captcha image to load
        captcha_image2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@class,'captcha-img')]")))
        captcha_image2.screenshot("captcha2.png")
        print("Captcha input and image loaded successfully.")
        # ✅ Use OCR to Read CAPTCHA Text
        captcha_text2 = pytesseract.image_to_string(Image.open("captcha2.png")).strip()
        print("Detected CAPTCHA:", captcha_text2)
        time.sleep(2)
        captcha_.send_keys(captcha_text2)
        time.sleep(3)
        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]")))
        continue_button.click()
       
    last_captcha()
    #check if the captcha is solved
    attempt2= 0
    while attempt2 < 3:
        time.sleep(4)
        try:
            # Check if login was successful
            if driver.find_element(By.XPATH, "//span[contains(text(), 'Payment Methods')]").is_displayed():
                print("captcha 2 solved successfully !")
                return True
        except:
            pass

        try:
            # Check if an error message appears (indicating CAPTCHA failure)
            error_message2 = driver.find_element(By.XPATH, "//div[contains(text(), 'Error!')]").text
            if error_message2:
                print("Login failed due to incorrect CAPTCHA. Retrying...")
                last_captcha()
                attempt2 += 1
        except:
            pass

    print("Login failed after multiple attempts.")
    return False

def login_with_upi(driver):
    #wait=WebDriverWait(driver,10)
   
    print("Final booking step.")
    time.sleep(1)
    buttons = [
    "//*[@id='pay-type']/span/div[2]",
    "//*[@id='bank-type']/div/table/tr/span[1]/td/div/div",
    "//*[@id='psgn-form']/div[1]/div[1]/app-payment/div[2]/button[2]"
    ]

    for xpath in buttons:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        driver.execute_script("arguments[0].scrollIntoView();", button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", button)
        print("Pay through QR")
    time.sleep(60)




if __name__ == "__main__":
    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    # User credentials and journey date
    USERNAME = "" #enter your irctc username
    PASSWORD = ""#enter your irctc password
    JOURNEY_DATE = "07/04/2025"  # Replace 'dd/mm/yyyy' with the actual date
    source_station = "PUNE"
    destination_station = "AHMADNAGAR"
    open_irctc(driver, USERNAME, PASSWORD)
    input_station_details(driver, JOURNEY_DATE,source_station,destination_station)

    #train info

    train_name = "PUNE DNR EXPRESS (12149)"  # Example train
    class_type = "AC 3 Tier (3A)"  # Example class
    travel_date = "Mon, 07 Apr"  # Example date (Must match format from HTML)  "Mon, 07 Apr"
    select_train_and_class(driver, train_name, class_type, travel_date)

    # Example passenger data
    passenger_data = [
    {"name": "Shikhar Verma", "age": "18", "gender": "Male", "nationality": "India", "berth": "Lower"},
    {"name": "Md Amaan Haque", "age": "19", "gender": "Male", "nationality": "India", "berth": "Upper"},
    ]
    add_passengers(driver, passenger_data)
    
    wait_for_url(driver, "https://www.irctc.co.in/nget/booking/psgninput")
    finalize_booking_details(driver)
    login_with_upi(driver)
