# 🤖 Youth Dream 自動投票機器人 (Auto Voting Bot)

這是一個基於 **Python + Selenium** 開發的自動化投票工具，專為 **Youth Dream 平台**設計。具備自動登入、2Captcha 驗證碼破解、多執行緒併發處理，以及支援多個投票目標的功能。

---

## ✨ 主要功能

### 🚀 高效能併發

* 支援 **多執行緒 (Multithreading)**
* 可同時開啟多個瀏覽器視窗進行投票
* 大幅縮短投票時間

### 🛡️ 驗證碼破解

* 整合 **2Captcha API**
* 自動識別登入驗證碼並填入

### 👻 雙模式執行

* **前台模式**：顯示瀏覽器視窗，方便觀察與除錯
* **無頭模式（Headless）**：背景靜默執行、降低資源消耗

### 🎯 多目標支援

* 可設定多個投票網址
* 程式會依序完成所有目標的投票

### 📸 智慧截圖

* 投票成功後自動**滾動至頁面底部截圖**
* 依據不同投票網址自動建立資料夾：

  * `Target_1/`
  * `Target_2/`
  * …依此類推

### 🔧 設定分離

* 敏感資料（API Key）與一般設定分離
* 管理更安全、維護更方便

---

## 📂 檔案結構

請確保資料夾內包含以下檔案：

| 檔案名稱               | 用途說明                                |
| ------------------ | ----------------------------------- |
| `main.py`          | 🐍 程式核心邏輯代碼                         |
| `.env`             | 🔑 私密設定（放置 2Captcha API Key）        |
| `config.ini`       | ⚙️ 一般設定（網址、執行緒數量、瀏覽器模式）             |
| `accounts.csv`     | 👥 帳號密碼清單                           |
| `chromedriver.exe` | 🌐 Chrome WebDriver（需與 Chrome 版本相符） |
| `install.bat`      | 📦 一鍵安裝 Python 套件                   |
| `run.bat`          | ▶️ 一鍵執行程式                           |

---

## 🛠️ 安裝與設定教學

### 1. 環境準備

1. 安裝 **Python 3.x**（記得勾選 *Add Python to PATH*）
2. 下載符合您 **Chrome 版本**的 ChromeDriver 並放入專案資料夾

---

### 2. 安裝套件

雙擊 `install.bat`
等待顯示 **「所有套件安裝成功」** 即完成。

---

### 3. 準備帳號（accounts.csv）

建立一個 CSV，格式如下（第一列為標題，程式會自動跳過）：

```csv
email,password
user1@example.com,password123
user2@example.com,password456
```

---

### 4. 設定金鑰（.env）

編輯 `.env`：

```
CAPTCHA_API_KEY=你的_2Captcha_API_Key
```

---

### 5. 調整參數（config.ini）

`config.ini` 檔案可用來設定程式行為：

```ini
[Browser]
# True = 隱藏視窗（背景執行）, False = 顯示視窗
Headless = False

[Performance]
# 同時開啟的瀏覽器視窗數
MaxWorkers = 2

[Urls]
# 投票網址清單（移除不需投票的網址即可）
TargetUrls = 
    https://website.com/vote/project_A
    https://website.com/vote/project_B
```

---

## ▶️ 如何使用

1. 確認上述設定皆已完成
2. 雙擊 `run.bat`
3. 程式會自動開啟瀏覽器並開始投票
4. 完成後視窗會提示 **「所有作業結束」**

---

## 📁 輸出結果

所有截圖會儲存於 `screenshots` 資料夾，並依目標分類：

* `screenshots/Target_1/`
* `screenshots/Target_2/`

檔名格式：

```
帳號_success_日期時間.png
```

---

## ⚠️ 注意事項

* **ChromeDriver 版本需與 Chrome 相符**
  Chrome 自動更新後，若版本不符需重新下載。
* **2Captcha 需消耗點數**
  請確認帳戶餘額足夠。
* **執行速度受電腦效能影響**
  RAM 較低可調整 `MaxWorkers = 1` 或 `2`。

---

## 📜 免責聲明

本工具僅供 **技術研究** 與 **自動化測試教學用途**。
請勿用於任何違反法律或目標網站使用條款之行為。
使用者需自行承擔因使用本工具所產生之所有後果。