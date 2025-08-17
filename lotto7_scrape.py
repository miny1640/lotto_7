from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, csv, re

BASE_URL = "https://www.mizuhobank.co.jp/takarakuji/check/loto"
LATEST_URL = f"{BASE_URL}/loto7/index.html"
FROMTO_URL_TEMPLATE = f"{BASE_URL}/backnumber/detail.html?fromto={{start}}_{{end}}&type=loto7"
CSV_FILE = "lotto7_results.csv"

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    return driver

def crawl_web_page(url, driver, wait_time):
    driver.get(url)
    time.sleep(wait_time)  # JS 렌더링 대기
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup

def get_loto7_numbers(soup):
    title = soup.find("h1").get_text(strip=True)
    print(f"📌 {title}")

    # 당첨번호 테이블 찾기
    result_block = soup.find("div", class_="js-lottery-backnumber-list")  # 테이블 블럭

    # 번호 테이블 찾기
    numbers_table = result_block.find("table")
    trs = numbers_table.find_all("tr")

    results = []
    # 번호 추출
    for tr in trs:
        td = tr.find("td")
        th = tr.find("th")
        if td and th:
            text = th.get_text(strip=True)
            match = re.search(r"第(\d+)回", text)
            round_no = match.group(1)
            draw_no = [td.get_text(strip=True) for td in tr.find_all("td")]
            results.append({
                "round": round_no,
                "draw_num1": draw_no[1],
                "draw_num2": draw_no[2],
                "draw_num3": draw_no[3],
                "draw_num4": draw_no[4],
                "draw_num5": draw_no[5],
                "draw_num6": draw_no[6],
                "draw_num7": draw_no[7],
                "bonus_num1": draw_no[8],
                "bonus_num2": draw_no[9]
            })
    
    return results

def get_draw_no(soup):
    title_element = soup.find("h3")
    if not title_element:
        print("타이틀 요소를 찾을 수 없습니다.")
        return None
    title = title_element.get_text(strip=True)
    # match = re.search(r"第(\d+)回", title)
    matches = re.findall(r"第(\d+)回", title)
    if matches:
        last_match = int(matches[-1])
        return last_match
    else:
        print("회차 번호를 찾을 수 없습니다.")
        return None

def write_to_csv(results, csv_file):
    fieldnames = ["round", "draw_num1", "draw_num2", "draw_num3", "draw_num4", "draw_num5", "draw_num6", "draw_num7", "bonus_num1", "bonus_num2"]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        # 데이터를 회차(round)의 내림차순으로 정렬하여 저장합니다.
        # 'round' 키의 값을 정수로 변환하여 비교합니다.
        sorted_results = sorted(results, key=lambda x: int(x['round']), reverse=True)
        writer.writerows(sorted_results)

def main():
    driver = get_driver()

    last_draw_soup = crawl_web_page(LATEST_URL, driver, 3)
    last_draw_no = get_draw_no(last_draw_soup)

    draw_numbers_url = FROMTO_URL_TEMPLATE.format(start=1, end=last_draw_no)
    draw_numbers_soup = crawl_web_page(draw_numbers_url, driver, 10)
    data = get_loto7_numbers(draw_numbers_soup)
    write_to_csv(data, CSV_FILE)

    driver.quit()    

# 실행
if __name__ == "__main__":
    main()
