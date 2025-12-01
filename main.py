import os
import time
import csv
import requests
import configparser
import concurrent.futures
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException

# --- 1. 載入設定 ---
load_dotenv()

# [關鍵修正] 加入 interpolation=None，告訴程式不要把網址裡的 % 當成變數處理
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini', encoding='utf-8')

if not os.path.exists('config.ini'):
    print("❌ 錯誤：找不到 config.ini 設定檔！")
    exit(1)

# --- 2. 變數配置 ---
# 從 .env 讀取私密金鑰
API_KEY = os.getenv("CAPTCHA_API_KEY")

try:
    # 從 config.ini 讀取一般設定
    CHROME_DRIVER_PATH = config.get('Browser', 'DriverPath')
    HEADLESS_MODE = config.getboolean('Browser', 'Headless')
    
    MAX_WORKERS = config.getint('Performance', 'MaxWorkers')
    MAX_LOGIN_RETRIES = config.getint('Performance', 'MaxLoginRetries')
    
    ACCOUNTS_FILE = config.get('Data', 'AccountsFile')
    
    LOGIN_URL = config.get('Urls', 'LoginUrl')
    
    # 讀取多行網址，過濾掉空行
    raw_urls = config.get('Urls', 'TargetUrls')
    TARGET_URLS = [url.strip() for url in raw_urls.split('\n') if url.strip()]

except Exception as e:
    print(f"❌ config.ini 讀取錯誤: {e}")
    print("請檢查設定檔內容格式是否正確。")
    exit(1)

SCREENSHOT_DIR = "screenshots"

# 基本檢查
if not API_KEY:
    print("❌ 錯誤：未在 .env 找到 CAPTCHA_API_KEY")
    exit(1)

if not TARGET_URLS:
    print("❌ 錯誤：config.ini 中沒有設定 TargetUrls (目標網址)")
    exit(1)

# 確保截圖主目錄存在
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def get_driver():
    """配置並回傳 Chrome Driver"""
    chrome_options = Options()
    if HEADLESS_MODE:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        # 無頭模式下設定大視窗，確保截圖完整
        chrome_options.add_argument("--window-size=1920,1080")
    else:
        chrome_options.add_argument("--start-maximized")

    chrome_options.add_argument("--log-level=3")
    # 規避自動化偵測
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def solve_captcha_base64(driver, element):
    """直接從記憶體截圖並傳送 Base64 給 2Captcha"""
    try:
        # 取得圖片的 base64 字串
        img_base64 = element.screenshot_as_base64
        
        # 上傳給 2Captcha
        response = requests.post(
            "http://2captcha.com/in.php",
            data={"key": API_KEY, "method": "base64", "body": img_base64, "json": 1}
        )
        resp_json = response.json()
        
        if resp_json.get("status") != 1:
            print(f"⚠️ 驗證碼上傳失敗: {resp_json}")
            return None

        captcha_id = resp_json.get("request")
        
        # 輪詢等待解碼結果
        result_url = f"http://2captcha.com/res.php?key={API_KEY}&action=get&id={captcha_id}&json=1"
        for _ in range(20): # 最多等待 40 秒
            time.sleep(2)
            result_resp = requests.get(result_url).json()
            if result_resp.get("status") == 1:
                return result_resp.get("request")
            elif result_resp.get("request") == "CAPCHA_NOT_READY":
                continue
            else:
                return None
    except Exception as e:
        print(f"⚠️ 驗證碼處理異常: {e}")
    return None

