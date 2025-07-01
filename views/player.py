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

#기아타이거즈 정보 따오기
def kia_player():
    uri="https://tigers.co.kr/players/entry-status"
    driver.get(uri)
    time.sleep(1)

    soup=BeautifulSoup(driver.page_source,'html.parser')
    rows=soup.select('tbody>tr')
    kia_list=[]
    for row in rows:
        ths=row.find_all("th")
        name=ths[1].get_text(strip=True)

        tds=row.find_all("td")
        if len(tds)<6:
            continue
        position=tds[0].get_text(strip=True)
        number=tds[1].get_text(strip=True)
        toota=tds[2].get_text(strip=True)
        birth=tds[3].get_text(strip=True)
        height=tds[4].get_text(strip=True)
        weight=tds[5].get_text(strip=True)

        player_dict={
            "name":name,
            "position":position,
            "number":number,
            "toota":toota,
            "birth": birth,
            "height": height,
            "weight": weight
        }
        kia_list.append(player_dict)
    return kia_list

# teams_col1.insert_one({"kia_player":kia_player()})

#롯데 자이언츠 정보 따오기

#LG 트윈스 정보 따오기
# def lg_player():
#     uri="https://www.lgtwins.com/service/html.ncd?view=%2Fpc_twins%2Ftwins_player%2Ftwins_rosters&baRq=IN_DS&IN_DS.YEAR=&baRs=OUT_DS1%2COUT_DS2&actID=BR_RetrievePlayerRosters"
#     options.add_argument("--disable-gpu")
#     driver = webdriver.Chrome(options=options)
#     driver.get(uri)
#     time.sleep(1)

#     soup=BeautifulSoup(driver.page_source,'html.parser')
#     driver.quit()

#     rows=soup.select('.tab_content>.board_dic')
#     lg_list=[]
#     for row in rows:
#         image=soup.select_one('.header>.img_wrap img')
#         image_url = image['src']if image and image.has_attr('src')else ""
#         name=soup.select_one('.header .title h3')
#         name_id=name.get_text(strip=True) if name else""
#         ps=row.find_all("p")
#         if len(ps)<5:
#             continue
#         toota=ps[1].get_text(strip=True)
#         birth=ps[2].get_text(strip=True)
#         heightWeight=ps[3].get_text(strip=True)

#         player_dict={
#             "name":name_id,
#             "image":image_url,
#             "toota":toota,
#             "birth":birth,
#             "heightWeight":heightWeight
#         }
#         lg_list.append(player_dict)
#     return lg_list

# print(lg_player())

#두산 베어스 정보 따오기
#삼성
#kt

#한화 이글스 정보 따오기
def hanhwa_player():
    url = "https://www.koreabaseball.com/Player/Register.aspx"
    driver.get(url)
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    players = soup.select('.row > table > tbody > tr')

    hanhwa_list = []
    for player in players:
        tds = player.find_all("td")
        if len(tds) < 5:
            continue

        number = tds[0].get_text(strip=True)
        name = tds[1].get_text(strip=True)
        toota = tds[2].get_text(strip=True)
        birth = tds[3].get_text(strip=True)
        spec = tds[4].get_text(strip=True)

        player_dict = {
            "number": number,
            "name": name,
            "toota": toota,
            "birth": birth,
            "spec": spec
        }
        hanhwa_list.append(player_dict)
    return hanhwa_list

teams_col7.insert_one({"hanhwa_player":hanhwa_player()})

