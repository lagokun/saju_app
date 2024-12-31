import os
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
    song_list = [
        '이루리 - 우주소녀', '아파트 - 윤수일', '한걸음 - 겸빛, 윤슬', '너와의 모든 지금 - 재쓰비 (JAESSBEE)',
        '새해 복 - 장기하와 얼굴들', '듣기만 해도 성공하는 음악 - 조빈', '나는 자기 암시 - 스위스',
        '이루리 - 우주소녀', '행복 (Happiness) - Red Velvet(레드벨벳)', 'JACKPOT - 블락비 (Block B)',
        '로또당첨송 - 썬차일드', '좋아합니다 - DAY6 (데이식스)', '내가 제일 잘 나가 - 2NE1',
        '돈벼락 - 김필', '나는 행복합니다 - 윤향기', 'Happy - 태연 (TAEYEON)',
        '파이팅 해야지 (Feat. 이영지) - 부석순 (SEVENTEEN)', 'SMILEY (Feat. BIBI) - YENA (최예나)',
        '대박이야! - 대성', 'Dreams Come True - aespa', '퀸카 (Queencard) - (여자)아이들',
        'Forever Young - BLACKPINK', '아주 NICE - 세븐틴 (SEVENTEEN)', 'HAPPY - DAY6 (데이식스)',
        '가보자 - Xydo (시도)', '반짝, 빛을 내 - 윤하 (YOUNHA)', '고민보다 Go - 방탄소년단',
        '소확행 - 임창정', '아모르 파티 - 김연자', '니 팔자야 - 노라조', '시작 - 가호 (Gaho)',
        'Go! - 도겸', 'Butterfly - 러브홀릭스', '슈퍼스타 - 이한철',
        'Bravo My Life (브라보 마이 라이프) - 봄여름가을겨울', '장가가고 싶은 남자 시집가고 싶은 여자 - 장미여관',
        '행복의 주문 - 커피소년', '성공 (Feat. JYP) - 유브이 (UV)', '수고했어, 오늘도 - 옥상달빛',
        '돈에 깔려 죽어 (Feat. Ja Mezz) - 수퍼비 (SUPERBEE), 트웰브 (twlv)', '엄지 척 - 홍진영',
        '결혼해줄래 - 이승기', '꽃길 - BIGBANG (빅뱅)', '꽃길만 걷게 해줄게 - 데이브레이크 (DAYBREAK)',
        '승천가 - Stray Kids (스트레이 키즈)', '별일 없이 산다 - 장기하와 얼굴들', '효도합시다 (prod. 플레이사운드) - 정동원',
        'Hello Future - NCT DREAM', '기적 (Duet With 이소은) - 김동률', '주인공 - 거북이',
        '내게 애인이 생겼어요 - 나훈아', '걱정 마라 지나간다 - 조항조', 'The Greatest Beginning - 신해철',
        'Number 1 - 이달의 소녀', 'Gucci - 제시 (Jessi)', '백세인생 - 이애란', 'GOLD - Wanna One (워너원)', 'MONEY - 리사 (LISA)',
        '행복 - H.O.T.', '애인만들기 - SS501', 'Beautiful Beautiful - 온앤오프 (ONF)', '여행 - 볼빨간사춘기', '거침없이 - 부석순 (SEVENTEEN)',
        'DOOL - 미노이 (meenoi)', '시작이 좋아 (feat. 강민희 Of 미스에스) - 버벌진트', '말하는 대로 - 처진 달팽이 (유재석 & 이적)', '꽃길 (Prod. By ZICO) - 김세정',
        '좋은일이 있을거야 - 제이레빗(J Rabbit)', '작전명 청-춘! - 잔나비', '지금 이 순간 -뮤지컬 지킬 앤 하이드 OST', '참고사항 - 이무진', '오르트구름 - 윤하',
        '내게 사랑이 뭐냐고 물어본다면 - 로이킴', '대양 - 라이프앤타임', '호랑이 - 라이프앤타임', '찬란 - 나상현씨밴드', '버터플라이 - 러브홀릭스', '행운을 빌어요 - 페터톤스'
    ]
    
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
    newyear_luck = '재물운' if request.form.get('2025_luck') else None
    job_luck = '직장운' if request.form.get('job_luck') else None
    wealth_luck = '재물운' if request.form.get('wealth_luck') else None
    marriage_luck = '결혼운' if request.form.get('marriage_luck') else None
    love_luck = '연애운' if request.form.get('love_luck') else None

    # 선택된 운세 항목
    selected_lucks = [luck for luck in [newyear_luck, job_luck, wealth_luck, marriage_luck, love_luck] if luck]
    if selected_lucks:
        lucks_text = ', '.join(selected_lucks)
    else:
        lucks_text = '없음'

    # song_list에서 2개 무작위 선택
    selected_songs = random.sample([song for song in song_list if song], 2)  # 빈 문자열 제거

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
    ### 2025년 신년운세 
    ### 직장운
    ### 재물운
    ### 결혼운
    ### 연애운
    ### 총평
    ### 향후 계획
    ### 2025년 새해 노래 추천
    🎵{selected_songs[0]}
    🎵{selected_songs[1]}
    ### 홍보
    아마따 에이전트를 통한 오늘 운세와 일정 알림 기능이 추가될 예정입니다.\n(Webex 사용자 추가 -> "아마따 에이전트" 검색!)
    """

    try:
        # OpenAI GPT API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 모델 이름 수정 (오타 수정)
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
    모든 섹션은 간단하게 2-3줄 정도로 작성해 주세요.

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
    ### 홍보
    아마따 에이전트를 통한 오늘 운세와 일정 알림 기능이 추가될 예정입니다.\n(Webex 사용자 추가 -> "아마따 에이전트" 검색!)
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
#     app.run(debug=True)
