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

# #기아타이거즈 정보 따오기
# def kia_player():
#     uri="https://tigers.co.kr/players/entry-status"
#     driver.get(uri)
#     time.sleep(1)

#     soup=BeautifulSoup(driver.page_source,'html.parser')
#     rows=soup.select('tbody>tr')
#     kia_list=[]
#     for row in rows:
#         ths=row.find_all("th")
#         name=ths[1].get_text(strip=True)

#         tds=row.find_all("td")
#         if len(tds)<6:
#             continue
#         position=tds[0].get_text(strip=True)
#         number=tds[1].get_text(strip=True)
#         toota=tds[2].get_text(strip=True)
#         birth=tds[3].get_text(strip=True)
#         height=tds[4].get_text(strip=True)
#         weight=tds[5].get_text(strip=True)

#         player_dict={
#             "name":name,
#             "position":position,
#             "number":number,
#             "toota":toota,
#             "birth": birth,
#             "height": height,
#             "weight": weight
#         }
#         kia_list.append(player_dict)
#     return kia_list

# # teams_col1.insert_one({"kia_player":kia_player()})

# #롯데 자이언츠 정보 따오기

# #LG 트윈스 정보 따오기
# # def lg_player():
# #     uri="https://www.lgtwins.com/service/html.ncd?view=%2Fpc_twins%2Ftwins_player%2Ftwins_rosters&baRq=IN_DS&IN_DS.YEAR=&baRs=OUT_DS1%2COUT_DS2&actID=BR_RetrievePlayerRosters"
# #     options.add_argument("--disable-gpu")
# #     driver = webdriver.Chrome(options=options)
# #     driver.get(uri)
# #     time.sleep(1)

# #     soup=BeautifulSoup(driver.page_source,'html.parser')
# #     driver.quit()

# #     rows=soup.select('.tab_content>.board_dic')
# #     lg_list=[]
# #     for row in rows:
# #         image=soup.select_one('.header>.img_wrap img')
# #         image_url = image['src']if image and image.has_attr('src')else ""
# #         name=soup.select_one('.header .title h3')
# #         name_id=name.get_text(strip=True) if name else""
# #         ps=row.find_all("p")
# #         if len(ps)<5:
# #             continue
# #         toota=ps[1].get_text(strip=True)
# #         birth=ps[2].get_text(strip=True)
# #         heightWeight=ps[3].get_text(strip=True)

# #         player_dict={
# #             "name":name_id,
# #             "image":image_url,
# #             "toota":toota,
# #             "birth":birth,
# #             "heightWeight":heightWeight
# #         }
# #         lg_list.append(player_dict)
# #     return lg_list

# # print(lg_player())

# #두산 베어스 정보 따오기
# #삼성
# #kt

# #한화 이글스 정보 따오기
# def hanhwa_player():
#     url = "https://www.koreabaseball.com/Player/Register.aspx"
#     driver.get(url)
#     time.sleep(1)

#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     players = soup.select('.row > table > tbody > tr')

#     hanhwa_list = []
#     for player in players:
#         tds = player.find_all("td")
#         if len(tds) < 5:
#             continue

#         number = tds[0].get_text(strip=True)
#         name = tds[1].get_text(strip=True)
#         toota = tds[2].get_text(strip=True)
#         birth = tds[3].get_text(strip=True)
#         spec = tds[4].get_text(strip=True)

#         player_dict = {
#             "number": number,
#             "name": name,
#             "toota": toota,
#             "birth": birth,
#             "spec": spec
#         }
#         hanhwa_list.append(player_dict)
#     return hanhwa_list

# teams_col7.insert_one({"hanhwa_player":hanhwa_player()})

#############################################################################

# 페이지 열기
# url = "https://www.koreabaseball.com/Player/Register.aspx"
# driver.get(url)
# print("페이지 접속 완료")
# time.sleep(2)

# # 팀 ID와 팀 이름 리스트
# team_ids = ['HH', 'LG', 'LT', 'OB', 'WO', 'SS', 'SK', 'NC', 'KT', 'HT']
# team_names = ['한화', 'LG', '롯데', '두산', '키움', '삼성', 'SSG', 'NC', 'KT', 'KIA']

# # 팀별 반복
# for tid, tname in zip(team_ids, team_names):
#     print(f"\n===== {tname} =====")
#     try:
#         # 팀 버튼 클릭
#         team_btn = driver.find_element(By.XPATH, f'//li[@data-id="{tid}"]/a')
#         team_btn.click()
#         print(f"{tname} 클릭 완료")
#         time.sleep(2)

#         # HTML 파싱
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         rows = soup.select('[class^="tNData"] tbody tr')
#         print(f"{tname} 선수 수: {len(rows)}명")

#         # 선수 정보 출력
#         for row in rows:
#             cols = row.select('td')
#             if len(cols) >= 5:
#                 number = cols[0].text.strip()
#                 name = cols[1].text.strip()
#                 toota = cols[2].text.strip()
#                 birth = cols[3].text.strip()
#                 spec = cols[4].text.strip()
#                 print(f"{number} {name} {toota} {birth} {spec}")
#     except Exception as e:
#         print(f"{tname} 처리 중 오류 발생: {e}")


    # 선수별 영상 추출 작업 시작
def get_player_clips(player_name):
        query = f"kbo {player_name}"
        # url = f"https://search.naver.com/search.naver?query={query}&where=video"
        url = f"https://search.naver.com/search.naver?where=video&sort=date&view=big&query={query}&playtime=&period=&dtype=&ptype=&selected_cp=&sm=mtb_opt&ie=utf8&nso=so:dd,p:all&x_video="
        driver.get(url)
        time.sleep(2)  # 페이지 로딩 대기

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.select(".list_wrap")

        # print(items)

        video_list = []
        for item in items[:5]:
            title_tag = item.select_one('.info_area .info_title')
            
            link_tag = item.select_one('.thumb_area a')
            
            thumb_tag = item.select_one('.thumb_area img')
            
            meta_spans = item.select('.desc_group span.desc')
            # print(meta_spans)
            # print(title_tag,link_tag,thumb_tag,meta_spans)

            if not (title_tag and link_tag and thumb_tag and len(meta_spans) >= 2):
                continue

            link = link_tag['href']
            if "youtube.com" in link and "v=" in link:
                video_id = link.split("v=")[-1].split("&")[0]
                embed_link = f"https://www.youtube.com/embed/{video_id}"
                watch_link = link
            else:
                continue

            video = {
                "title": title_tag.get_text(strip=True),
                "embed_link": embed_link,
                "watch_link": watch_link,
                "thumbnail": thumb_tag['src'],
                "date": meta_spans[0].get_text(strip=True),
                "views": meta_spans[1].get_text(strip=True)
            }
            video_list.append(video)

        return video_list

videos = get_player_clips("김도영")
print(videos)
for i, v in enumerate(videos, start=1):
    print(f"[{i}] 제목: {v['title']}")
    print(f"    🎬 Watch: {v['watch_link']}")
    print(f"    📺 Embed: {v['embed_link']}")
    print(f"    🖼️ 썸네일: {v['thumbnail']}")
    print(f"    📅 날짜: {v['date']}")
    print(f"    👁️ 조회수: {v['views']}")
    print("-" * 80)

# 브라우저 종료
driver.quit()