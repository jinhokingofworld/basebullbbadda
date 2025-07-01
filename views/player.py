# import os
# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"        # TensorFlow 로그 제거
# os.environ["DISABLE_TFLITE_DELEGATE"] = "1" 
# import requests
# from bs4 import BeautifulSoup
# from pymongo import MongoClient
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import time
# from flask import Flask, Blueprint, render_template, jsonify,request,session
# from datetime import datetime

# team_page = Blueprint('team', __name__, static_folder="static", template_folder="templates", url_prefix="/team")

# uri="mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true"
# client=MongoClient("mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true")

# #db 10개 생성
# db=client.Splint2_Database
# teams_col1=db.kia_player
# teams_col2=db.lotte_player
# teams_col3=db.lg_player
# teams_col4=db.dosan_player
# teams_col5=db.samsung_player
# teams_col6=db.kt_player
# teams_col7=db.hanhwa_player
# teams_col8=db.kiwoom_player
# teams_col9=db.nc_player
# teams_col10=db.ssg_player

# #셀레니움 기본 설정 
# options=Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shu-usage')

# driver=webdriver.Chrome(options=options)

# team_code_id={
#     "KIA 타이거즈": "HT",
#     "롯데 자이언츠": "LT",
#     "LG 트윈스": "LG",
#     "두산 베어스": "OB",
#     "삼성 라이온즈": "SS",
#     "KT 위즈": "KT",
#     "한화 이글스": "HH",
#     "키움 히어로즈": "WO",
#     "NC 다이노스": "NC",
#     "SSG 랜더스": "SK"
# }

# headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# #팀 별 선수 이름 따오기
# def get_player(team_name):
#     team_id=team_code_id[team_name]
#     uri=f"https://www.koreabaseball.com/Player/Register.aspx?seriresId=0&teamId={team_id}"
#     driver.get("https://www.koreabaseball.com/Player/Register.aspx")
#     time.sleep(1.5)
#     soup=BeautifulSoup(driver.page_source,'html.parser')
#     players=soup.select('.row>table>tbody>tr')

#     players_list=[]
#     for player in players:
#         tds=player.find_all("td")
#         if len(tds)<5:
#             continue

#         number=tds[0].get_text(strip=True)
#         name=tds[1].get_text(strip=True)
#         toota=tds[2].get_text(strip=True)
#         birth=tds[3].get_text(strip=True)
#         spec=tds[4].get_text(strip=True)

#         playerdict={
#             "number":number,
#             "name":name,
#             "toota":toota,
#             "birth":birth,
#             "spec":spec
#         }
#         players_list.append(playerdict)
#     return players_list