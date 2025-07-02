import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"        # TensorFlow 로그 제거
os.environ["DISABLE_TFLITE_DELEGATE"] = "1" 
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from flask import Flask, Blueprint, render_template, jsonify,request,session
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


team_page = Blueprint('team', __name__, static_folder="static", template_folder="templates", url_prefix="/team")

uri="mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true"
client=MongoClient("mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true")

#db 10개 생성
db=client.Splint2_Database
teams_col1=db.kia_player
teams_col2=db.lotte_player
teams_col3=db.lg_player
teams_col4=db.dosan_player
teams_col5=db.samsung_player
teams_col6=db.kt_player
teams_col7=db.hanhwa_player
teams_col8=db.kiwoom_player
teams_col9=db.nc_player
teams_col10=db.ssg_player

#셀레니움 기본 설정 
options=Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shu-usage')

driver=webdriver.Chrome(options=options)


headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

collections=[
    db.kia_player, db.lotte_player, db.lg_player, db.dosan_player, db.samsung_player,
    db.kt_player, db.hanhwa_player, db.kiwoom_player, db.nc_player, db.ssg_player
]
team_name=['KIA','롯데','LG','두산','삼성','KT','한화','키움','NC','SSG']
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
#kbo에서 선수 리스트 가져오기 
def player_list():
    url = "https://www.koreabaseball.com/Player/Register.aspx"
    driver.get(url)
    time.sleep(1)


    # team_id=['HT','LT','LG','OB','SS','KT','HH','WO','NC','SK']
    team_name=['KIA','롯데','LG','두산','삼성','KT','한화','키움','NC','SSG']

# 팀별 반복
    for idx, (tid,tname) in enumerate(zip(team_id, team_name)):
        try:
            # 팀 버튼 클릭
            team_btn = driver.find_element(By.XPATH, f'//li[@data-id="{tid}"]/a')
            team_btn.click()
            time.sleep(2)

            # HTML 파싱
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            rows = soup.select('[class^="tNData"] tbody tr')

            players=[]

            # 선수 정보 뽑아옴 
            now = time.time()
            for row in rows:
                cols = row.select('td')
                if len(cols) >= 3:
                    player_dict={
                        "name": cols[1].text.strip(),     # 이름
                        "number": cols[0].text.strip(),   # 번호
                        "toota": cols[2].text.strip(),    # 투타
                        "birth": cols[3].text.strip(),    # 생년월일
                        "spec": cols[4].text.strip(),
                        "lastUpdatedTime": now
                    }
                    players.append(player_dict)

            # collections[idx].delete_many({})
            # collections[idx].insert_many(players)

        except Exception as e:
            print(f"{tname} 처리 중 오류 발생: {e}")
    driver.quit()

#선수 아이디 mongoDB 삽입  (한화)
def hanhwa_id_list():
    hanhwa_id=['82211', '73750', '85570', '74745', '95409', '72108' ,'78745','84510','82374', '93112','72139',
    '52701', '65056', '61666', '54729', '55730', '63765', '53754', '65769', '54755', '67703','65707', '54768', '76715'
    '78288', '76812', '64006', '65703', '69737', '62700', '79192',
    '53764', '54795', 
    '55703', '66657', '66704', '69766' ,'50707', '68700', '79608'
    ]
    hanhwa_player=list(teams_col7.find().sort("_id",1)) #순서대로 저장되게 설정 
    
    if len(hanhwa_player)!=len(hanhwa_id):
        print("DB 선수 수:", db.hanhwa_player.count_documents({}))
        print("playerId 수:", len(hanhwa_id))

        print("선수 수와 아이디 수가 다름")
        return 
    
    for player,pid in zip (hanhwa_player, hanhwa_id):
        teams_col7.update_one(
            {"_id": player["_id"]},
            {"$set":{"playerId": pid}}
        )

#한화 선수 따기 
def hanhwa_image_list():
    players=list(teams_col7.find({"playerId":{"$exists":True}}))

    for player in players:
        pid=player.get("playerId")
        
        uri=f"https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId={pid}"
        driver.get(uri)
        time.sleep(0.5)

        soup=BeautifulSoup(driver.page_source,'html.parser')
        img_1=soup.select_one('.player_info .photo img')
        img_uri=img_1['src']if img_1 and img_1.has_attr('src')else""
        teams_col7.update_one(
            {"_id":player["_id"]},
            {"$set":{"img":img_uri}}
        )


# hanhwa_id_list()
# player_list()
# hanhwa_image_list()