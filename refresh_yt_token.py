#!/usr/bin/env python3
import json
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def get_yt_music_token():
    # 設定 Chrome 為 headless 模式，並啟用 performance log
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # 啟用 performance logging
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    # 使用 Service 指定 chromedriver 的路徑
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # 開啟 YouTube Music 網站
    driver.get("https://music.youtube.com")
    # 等待網頁載入（依網速可調整等待時間）
    time.sleep(10)
    
    # 取得 performance logs
    logs = driver.get_log("performance")
    token = None

    # 解析每筆 log，篩選出含有 innertube 請求的項目
    for entry in logs:
        try:
            message = json.loads(entry["message"])["message"]
            if "request" in message and "headers" in message["request"]:
                headers = message["request"]["headers"]
                # 此處以 "Authorization" 為例，實際請求可能不同
                if "Cookie" in headers:
                    token = headers["Cookie"]
                    break
        except Exception as e:
            continue

    driver.quit()
    return token

if __name__ == '__main__':
    token = get_yt_music_token()
    if token:
        print(token)
    else:
        print("無法取得 token", file=sys.stderr)
        sys.exit(1)
