import pandas as pd
from datetime import datetime
import sys  # 프로그램 종료를 위한 모듈

# CSV 파일 불러오기
file_path = './dataset/crawled/yinyang_calendar.csv'
df = pd.read_csv(file_path)


# 종료 여부 체크 함수
def check_for_exit(user_input):
    if user_input.lower() == "종료":
        print("프로그램을 종료합니다.")
        sys.exit()


# 날짜 입력 형식을 체크하는 함수
def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# 사용자 입력 받기
def get_user_input():
    # 안내 메시지 출력
    print("대화형 모드에 오신 것을 환영합니다! '종료'라고 입력하면 대화가 종료됩니다.")
    
    # 날짜 입력 받기
    date_str = input("날짜를 입력하세요 (형식: YYYY-MM-DD): ")
    while not is_valid_date(date_str):
        check_for_exit(date_str)  # 종료 체크
        print("날짜 형식이 올바르지 않습니다. 다시 입력하세요.")
        date_str = input("날짜를 입력하세요 (형식: YYYY-MM-DD): ")
    
    # 성별 입력 받기
    gender = input("성별을 입력하세요 (남자/여자): ")
    while gender not in ["남자", "여자"]:
        check_for_exit(gender)  # 종료 체크
        print("성별은 '남자' 또는 '여자'만 가능합니다.")
        gender = input("성별을 입력하세요 (남자/여자): ")
    
    return date_str, gender


# 해당 날짜에 해당하는 오행 값 출력
def display_elements_for_date(date_str):
    # 'date' 열에서 입력한 날짜와 일치하는 행을 찾습니다
    if date_str in df['date'].values:
        row = df[df['date'] == date_str].iloc[0]
        date = [row['yeonju'], row['wolju'], row['ilju']]
        wood_num = row['wood']
        fire_num = row['fire']
        water_num = row['water']
        earth_num = row['earth']
        metal_num = row['metal']
        return wood_num, fire_num, water_num, earth_num, metal_num, date
    else:
        return None


# 메인 로직
def generate_result(date_str, gender):
    # 오행 값 가져오기
    elements = display_elements_for_date(date_str)
    
    if elements is not None:
        wood_num, fire_num, water_num, earth_num, metal_num, date = elements
        result = f"사주에 따른 자원오행이 목은 {wood_num}개, 화는 {fire_num}개, 수는 {water_num}개, 토는 {earth_num}개, 금은 {metal_num}개일 때, 이 사주를 보완하는 한국 {gender} 이름 짓고 뜻 풀이해줘"
        return result, date
    else:
        return f"{date_str}에 해당하는 데이터가 없습니다."