def process_account(account_data):
    """單一帳號的完整流程 (登入 + 多目標投票)"""
    email, password = account_data
    driver = get_driver()
    wait = WebDriverWait(driver, 20)
    
    print(f"[{email}] 啟動瀏覽器 (共需投 {len(TARGET_URLS)} 個項目)...")
    
    try:
        # --- 登入流程 ---
        driver.get(LOGIN_URL)
        login_success = False
        
        for attempt in range(MAX_LOGIN_RETRIES):
            try:
                try:
                    alert = driver.switch_to.alert
                    alert.accept()
                except:
                    pass

                email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
                email_input.clear()
                email_input.send_keys(email)
                
                pass_input = driver.find_element(By.NAME, "password")
                pass_input.clear()
                pass_input.send_keys(password)
                
                captcha_img = driver.find_element(By.XPATH, "//a[@id='captcha']/img")
                code = solve_captcha_base64(driver, captcha_img)
                
                if code:
                    driver.find_element(By.NAME, "captcha").clear()
                    driver.find_element(By.NAME, "captcha").send_keys(code)
                    
                    submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
                    driver.execute_script("arguments[0].click();", submit_btn)
                    
                    try:
                        wait.until(lambda d: "member/login" not in d.current_url)
                        login_success = True
                        print(f"[{email}] 登入成功！")
                        break 
                    except TimeoutException:
                        print(f"[{email}] 登入後未跳轉 (第 {attempt+1} 次)，重試...")
                        driver.find_element(By.ID, "captcha").click()
                        time.sleep(2)
                else:
                    print(f"[{email}] 驗證碼解析失敗，刷新重試...")
                    driver.find_element(By.ID, "captcha").click()
                    
            except UnexpectedAlertPresentException:
                try:
                    driver.switch_to.alert.accept()
                except:
                    pass
            except Exception as e:
                print(f"[{email}] 登入步驟錯誤: {e}")

        if not login_success:
            print(f"[{email}] ❌ 無法登入，放棄此帳號。")
            return

        # --- 多重投票流程 ---
        for index, url in enumerate(TARGET_URLS, start=1):
            print(f"[{email}] 前往第 {index} 個投票網址...")
            driver.get(url)
            
            try:
                vote_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'vote-project')]")))
                driver.execute_script("arguments[0].click();", vote_btn)
                
                toast = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "toast-message")))
                msg = toast.text
                
                should_screenshot = False
                status_text = ""

                if "投票完成" in msg:
                    status_text = "success"
                    print(f"[{email}] ✅ 第 {index} 票成功！")
                    should_screenshot = True
                elif "已經投給" in msg:
                    status_text = "already_voted" 
                    print(f"[{email}] ⚠️ 第 {index} 票今日已投過。")
                    should_screenshot = False
                else:
                    print(f"[{email}] ❓ 第 {index} 票結果: {msg}")

                if should_screenshot:
                    # 滾動到底部
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1) 

                    # 建立專屬資料夾
                    target_folder = os.path.join(SCREENSHOT_DIR, f"Target_{index}")
                    os.makedirs(target_folder, exist_ok=True)

                    # 儲存截圖
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"{email}_{status_text}_{timestamp}.png"
                    driver.save_screenshot(os.path.join(target_folder, filename))
            
            except TimeoutException:
                print(f"[{email}] ❌ 第 {index} 票逾時或找不到按鈕。")
            except Exception as e:
                print(f"[{email}] ❌ 第 {index} 票發生錯誤: {e}")
            
            time.sleep(1)

        print(f"[{email}] 任務完成。")

    except Exception as e:
        print(f"[{email}] 發生全域錯誤: {e}")
    finally:
        driver.quit()

def main():
    if not os.path.exists(ACCOUNTS_FILE):
        print(f"❌ 找不到 {ACCOUNTS_FILE}。")
        return

    accounts = []
    try:
        with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    accounts.append(row[:2])
    except Exception as e:
        print(f"讀取 CSV 失敗: {e}")
        return

    print(f"=== 準備處理 {len(accounts)} 個帳號 ===")
    print(f"=== 目標數量: {len(TARGET_URLS)} 個 ===")
    print(f"模式: {'隱藏視窗' if HEADLESS_MODE else '顯示視窗'}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(process_account, accounts)
        
    print("=== 所有作業結束 ===")

if __name__ == "__main__":
    main()  