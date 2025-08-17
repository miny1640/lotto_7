import pandas as pd
import numpy as np
import csv
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

CSV_FILE = "lotto7_results.csv"

def scale_numbers(file_name, scaler):
    # 1. 데이터 로드
    df = pd.read_csv(file_name)

    # 회차, 당첨번호 컬럼이 있다고 가정하고, 번호만 추출
    numbers = df.iloc[:, 1:8].values  # 예: 1~7번 열이 당첨번호

    # 정규화
    scaled_numbers = scaler.fit_transform(numbers)
    return scaled_numbers

def predict_numbers(scaled_numbers, sequence_length, scaler, predict_num):
    # 2. 학습용 데이터 생성
    x, y = [], []
    for i in range(len(scaled_numbers) - sequence_length):
        x.append(scaled_numbers[i:i+sequence_length])
        y.append(scaled_numbers[i+sequence_length])
    x = np.array(x)
    y = np.array(y)

    # 3. LSTM 모델 구성
    model = Sequential()
    model.add(LSTM(64, activation='relu', input_shape=(sequence_length, 7)))
    model.add(Dense(predict_num))
    model.compile(optimizer='adam', loss='mse')

    # 4. 모델 학습
    model.fit(x, y, epochs=200, batch_size=8, verbose=1)

    # 5. 다음 회차 예측
    last_sequence = scaled_numbers[-sequence_length:]
    last_sequence = np.expand_dims(last_sequence, axis=0)
    predicted_scaled = model.predict(last_sequence)

    # 역정규화
    predicted_numbers = scaler.inverse_transform(predicted_scaled)[0]

    # 반올림, 정수 변환, 중복 제거, 정렬
    predicted_numbers = np.unique(np.round(predicted_numbers).astype(int))
    predicted_numbers = np.clip(predicted_numbers, 1, 37)  # 로또7 번호 범위 제한
    predicted_numbers = sorted(predicted_numbers)

    # 다음 회차 예측 번호
    return predicted_numbers

def write_to_csv(results, csv_file):
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # CSV 파일 헤더 작성
        writer.writerow([f"number{i}" for i in range(1, 8)])
        # 각 예측 조합을 한 행으로 저장
        writer.writerows(results)

def main():
    scaler = MinMaxScaler(feature_range=(0, 1))

    file_name = CSV_FILE
    sequence_length = 20 # 최근 20회 당첨 번호로 다음 회차 예측
    predict_num = 7 # 7개의 번호 예측

    scaled_numbers = scale_numbers(file_name, scaler)

    lotto7_predictions = []
    for _ in range(5):
        prediction = predict_numbers(scaled_numbers, sequence_length, scaler, predict_num)
        lotto7_predictions.append(prediction)

    # 예측 결과를 CSV 파일로 저장
    output_filename = "lotto7_lstm_predictions.csv"
    write_to_csv(lotto7_predictions, output_filename)

# 실행
if __name__ == "__main__":
    main()
