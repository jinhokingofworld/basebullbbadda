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

#kbo에서 선수 리스트 가져오기 
def player_list():
    url = "https://www.koreabaseball.com/Player/Register.aspx"
    driver.get(url)
    time.sleep(1)


    team_id=['HT','LT','LG','OB','SS','KT','HH','WO','NC','SK']
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

            collections[idx].delete_many({})
            collections[idx].insert_many(players)

        except Exception as e:
            print(f"{tname} 처리 중 오류 발생: {e}")
    driver.quit()


player_list()