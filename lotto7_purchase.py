import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# ===== CSV 읽기 =====
csv_file = "lotto7_lstm_predictions.csv"
df = pd.read_csv(csv_file)
predictions = df.values.tolist()

# ===== Chrome 드라이버 설정 =====
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 종료 안 함
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)

# ===== 로또7 구매 페이지 열기 =====
driver.get("https://www.takarakuji-official.jp/ec/?__ope=%E3%83%AD%E3%83%88&__fromScreenId=SC_WMA_SP_001#loto")

time.sleep(5)  # 페이지 로딩 대기

driver.find_element(By.XPATH, '//a[@onclick="document.loto7FForm.submit(); return false;"]').click()
time.sleep(10)

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
    driver.find_element(By.CSS_SELECTOR, ".m_lotteryNumPager_btn.m_lotteryNumPager_btn__next").click()
    time.sleep(1)

driver.find_element(By.CSS_SELECTOR, ".m_btn.m_infoPrice_btn.m_btn__block").click()
time.sleep(5)

driver.find_element(By.XPATH, '//a[@onclick="document.ecCartPaymentForm.formBtn.click(); return false;"]').click()
time.sleep(5)

# ===== 안내 메시지 =====
driver.execute_script("""
    alert("번호 선택이 완료되었습니다.\\n로그인 및 결제는 직접 진행하세요.");
""")
print("✅ 번호 선택 완료. 결제는 직접 진행하세요.")
# time.sleep(60)
# driver.quit()
