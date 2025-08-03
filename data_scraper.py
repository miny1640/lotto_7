from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, csv, re

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    return driver

def crawl_web_page(url):
    driver = get_driver()
    driver.get(url)
    time.sleep(3)  # JS 렌더링 대기
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    return soup

def get_loto7_numbers_range(round_no_start, round_no_end):
    if round_no_start > round_no_end:
        temp = round_no_start
        round_no_start = round_no_end
        round_no_end = temp

    url = f"https://www.mizuhobank.co.jp/takarakuji/check/loto/backnumber/detail.html?fromto={round_no_start}_{round_no_end}&type=loto7"

    soup = crawl_web_page(url)

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
            match = re.search(r"第(\d+)回", th.get_text(strip=True))
            round_no = match.group(1)
            draw_no = [td.get_text(strip=True) for td in tr.find_all("td")]
            results.append({
                "round": round_no,
                "draw_numbers": ','.join(draw_no[1:8]),
                "donus_number": ','.join(draw_no[8:])
            })
    
    return results

def get_last_draw_no():
    url = "https://www.mizuhobank.co.jp/takarakuji/check/loto/loto7/index.html"
    soup = crawl_web_page(url)

    title = soup.find("h3").get_text(strip=True)
    match = re.search(r"第(\d+)回", title)

    return int(match.group(1))

def write_to_csv(results, csv_file):
    fieldnames = ["round", "draw_numbers", "donus_number"]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

# 실행
if __name__ == "__main__":
    csv_file = "lotto7_results.csv"
    data = get_loto7_numbers_range(1, get_last_draw_no())
    write_to_csv(data, csv_file)
