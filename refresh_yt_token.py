#!/usr/bin/env python3
import json
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_yt_music_token():
    # 設定 Chrome 為 headless 模式，並啟用 performance log
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # 設定 performance logging
    chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    # 指定 chromedriver 路徑（根據 runner 環境自行調整）
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=chrome_options)
    
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
            # 假設 token 存在於某個內部 API 的 request headers 中
            if "request" in message and "headers" in message["request"]:
                headers = message["request"]["headers"]
                # 此處以 "Authorization" 為例，實際請求可能不同
                if "Authorization" in headers:
                    token = headers["Authorization"]
                    break
        except Exception as e:
            continue

    driver.quit()
    return token

if __name__ == '__main__':
    token = get_yt_music_token()
    if token:
        # 將 token 輸出到標準輸出，方便後續步驟捕獲
        print(token)
    else:
        print("無法取得 token", file=sys.stderr)
        sys.exit(1)
