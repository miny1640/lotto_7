import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, os, datetime

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    return driver

# ===== CSV 읽기 =====
csv_file = "lotto7_lstm_predictions.csv"
df = pd.read_csv(csv_file)
predictions = df.values.tolist()

# ===== Chrome 드라이버 설정 =====
driver = get_driver()

# ===== 로또7 구매 페이지 열기 =====
driver.get("https://www.takarakuji-official.jp/ec/?__ope=%E3%83%AD%E3%83%88&__fromScreenId=SC_WMA_SP_001#loto")

time.sleep(5)  # 페이지 로딩 대기

driver.find_element(By.XPATH, '//a[@onclick="document.loto7FForm.submit(); return false;"]').click()
time.sleep(10)

# ===== 폴더 생성 =====
todayToString = datetime.date.today().strftime('%Y%m%d')
screenshot_dir = f"screenshots/{todayToString}"
screenshot_dir = os.path.join(os.getcwd(), screenshot_dir)
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

n = 0
# ===== 조합 자동 선택 =====
for target_combination in predictions:
    print(f"자동 선택할 조합: {target_combination}")

    # 모든 번호 버튼 요소 가져오기
    buttons = driver.find_elements(By.CLASS_NAME, "m_lotteryNumInputNum_btn")

    # 각 번호 클릭
    for number in target_combination:
        for btn in buttons:
            if btn.text.strip() == str(number):
                btn.click()
                print(f"번호 {number} 선택 완료")
                time.sleep(0.3)  # 클릭 간격
                break
    n += 1

    screenshot_file = f"{n}.png"
    screenshot_path = os.path.join(screenshot_dir, screenshot_file)
    driver.save_screenshot(screenshot_path)
    driver.find_element(By.CSS_SELECTOR, ".m_lotteryNumPager_btn.m_lotteryNumPager_btn__next").click()
    print(f"{n}번째 조합 선택 완료")
    time.sleep(1)

driver.quit()
