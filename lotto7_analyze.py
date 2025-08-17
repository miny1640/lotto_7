import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# CSV 파일 경로
CSV_FILE = "lotto7_results.csv"

# CSV 파일 읽기
df = pd.read_csv(CSV_FILE)

# 번호1~번호7 열만 추출
main_numbers = df[["draw_num1", "draw_num2", "draw_num3", "draw_num4", "draw_num5", "draw_num6", "draw_num7"]]

# 하나의 리스트로 번호를 모두 수집
all_numbers = main_numbers.values.flatten()

# 등장 횟수 세기
counter = Counter(all_numbers)
sorted_counts = dict(sorted(counter.items()))

# 결과 출력
print("번호별 등장 횟수:")
for num, cnt in sorted_counts.items():
    print(f"{num:2d}번: {cnt}회")

# 히스토그램 그리기
plt.figure(figsize=(15, 6))
plt.bar(sorted_counts.keys(), sorted_counts.values(), color='skyblue')
plt.title('Number appearance(Lotto 7)', fontsize=16)
plt.xlabel('number', fontsize=12)
plt.ylabel('appearance', fontsize=12)
plt.xticks(range(min(sorted_counts), max(sorted_counts)+1))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
