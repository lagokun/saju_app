import os
from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI  # OpenAI 라이브러리 임포트 수정
from dotenv import load_dotenv
load_dotenv()

app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
)

# OpenAI API 키 설정
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # 여기에 실제 API 키를 입력하세요.# 환경 변수에서 API 키 로드

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/saju')
def saju():
    return render_template('index.html')

@app.route('/compatibility')
def compatibility():
    return render_template('compatibility.html')

@app.route('/result', methods=['POST'])
def result():
    # 사용자 입력 받기

    birth_year = request.form.get('birth_year')
    birth_month = request.form.get('birth_month')
    birth_day = request.form.get('birth_day')
    
    # 생년월일 유효성 검사
    if not all([birth_year, birth_month, birth_day]):
        return "생년월일을 모두 입력해주세요.", 400
    
    birth_date = f"{birth_year}년 {birth_month}월 {birth_day}일"
    
    birth_period = request.form.get('birth_period')
    birth_hour = request.form.get('birth_hour')
    birth_minute = request.form.get('birth_minute')
    
    # 태어난 시간 유효성 검사 및 처리
    if birth_period == '모름':
        birth_time = "모름"
    else:
        if not all([birth_period, birth_hour, birth_minute]):
            return "태어난 시간을 모두 입력해주세요.", 400
        birth_time = f"{birth_period} {birth_hour}시 {birth_minute}분"
    
    gender = request.form.get('gender')
    name = request.form.get('name')
    mbti = request.form.get('mbti')
    blood_type = request.form.get('blood_type')
    wealth_luck = '재물운' if request.form.get('wealth_luck') else None
    marriage_luck = '결혼운' if request.form.get('marriage_luck') else None
    love_luck = '연애운' if request.form.get('love_luck') else None

    # 선택된 운세 항목
    selected_lucks = [luck for luck in [wealth_luck, marriage_luck, love_luck] if luck]
    if selected_lucks:
        lucks_text = ', '.join(selected_lucks)
    else:
        lucks_text = '없음'

    # GPT에 보낼 프롬프트 생성
    prompt = f"""
    아래의 정보를 바탕으로 사주를 풀이해 주세요.

    생년월일: {birth_date}
    태어난 시간: {birth_time}
    성별: {gender}
    이름: {name}
    MBTI: {mbti}
    혈액형: {blood_type}
    분석 항목: {lucks_text}

    사주는 한국 전통 사주 이론에 따라 해석해 주세요. 각 항목에 대해 자세하게 작성해 주세요.
    모든 섹션은 간단하게 2-3줄 정도로 작성해 주세요.

    출력 결과는 다음 섹션을 반드시 포함해야 합니다:
    ### 기본 사주 구성
    ### 재물운
    ### 결혼운
    ### 연애운
    ### 총평
    ### 향후 계획

    ### 향후 계획
    1월 중 webex 봇을 통한 일일 사주받기와 일일 일정 알림 기능이 추가될 예정입니다. 사주뺌 많관부🐍
    """

    try:
        # OpenAI GPT API 호출
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 한국의 전통 사주 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3,
        )
        # GPT의 응답 받기
        gpt_response = response.choices[0].message.content.strip()
        gpt_response = gpt_response.lstrip()
        
        print("#####################################################")
        print(gpt_response)

    except Exception as e:
        gpt_response = f"오류가 발생했습니다: {str(e)}"

    return render_template('result.html', result=gpt_response)


@app.route('/compatibility_result', methods=['POST'])
def compatibility_result():
    # 첫 번째 사람 정보
    name1 = request.form.get('name1')
    birth_year1 = request.form.get('birth_year1')
    birth_month1 = request.form.get('birth_month1')
    birth_day1 = request.form.get('birth_day1')
    mbti1 = request.form.get('mbti1')
    
    # 두 번째 사람 정보
    name2 = request.form.get('name2')
    birth_year2 = request.form.get('birth_year2')
    birth_month2 = request.form.get('birth_month2')
    birth_day2 = request.form.get('birth_day2')
    mbti2 = request.form.get('mbti2')
    
    # 입력 유효성 검사
    if not all([name1, birth_year1, birth_month1, birth_day1,
                name2, birth_year2, birth_month2, birth_day2, mbti1, mbti2]):
        return "모든 필드를 입력해주세요.", 400
    
    birth_date1 = f"{birth_year1}년 {birth_month1}월 {birth_day1}일"
    birth_date2 = f"{birth_year2}년 {birth_month2}월 {birth_day2}일"
    
    # MBTI가 "모름"인 경우 None으로 설정
    mbti1_display = mbti1 if mbti1 != "모름" else "알 수 없음"
    mbti2_display = mbti2 if mbti2 != "모름" else "알 수 없음"
    
    # GPT에 보낼 프롬프트 생성
    prompt = f"""
    두 사람의 생년월일, 이름, 그리고 MBTI 유형을 바탕으로 궁합을 풀이해 주세요.

    사람 1:
    이름: {name1}
    생년월일: {birth_date1}
    MBTI: {mbti1_display}

    사람 2:
    이름: {name2}
    생년월일: {birth_date2}
    MBTI: {mbti2_display}

    궁합을 한국 전통 사주 이론과 MBTI 유형을 고려하여 분석해 주세요. 다음 섹션을 반드시 포함해야 합니다:
    ### 기본 정보
    ### 사주 기반 상호 호환성
    ### MBTI 기반 상호 호환성
    ### 장점과 단점
    ### 총평

    ### 향후 사주뺌 계획
    1월 중 webex 봇을 통한 일일 사주, 일일 일정 알림 기능이 추가될 예정입니다. 사주뺌 많관부🐍
    """

    try:
        # OpenAI GPT API 호출
        response = client.chat.completions.create(
            model="gpt-4",  # 모델 이름 수정 (예: "gpt-4" 사용)
            messages=[
                {"role": "system", "content": "당신은 한국의 전통 사주 전문가이자 MBTI 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        # GPT의 응답 받기
        gpt_response = response.choices[0].message.content.strip()
        gpt_response = gpt_response.lstrip()

        print("#####################################################")
        print(gpt_response)

    except Exception as e:
        gpt_response = f"오류가 발생했습니다: {str(e)}"

    return render_template('compatibility_result.html', result=gpt_response)

# if __name__ == '__main__':
#     # 디버그 모드에서 실행 (배포 시에는 False로 설정)
#     app.run(debug=False)
