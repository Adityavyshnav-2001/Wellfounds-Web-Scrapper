import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool

app = FastAPI()

# CORS Middleware to allow frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model to accept input from frontend
class MessageRequest(BaseModel):
    message: str

def human_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))

def send_message_sample(message: str):
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-data-dir=/Users/adityavyshnav/Library/Application Support/Google/Chrome")
    options.add_argument("--profile-directory=Profile 1")

    driver = uc.Chrome(options=options)

    try:
        driver.get("https://www.google.com")
        human_delay(2, 4)

        # Navigate to the site where cookies need to be added
        driver.get("https://www.wellfound.com/messages")
        human_delay(2, 5)

        

        driver.refresh()
        human_delay(2, 4)

        driver.maximize_window()

        # Click on message thread for DexyAI
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[4]/div/nav/a[5]'))
        )
        element_1 = driver.find_element(By.XPATH, '//*[@id="main"]/div[4]/div/nav/a[5]')
        ActionChains(driver).move_to_element(element_1).pause(random.uniform(1, 2)).click().perform()
        human_delay(3, 5)

        # Select the DexyAI thread
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h3[@class="styles_startupName__RdpFG" and text()="DexyAI"]'))
        )
        element_2 = driver.find_element(By.XPATH, '//h3[@class="styles_startupName__RdpFG" and text()="DexyAI"]')
        ActionChains(driver).move_to_element(element_2).pause(random.uniform(1, 2)).click().perform()
        human_delay(2, 4)

        # Enter the message in the input field
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form-input--body"]'))
        )
        input_box = driver.find_element(By.XPATH, '//*[@id="form-input--body"]')
        input_box.click()
        human_delay(1, 3)

        # Type the message character by character with a delay
        for char in message:
            input_box.send_keys(char)
            time.sleep(random.uniform(0.2, 0.6))

        human_delay(2, 4)

        # Wait for the submit button and click
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and contains(@class, "styles-module_component_88XzG") and text()="Send"]'))
        )
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit" and contains(@class, "styles-module_component_88XzG") and text()="Send"]')

        # Use JavaScript to click the submit button
        driver.execute_script("arguments[0].click();", submit_button)
        human_delay(2, 4)

        print("Message submitted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

@app.post("/send-message/")
async def send_message(request: MessageRequest):
    message = request.message
    data = await run_in_threadpool(lambda: send_message_sample(message))
    return JSONResponse(content={"status": "Message sent successfully!"})
