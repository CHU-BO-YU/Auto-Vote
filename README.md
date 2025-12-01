# 自動投票機器人使用說明

本工具用於自動化跑投票流程，包含自動登入、解析 CAPTCHA、投票與截圖。本說明將逐步引導你完成環境設定與操作。

---

# 0. 取得本專案

## 方法一：使用 Git 下載（推薦）

```bash
git clone https://github.com/你的帳號/你的專案.git
cd 你的專案
```

## 方法二：下載 ZIP

1. 前往 GitHub 專案頁
2. 點擊 **Code** → **Download ZIP**
3. 解壓縮後即可使用

所有檔案（chromedriver.exe、install.bat、run.bat 等）皆已包含在專案內，不需移動或修改路徑。

---

# 1. 環境準備

## 安裝 Python

請至 Python 官方網站下載並安裝（安裝時務必勾選 Add Python to PATH）：
[https://www.python.org/downloads/](https://www.python.org/downloads/)

## ChromeDriver

本專案已附上 `chromedriver.exe`，無需下載額外檔案。

---

# 2. 初始設定

## 2.1 安裝套件

在專案資料夾中執行：

```
install.bat
```

程式會自動安裝所需的 Python 套件。

---

## 2.2 設定帳號

本程式會從 `accounts.csv` 讀取帳密。
請依以下格式填寫：

```csv
email,password
user1@test.com,pass123
user2@test.com,pass456
```

可新增多組帳號，一行一組。

---

## 2.3 設定 2Captcha API 金鑰

前往 2Captcha 註冊並儲值：
[https://2captcha.com/](https://2captcha.com/)

取得 API Key 後，填入 `.env` 檔：

```env
CAPTCHA_API_KEY=你的_API_KEY
```

---

# 3. 設定 config.ini

以下為完整的 `config.ini`，可直接使用，不需調整路徑。

```ini
[Browser]
DriverPath = chromedriver.exe
Headless = False

[Performance]
MaxWorkers = 2
MaxLoginRetries = 5

[Data]
AccountsFile = accounts.csv

[Urls]
LoginUrl = https://youthdream.phdf.org.tw/member/login

TargetUrls = 
    # 寒服專案網址
    https://youthdream.phdf.org.tw/project/show?keyword=%E7%9C%9F%E7%9B%B8%E5%8F%AA%E6%9C%89%E4%B8%80%E5%80%8B%21%E4%B8%AD%E8%8A%B8%E5%81%B5%E6%8E%A2%E5%9C%98%E4%BA%8B%E4%BB%B6%E7%B0%BF&page=1

    # Maker 專案網址
    https://youthdream.phdf.org.tw/project/show?keyword=maker&page=1
```

---

## 3.1 如何新增投票網址

只需在 TargetUrls 下面加入一行（注意縮排）：

```ini
TargetUrls =
    https://...(寒服)
    https://...(maker)
    https://youthdream.phdf.org.tw/project/show?keyword=robot&page=1
```

縮排至少四個空格非常重要，否則程式無法讀取。

---

## 3.2 如何刪除不需要的網址

如果你不想投某一個項目，只要將那一行（含註解）刪除即可，例如：

```ini
TargetUrls =
    # Maker 專案網址
    https://youthdream.phdf.org.tw/project/show?keyword=maker&page=1
```

---

## 3.3 Headless 模式（隱藏瀏覽器）

如需隱藏視窗，將：

```ini
Headless = False
```

改為：

```ini
Headless = True
```

---

# 4. 開始執行程式

在專案資料夾中執行：

```
run.bat
```

程式將會：

1. 讀取帳號
2. 逐一登入
3. 處理 2Captcha
4. 自動投票
5. 截圖存入 `screenshots/`

執行完畢會自動結束。

---

# 5. 常見問題（FAQ）

### 程式無法登入？

* 檢查帳號密碼是否正確
* 檢查 2Captcha 餘額是否足夠
* 網站可能暫時維護，可稍後再試

### 顯示找不到 chromedriver？

本專案已內附 `chromedriver.exe`，請確保你沒有手動移動或刪除。

### 投票網址讀不到？

請檢查：

* 是否有縮排
* 每行是否都是完整的 URL
* 不要在 TargetUrls= 同一行放網址