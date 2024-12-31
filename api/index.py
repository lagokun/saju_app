import os
import json
import random
from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI  # OpenAI 라이브러리 임포트 수정
# from dotenv import load_dotenv
# load_dotenv()

app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
)

# OpenAI API 키 설정
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # 여기에 실제 API 키를 입력하세요.# 환경 변수에서 API 키 로드

PROMOTION_MESSAGE = """
### [홍보 메시지]
방금 본 2025 신년운세, 일주일 뒤면 까먹을걸요?
매일매일 오늘의 운세, 행운의 메시지를 받아보고 싶으신가요?✨
할일 관리 에이전트 '아마따 에이전트'에 곧 기능이 추가될 예정이에요!
아마따 에이전트로 오늘 하루 대화 요약, 할일 관리를 시작하시고 잠시만 기다려주세요!⏳

📝아마따 에이전트 등록 방법
1. webex 방에 "아마따 에이전트" 추가
2. @아마따 등록
3. 18시마다 대화 자동 요약, 할일이 정리되어 메시지가 옵니다.
🔒아마따 에이전트는 대화 내용을 저장하지 않습니다. 안심하고 사용하세요!

아마따 에이전트 문의: AI Tech Lab 박주혜 프로
"""

# songs.json 파일 로드
song_json_path = os.path.join(app.static_folder, 'json', 'song.json')
with open(song_json_path, 'r', encoding='utf-8') as f:
    SONG_LIST = json.load(f)

# song_list = [
#     '', '', '',
#     '', '', '',
#     '', '',
#     '', '', '퀸카 (Queencard) - (여자)아이들',
#     'Forever Young - BLACKPINK', '아주 NICE - 세븐틴 (SEVENTEEN)', 'HAPPY - DAY6 (데이식스)',
#     '가보자 - Xydo (시도)', '반짝, 빛을 내 - 윤하 (YOUNHA)', '고민보다 Go - 방탄소년단',
#     '소확행 - 임창정', '아모르 파티 - 김연자', '니 팔자야 - 노라조', '시작 - 가호 (Gaho)',
#     'Go! - 도겸', 'Butterfly - 러브홀릭스', '슈퍼스타 - 이한철',
#     'Bravo My Life (브라보 마이 라이프) - 봄여름가을겨울', '장가가고 싶은 남자 시집가고 싶은 여자 - 장미여관',
#     '행복의 주문 - 커피소년', '성공 (Feat. JYP) - 유브이 (UV)', '수고했어, 오늘도 - 옥상달빛',
#     '돈에 깔려 죽어 (Feat. Ja Mezz) - 수퍼비 (SUPERBEE), 트웰브 (twlv)', '엄지 척 - 홍진영',
#     '결혼해줄래 - 이승기', '꽃길 - BIGBANG (빅뱅)', '꽃길만 걷게 해줄게 - 데이브레이크 (DAYBREAK)',
#     '승천가 - Stray Kids (스트레이 키즈)', '별일 없이 산다 - 장기하와 얼굴들', '효도합시다 (prod. 플레이사운드) - 정동원',
#     'Hello Future - NCT DREAM', '', '',
#     '', '', '',
#     '', '', '', '', '',
#     '', '', '', '', '',
#     '', '', '', '',
#     '', '', '', '', '',

# ]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/saju')
def saju():
    return render_template('index.html')

@app.route('/compatibility')
def compatibility():
    return render_template('compatibility.html')

@app.route('/newyearsong')
def newyearsong():
    recommended_songs = random.sample(SONG_LIST, 1)
    return render_template('newyearsong.html', songs=recommended_songs)

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
    
    # 운세 항목 처리
    luck_mapping = {
        '2025_luck': '2025년 신년운세',
        'job_luck': '직장운',
        'wealth_luck': '재물운',
        'marriage_luck': '결혼운',
        'love_luck': '연애운'
    }
    
    selected_lucks = [label for key, label in luck_mapping.items() if request.form.get(key)]
    
    # 운세 텍스트 생성
    if selected_lucks:
        lucks_text = ', '.join(selected_lucks)
    else:
        lucks_text = '없음'
    
    # 기본적인 prompt 정보
    base_prompt = f"""
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
    """

    # 포함할 섹션 동적으로 추가
    sections = [
        "### 기본 사주 구성"
    ]
    
    # 섹션 매핑
    section_mapping = {
        '2025년 신년운세': "### 2025년 신년운세",
        '직장운': "### 직장운",
        '재물운': "### 재물운",
        '결혼운': "### 결혼운",
        '연애운': "### 연애운",
    }
    
    for luck in selected_lucks:
        sections.append(section_mapping[luck])
    
    # 항상 포함되어야 하는 섹션
    sections.extend([
        "### 총평",
        "### 향후 계획"
    ])
    
    # 섹션을 prompt에 추가
    sections_text = "\n".join(sections)
    prompt = base_prompt + "\n" + sections_text.replace("새해 노래 추천", "").replace("### 2025년 새해 노래 추천", "")
    
    # 노래 추천이 선택된 경우 추가 처리
    if '새해 노래 추천' in selected_lucks:
        selected_songs = random.sample(song_list, 2)  # 중복 없이 2개 선택
    else:
        recommand_song = ""
    
    try:
        # OpenAI GPT API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 모델 이름 수정 (오타 수정)
            messages=[
                {"role": "system", "content": "당신은 한국의 전통 사주 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.1,
        )
        # GPT의 응답 받기
        gpt_response = response.choices[0].message.content.strip()
        gpt_response = gpt_response.lstrip()

    except Exception as e:
        gpt_response = f"오류가 발생했습니다: {str(e)}"
        
    # 노래 추천이 있을 경우 추가
    full_response = f"{gpt_response}{recommand_song}\n{PROMOTION_MESSAGE}"
    return render_template('result.html', result=full_response)

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
    모든 섹션은 적당하게 4-5줄 정도로 작성해 주세요.

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
    """

    try:
        # OpenAI GPT API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 모델 이름 수정 (예: "gpt-4" 사용)
            messages=[
                {"role": "system", "content": "당신은 한국의 전통 사주 전문가이자 MBTI 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.1,
        )

        # GPT의 응답 받기
        gpt_response = response.choices[0].message.content.strip()
        gpt_response = gpt_response.lstrip()

        # print("#####################################################")
        # print(gpt_response)

    except Exception as e:
        gpt_response = f"오류가 발생했습니다: {str(e)}"
        
    full_response = f"{gpt_response}\n{PROMOTION_MESSAGE}"
    
    return render_template('compatibility_result.html', result=full_response)

# if __name__ == '__main__':
#     # 디버그 모드에서 실행 (배포 시에는 False로 설정)
#     app.run(debug=True)
