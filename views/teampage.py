import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from flask import Flask, Blueprint, render_template, jsonify,request,session

team_page = Blueprint('team', __name__, static_folder="static", template_folder="templates", url_prefix="/team")

uri="mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true"
client=MongoClient("mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true")
db=client.Splint2_Database
teams_col=db.teams

options=Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shu-usage')

driver=webdriver.Chrome(options=options)

#팀 홈페이지 정보
team_homepage={
     "KIA 타이거즈": "https://tigers.co.kr/",
     "롯데 자이언츠": "https://www.giantsclub.com/html/",
     "LG 트윈스": "https://www.lgtwins.com/service/html.ncd?view=/pc_twins/twins_main/twins_main",
     "두산 베어스": "https://www.doosanbears.com",
     "삼성 라이온즈": "https://www.samsunglions.com",
     "KT 위즈": "https://www.ktwiz.co.kr",
     "한화 이글스": "https://www.hanwhaeagles.co.kr",
     "키움 히어로즈": "https://www.heroesbaseball.co.kr",
     "NC 다이노스": "https://www.ncdinos.com",
     "SSG 랜더스": "https://www.ssglanders.com"
}

#팀 연고지 정보
team_location={
    "KIA 타이거즈": "광주광역시",
    "롯데 자이언츠": "부산광역시",
    "LG 트윈스": "서울특별시",
    "두산 베어스": "서울특별시",
    "삼성 라이온즈": "대구광역시",
    "KT 위즈": "수원시",
    "한화 이글스": "대전광역시",
    "키움 히어로즈": "서울특별시",
    "NC 다이노스": "창원시",
    "SSG 랜더스": "인천광역시"
}

#팀당 우승횟수 
team_win={
    "KIA 타이거즈": "12회(1983, 1986~1989, 1991, 1993, 1996, 1997, 2009, 2017, 2024)",
    "롯데 자이언츠": "2회(1984, 1992)",
    "LG 트윈스": "3회(1990,1994,2023)",
    "두산 베어스": "6회(1982, 1995, 2001, 2015, 2016, 2019)",
    "삼성 라이온즈": "8회(1985, 2002, 2005, 2006, 2011~2014)",
    "KT 위즈": "1회(2021)",
    "한화 이글스": "1회(1999)",
    "키움 히어로즈": "-",
    "NC 다이노스": "1회(2020)",
    "SSG 랜더스": "5회(2007, 2008, 2010, 2018, 2022)"
}

#팀 색 가져오기
team_color={
    "KIA 타이거즈": "#EA0029",
    "롯데 자이언츠": "#041E42",
    "LG 트윈스": "#C30452",
    "두산 베어스": "#1A1748",
    "삼성 라이온즈": "#074CA1",
    "KT 위즈": "#000000",
    "한화 이글스": "#FC4E00",
    "키움 히어로즈": "#570514",
    "NC 다이노스": "#315288",
    "SSG 랜더스": "#CE0E2D"
}

team_code_id={
    "KIA 타이거즈": "HT",
    "롯데 자이언츠": "LT",
    "LG 트윈스": "LG",
    "두산 베어스": "OB",
    "삼성 라이온즈": "SS",
    "KT 위즈": "KT",
    "한화 이글스": "HH",
    "키움 히어로즈": "WO",
    "NC 다이노스": "NC",
    "SSG 랜더스": "SK"
}

headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

#동적 반복
for team_name in team_homepage.keys():
   
    query=f"{team_name}"
    uri=f"https://search.naver.com/search.naver?query={query}"
    res=requests.get(uri,headers=headers)
    soup=BeautifulSoup(res.text,'html.parser')

#팀 이미지 가져오기
    team_image=soup.select_one('.api_cs_wrap .thmb img')
    image_uri=team_image['src']if team_image and team_image.has_attr('src')else ""

#팀당 감독 들고오기
    team_manage=soup.select_one('.detail .class_etcinfo_sportsgame_managerTitle + dd a')
    manager=team_manage.get_text(strip=True) if team_manage else ""


    # team_id=team_code_id[team_name]
    # kbo_uri=f"https://www.koreabaseball.com/Schedule/Schedule.aspx?seriesId=0&teamId={team_id}"
    # driver.get(kbo_uri)
    # time.sleep(2)
    # html=driver.page_source
    # soup=BeautifulSoup(html,'html.parser')
    # sows=soup.select('table.tbl>tbody>tr')

    # schedule_list=[]
    # for row in rows:
    #     cols=row.find_all("td")
    #     if len(cols)>=5:
            

#팀 별 경기일정 가져오기 
    team_id=team_code_id[team_name]
    uri=f"https://www.koreabaseball.com/Schedule/Schedule.aspx?seriesId=0&teamId={team_id}"
    driver.get(uri)
    time.sleep(2)

    soup=BeautifulSoup(driver.page_source, 'html.parser')
    rows=soup.select('table.tbl >tbody>tr')

    schedule_list=[]
    current_date=""

    for row in rows:
        tds = row.find_all("td")
    
    # 최소한 날짜, 시간, 팀1, vs, 팀2가 있어야 함
    
        if 'day' in tds[0].get("class", []):
            current_date = tds[0].get_text(strip=True)
            time_ = tds[1].get_text(strip=True)
            team1 = tds[2].get_text(strip=True)
            team2 = tds[4].get_text(strip=True)
        else:
            time_ = tds[0].get_text(strip=True)
            team1 = tds[1].get_text(strip=True)
            team2 = tds[3].get_text(strip=True)

        short_name=team_name.split()[0].replace(" ","")
        if short_name not in (team1+team2).replace(" ",""):
            continue

        game = {
            "date": current_date,
            "time": time_,
            "teams": f"{team1}{team2}"
            }
        
        schedule_list.append(game)

    doc={
        "team_name":team_name,
        "team_image":image_uri,
        "team_location":team_location[team_name],
        "team_manage":manager,
        "team_win":team_win[team_name],
        "team_color":team_color[team_name],
        "team_homepage":team_homepage[team_name],
        "team_schedule": schedule_list
    }
    # teams_col.replace_one({"team_name":team_name},doc,upsert=True)


#정보 연결 
@team_page.route('/<teamName>')
def team_detail(teamName):
    #팀 정보 객체 찾아서 리디렉션과 동시에 던져줌
    team_data=teams_col.find_one({'team_name' : teamName})
    return render_template("teampage.html",team = team_data)

@team_page.route('/<teamName>/comment', methods =['POST'])
def post_comment():

    # 입력받은 Comment 데이터 가져오기
    input_comment = request.form['comment']

    #세션된 ID,닉네임 가져오기
    target_user = session.get('id')
    Nickname = session.get('nickname')

    # DB에 도큐멘트 형태로 변환
    doc = {
        'id' : target_user, 'nickname' : Nickname, 'comment' : input_comment } #좋아요 추가시 user db와 이름혼동문제 
    
    # DB에 아이디, 닉네임과 댓글 내용 데이터 저장
    db.team_comment.insert_one(doc)

    # 댓글 등록 성공 (응답 성공 반환)
    return jsonify( {'result': 'success','msg' : '댓글 등록 성공!', 'nickname' : Nickname, 'url' : '/<teamName>'})
    
    # #id와 nickname을 세션 등록
    # session['id'] = target_user['id']
    # session['nickname'] = nickname
    # return jsonify({'result': 'success', 'msg' : nickname + '님 환영합니다.', 'nickname' : nickname, 'url' : '/'})
