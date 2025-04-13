import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
import random
from fake_useragent import UserAgent
import pickle
import re
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver_autoinstaller.install()

def create_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    return options

def random_mouse_move(driver):
    try:
        window_width = driver.execute_script("return window.innerWidth;")
        window_height = driver.execute_script("return window.innerHeight;")
        action = ActionChains(driver)
        x_offset = random.randint(-window_width//2, window_width//2)
        y_offset = random.randint(-window_height//2, window_height//2)
        action.move_by_offset(x_offset, y_offset).perform()
        time.sleep(random.uniform(0.5, 1.5))
    except Exception as e:
        print(f"Mouse move error: {e}")
        driver.execute_script("window.scrollBy(0, 250);")
        time.sleep(1)

link_list = [
    "https://vidoza.net/wrydoiavxwah.html",
    "https://vidoza.net/4e092waby72t.html",
    "https://vidoza.net/x1glh2z2ccv3.html",
    "https://vidoza.net/jaujsy44dsfs.html",
    "https://vidoza.net/kbmt8ko3sqry.html",
    "https://vidoza.net/wz7y61mvyxgg.html",
    "https://vidoza.net/ympwmf1bf7ya.html",
    "https://vidoza.net/6xn620zitjmg.html"
]

selected_links = random.sample(link_list, 2)
selected_links = selected_links + selected_links

def run_main_selenium():
    for link in selected_links:
        for repeat in ["1", "2", "2"]:
            driver = webdriver.Chrome(options=create_chrome_options())
            try:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                driver.get("https://www.dailymotion.com/playlist/x9dd5m")
                time.sleep(random.uniform(5, 10))

                driver.get(link)
                time.sleep(random.uniform(3, 5))
                random_mouse_move(driver)

                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "vplayer")))

                for i in range(5):
                    try:
                        play_button_xpath = "//button[@title='Play Video']"
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, play_button_xpath)))
                        play_button = driver.find_element(By.XPATH, play_button_xpath)
                        driver.execute_script("arguments[0].scrollIntoView(true);", play_button)
                        play_button.click()
                        time.sleep(2)

                        driver.execute_script("""
                            var playButton = document.evaluate("//div[@id='vplayer']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                            if (playButton) {
                                playButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                setTimeout(function() { playButton.click(); }, 500);
                            }
                        """)
                        time.sleep(5)
                        driver.save_screenshot(f"screenshot_{i}.png")
                        random_mouse_move(driver)
                        random_mouse_move(driver)

                    except Exception as e:
                        print(f"Play button error: {e}")
                        try:
                            driver.execute_script("""
                                var element = document.getElementById('vplayer');
                                var clickEvent = new MouseEvent('click', {
                                    bubbles: true,
                                    cancelable: true,
                                    view: window
                                });
                                element.dispatchEvent(clickEvent);
                            """)
                            element = driver.find_element(By.XPATH, play_button_xpath)
                            actions = ActionChains(driver)
                            actions.move_to_element_with_offset(element, 5, 5).click().perform()
                            time.sleep(30)
                            driver.save_screenshot(f"screenshot_{i}.png")
                        except Exception as ee:
                            print(f"Fallback click failed: {ee}")

                time.sleep(150)
                driver.save_screenshot("screenshot_final.png")

                # Download phase
                download_button_xpath = "//a[@class='btn btn-success btn-lg btn-download btn-download-n']"
                for i in range(5):
                    try:
                        download_button = driver.find_element(By.XPATH, download_button_xpath)
                        download_button.click()
                        time.sleep(random.uniform(1, 3))
                        random_mouse_move(driver)
                        driver.save_screenshot(f"download_{i}.png")
                    except Exception as e:
                        print(f"Download error: {e}")
            except Exception as e:
                print(f"[Session error] {e}")
            finally:
                driver.quit()

# ==============================
# Retry wrapper with 20 mins timeout
# ==============================
start_time = time.time()
max_duration = 20 * 60  # 20 minutes in seconds

while True:
    try:
        run_main_selenium()
        break  # Success, exit loop
    except Exception as main_e:
        print(f"[Retrying] Error caught: {main_e}")
        if time.time() - start_time > max_duration:
            print("Time limit exceeded (20 minutes). Exiting.")
            break
        print("Retrying full session in 5 seconds...")
        time.sleep(5)
