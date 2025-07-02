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
from datetime import datetime

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

#두산 아이디 mongoDB 삽입
def dosan_id_list():
    dosan_id=['99543', '98144', '64803', '61204', '60181', '71835', '76869', '68289', '92501', '67266', '65639', '61643', '51264', '52204', '72523', '55239', '52206', '68220', '68249', '66291', '55257', '54263', '55268', '54219', '76232', '50208', '67207', '64468', '63123', '52267', '55252', '53554', '55208', '79231', '78224', '63257', '66209']
    dosan_player=list(teams_col4.find().sort("_id",1)) #순서대로 저장되게 설정 
    
    if len(dosan_player)!=len(dosan_id):
        print("DB 선수 수:", db.dosan_player.count_documents({}))
        print("playerId 수:", len(dosan_id))

        print("선수 수와 아이디 수가 다름")
        return 
    
    for player,pid in zip (dosan_player,dosan_id):
        teams_col4.update_one(
            {"_id": player["_id"]},
            {"$set":{"playerId": pid}}
        )

#두산 선수 이미지 따기
def dosan_image_list():
    players=list(teams_col4.find({"playerId":{"$exists":True}}))

    for player in players:
        pid=player.get("playerId")
        
        uri=f"https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId={pid}"
        driver.get(uri)
        time.sleep(0.5)

        soup=BeautifulSoup(driver.page_source,'html.parser')
        img_1=soup.select_one('.player_info .photo img')
        img_uri=img_1['src']if img_1 and img_1.has_attr('src')else""
        teams_col4.update_one(
            {"_id":player["_id"]},
            {"$set":{"img":img_uri}}
        )
#####################################333

#기아 아이디 mongoDB 삽입
def kia_id_list():
    kia_id=['70756', '75321', '73241', '99153', '70410', '70626', '62668', '65682', '77452', '63394', '72303', '63342', '53613', '50641', '52639', '76225', '54645', '66609', '77637', '69745', '50662', '55663', '54610', '53615', '60337', '78112', '68646', '64646', '50657', '50600', '66614', '55645', '69636', '64560', '66606', '65653', '72443', '67610', '61353']
    kia_player=list(teams_col1.find().sort("_id",1)) #순서대로 저장되게 설정 
    
    if len(kia_player)!=len(kia_id):
        print("DB 선수 수:", db.kia_player.count_documents({}))
        print("playerId 수:", len(kia_id))

        print("선수 수와 아이디 수가 다름")
        return 
    
    for player,pid in zip (kia_player,kia_id):
        teams_col1.update_one(
            {"_id": player["_id"]},
            {"$set":{"playerId": pid}}
        )
#기아 선수 이미지 따기
def kia_image_list():
    players=list(teams_col1.find({"playerId":{"$exists":True}}))

    for player in players:
        pid=player.get("playerId")
        
        uri=f"https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId={pid}"
        driver.get(uri)
        time.sleep(0.5)

        soup=BeautifulSoup(driver.page_source,'html.parser')
        img_1=soup.select_one('.player_info .photo img')
        img_uri=img_1['src']if img_1 and img_1.has_attr('src')else""
        teams_col1.update_one(
            {"_id":player["_id"]},
            {"$set":{"img":img_uri}}
        )

############################################
#키움 아이디 mongoDB 삽입
def kiwoom_id_list():
    kiwoom_id=['96723', '74163', '50372', '70312', '50365', '63920', '78148', '99137', '72154', '62353', '69328', '55313', '69360', '55301', '52330', '67116', '53301', '76118', '55348', '66018', '64350', '69045', '55394', '52395', '53312', '53344', '65357', '76267', '51302', '55392', '55397', '53309', '50167', '52305', '69332', '55326', '64340', '50357']
    kiwoom_player=list(teams_col8.find().sort("_id",1)) #순서대로 저장되게 설정 
    
    if len(kiwoom_player)!=len(kiwoom_id):
        print("DB 선수 수:", db.kiwoom_player.count_documents({}))
        print("playerId 수:", len(kiwoom_id))

        print("선수 수와 아이디 수가 다름")
        return 
    
    for player,pid in zip (kiwoom_player,kiwoom_id):
        teams_col8.update_one(
            {"_id": player["_id"]},
            {"$set":{"playerId": pid}}
        )

#키움 선수 이미지 따기
def kiwoom_image_list():
    players=list(teams_col8.find({"playerId":{"$exists":True}}))

    for player in players:
        pid=player.get("playerId")
        
        uri=f"https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId={pid}"
        driver.get(uri)
        time.sleep(0.5)

        soup=BeautifulSoup(driver.page_source,'html.parser')
        img_1=soup.select_one('.player_info .photo img')
        img_uri=img_1['src']if img_1 and img_1.has_attr('src')else""
        teams_col8.update_one(
            {"_id":player["_id"]},
            {"$set":{"img":img_uri}}
        )

####################################################
#kt 아이디 mongoDB 삽입
def kt_id_list():
    kt_id=['89620', '73113', '77733', '94843', '70553', '92401', '74339', '72801', '97351', '73228', '64001', '73117', '69113', '65516', '65048', '50030', '69032', '65060', '55043', '50859', '52060', '54063', '54354', '78548', '50066', '69056', '64504', '79402', '79240', '64007', '68504', '51003', '67025', '52001', '64166', '67644', '66706', '64004']
    kt_player=list(teams_col6.find().sort("_id",1)) #순서대로 저장되게 설정 
    
    if len(kt_player)!=len(kt_id):
        print("DB 선수 수:", db.kt_player.count_documents({}))
        print("playerId 수:", len(kt_id))

        print("선수 수와 아이디 수가 다름")
        return 
    
    for player,pid in zip (kt_player,kt_id):
        teams_col6.update_one(
            {"_id": player["_id"]},
            {"$set":{"playerId": pid}}
        )
#kt 선수 이미지 따기
def kt_image_list():
    players=list(teams_col6.find({"playerId":{"$exists":True}}))

    for player in players:
        pid=player.get("playerId")
        
        uri=f"https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId={pid}"
        driver.get(uri)
        time.sleep(0.5)

        soup=BeautifulSoup(driver.page_source,'html.parser')
        img_1=soup.select_one('.player_info .photo img')
        img_uri=img_1['src']if img_1 and img_1.has_attr('src')else""
        teams_col6.update_one(
            {"_id":player["_id"]},
            {"$set":{"img":img_uri}}
        )
#########################################################33
#lg 아이디 mongoDB 삽입
def lg_id_list():
    lg_id=['91350', '97300', '96761', '92809', '92905', '97350', '74139', '61114', '78813', '99152', '61101', '63248', '51111', '55121', '67143', '54119', '69134', '69108', '53139', '75867', '55146', '63950', '50106', '55167', '52154', '79365', '69102', '65207', '66162', '69100', '79109', '53123', '50054', '52103', '68119', '68110', '62415', '76290']
    lg_player=list(teams_col3.find().sort("_id",1)) #순서대로 저장되게 설정 
    
    if len(lg_player)!=len(lg_id):
        print("DB 선수 수:", db.lg_player.count_documents({}))
        print("playerId 수:", len(lg_id))

        print("선수 수와 아이디 수가 다름")
        return 
    
    for player,pid in zip (lg_player,lg_id):
        teams_col3.update_one(
            {"_id": player["_id"]},
            {"$set":{"playerId": pid}}
        )
#lg 선수 이미지 따기
def lg_image_list():
    players=list(teams_col3.find({"playerId":{"$exists":True}}))

    for player in players:
        pid=player.get("playerId")
        
        uri=f"https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId={pid}"
        driver.get(uri)
        time.sleep(0.5)

        soup=BeautifulSoup(driver.page_source,'html.parser')
        img_1=soup.select_one('.player_info .photo img')
        img_uri=img_1['src']if img_1 and img_1.has_attr('src')else""
        teams_col3.update_one(
            {"_id":player["_id"]},
            {"$set":{"img":img_uri}}
        )
##################################################################3
#롯데 아이디 mongoDB 삽입
def lotte_id_list():
    lotte_id=['90214', '76368', '75539', '93242', '94836', '78643', '94528', '74823', '72546', '72214', '64266', '65522', '64021', '76430', '55532', '62528', '55536', '52530', '50596', '67539', '50556', '54537', '51594', '68242', '61102', '68518', '52568', '60523', '68205', '77564', '51551', '62802', '55530', '55511', '68507', '78513', '54529', '55506', '52504']
    lotte_player=list(teams_col2.find().sort("_id",1)) #순서대로 저장되게 설정 
    
    if len(lotte_player)!=len(lotte_id):
        print("DB 선수 수:", db.lotte_player.count_documents({}))
        print("playerId 수:", len(lotte_id))

        print("선수 수와 아이디 수가 다름")
        return 
    
    for player,pid in zip (lotte_player,lotte_id):
        teams_col2.update_one(
            {"_id": player["_id"]},
            {"$set":{"playerId": pid}}
        )

#lotte 선수 이미지 따기
def lotte_image_list():
    players=list(teams_col2.find({"playerId":{"$exists":True}}))

    for player in players:
        pid=player.get("playerId")
        
        uri=f"https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId={pid}"
        driver.get(uri)
        time.sleep(0.5)

        soup=BeautifulSoup(driver.page_source,'html.parser')
        img_1=soup.select_one('.player_info .photo img')
        img_uri=img_1['src']if img_1 and img_1.has_attr('src')else""
        teams_col2.update_one(
            {"_id":player["_id"]},
            {"$set":{"img":img_uri}}
        )
#####################################################
#nc 아이디 mongoDB 삽입
def nc_id_list():
    nc_id= ['94629', '78640', '77454', '74456', '78361', '75441', '73306', '77104', '79364', '63914', '70434', '55903', '55912', '63959', '68900', '68902', '53973', '52995', '66920', '65949', '67954', '69969', '64995', '55995', '64022', '68912', '62907', '69995', '51996', '51907', '69992', '54944', '68904', '51344', '50902', '77532', '64101', '63963', '79215']
    nc_player=list(teams_col9.find().sort("_id",1)) #순서대로 저장되게 설정 
    
    if len(nc_player)!=len(nc_id):
        print("DB 선수 수:", db.nc_player.count_documents({}))
        print("playerId 수:", len(nc_id))

        print("선수 수와 아이디 수가 다름")
        return 
    
    for player,pid in zip (nc_player,nc_id):
        teams_col9.update_one(
            {"_id": player["_id"]},
            {"$set":{"playerId": pid}}
        )
#nc 선수 이미지 따기
def nc_image_list():
    players=list(teams_col9.find({"playerId":{"$exists":True}}))

    for player in players:
        pid=player.get("playerId")
        
        uri=f"https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId={pid}"
        driver.get(uri)
        time.sleep(0.5)

        soup=BeautifulSoup(driver.page_source,'html.parser')
        img_1=soup.select_one('.player_info .photo img')
        img_uri=img_1['src']if img_1 and img_1.has_attr('src')else""
        teams_col9.update_one(
            {"_id":player["_id"]},
            {"$set":{"img":img_uri}}
        )

##########################################
#삼성 아이디 mongo 삽입 
def samsung_id_list():
    samsung_id= ['96307', '71432', '72456', '84240', '99810', '76858', '95459', '73339', '73409', '72742', '55499', '53455', '65320', '54404', '60146', '75421', '62360', '50464', '68415', '54401', '55455', '51454', '55460', '53375', '65132', '74540', '54400', '52415', '62234', '52430', '65586', '54408', '62505', '66409', '65040', '67449', '50458', '69418']
    samsung_player=list(teams_col5.find().sort("_id",1)) #순서대로 저장되게 설정 
    
    if len(samsung_player)!=len(samsung_id):
        print("DB 선수 수:", db.samsung_player.count_documents({}))
        print("playerId 수:", len(samsung_id))

        print("선수 수와 아이디 수가 다름")
        return 
    
    for player,pid in zip (samsung_player,samsung_id):
        teams_col5.update_one(
            {"_id": player["_id"]},
            {"$set":{"playerId": pid}}
        )

#삼성 선수 이미지 따기
def samsung_image_list():
    players=list(teams_col5.find({"playerId":{"$exists":True}}))

    for player in players:
        pid=player.get("playerId")
        
        uri=f"https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId={pid}"
        driver.get(uri)
        time.sleep(0.5)

        soup=BeautifulSoup(driver.page_source,'html.parser')
        img_1=soup.select_one('.player_info .photo img')
        img_uri=img_1['src']if img_1 and img_1.has_attr('src')else""
        teams_col5.update_one(
            {"_id":player["_id"]},
            {"$set":{"img":img_uri}}
        )

#######################################################
#ssg 아이디 mongo 삽입 
def ssg_id_list():
    ssg_id= ['94310', '73213', '72325', '61743', '70121', '60882', '71848', '98808', '99314', '70820', '51897', '77829', '68856', '54833', '73211', '51867', '54803', '68043', '62869', '65343', '55855', '50812', '52809', '53892', '51865', '79456', '54805', '67893', '54812', '66917', '68868', '66864', '75847', '51868', '53827', '62895', '60558', '50854']
    ssg_player=list(teams_col10.find().sort("_id",1)) #순서대로 저장되게 설정 
    
    if len(ssg_player)!=len(ssg_id):
        print("DB 선수 수:", db.ssg_player.count_documents({}))
        print("playerId 수:", len(ssg_id))

        print("선수 수와 아이디 수가 다름")
        return 
    
    for player,pid in zip (ssg_player,ssg_id):
        teams_col10.update_one(
            {"_id": player["_id"]},
            {"$set":{"playerId": pid}}
        )

#삼성 선수 이미지 따기
def ssg_image_list():
    players=list(teams_col10.find({"playerId":{"$exists":True}}))

    for player in players:
        pid=player.get("playerId")
        
        uri=f"https://www.koreabaseball.com/Record/Retire/Hitter.aspx?playerId={pid}"
        driver.get(uri)
        time.sleep(0.5)

        soup=BeautifulSoup(driver.page_source,'html.parser')
        img_1=soup.select_one('.player_info .photo img')
        img_uri=img_1['src']if img_1 and img_1.has_attr('src')else""
        teams_col10.update_one(
            {"_id":player["_id"]},
            {"$set":{"img":img_uri}}
        )
# hanhwa_id_list()
# player_list()
# hanhwa_image_list()
# dosan_id_list()
# dosan_image_list()
# kia_id_list()
# kia_image_list()
# kiwoom_id_list()
# kiwoom_image_list()
# kt_id_list()
# kt_image_list()
# lg_id_list()
# lg_image_list()
# lotte_id_list()
# lotte_image_list()
# nc_id_list()
# nc_image_list()
# samsung_id_list()
# samsung_image_list()
# ssg_id_list()
# ssg_image_list()

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

# videos = get_player_clips("김도영")
# print(videos)
# for i, v in enumerate(videos, start=1):
#     print(f"[{i}] 제목: {v['title']}")
#     print(f"Watch: {v['watch_link']}")
#     print(f"Embed: {v['embed_link']}")
#     print(f"썸네일: {v['thumbnail']}")
#     print(f"날짜: {v['date']}")
#     print(f"조회수: {v['views']}")
#     print("-" * 80)

# 선수별 영상 MongoDB에 저장 
def player_clip_list(team_name_input): # ** player_clip_list 함수의 매개변수는 반드시 team_name의 문자열과 동일해야함**


    ########## 
    # 전역변수 collections, team_name 사용 
    #
    # collections=[
    # db.kia_player, db.lotte_player, db.lg_player, db.dosan_player, db.samsung_player,
    # db.kt_player, db.hanhwa_player, db.kiwoom_player, db.nc_player, db.ssg_player]
    #
    # team_name=['KIA','롯데','LG','두산','삼성','KT','한화','키움','NC','SSG']
    ###########

    #팀의 컬렉션 위치 찾기
    idx = team_name.index(team_name_input)
    
    # DB에서 해당 선수의 팀 컬렉션 찾기
    team_collection = collections[idx]
    
    # 해당 팀의 전체 선수 이름 추출 
    team_player_name =team_collection.find({}, {"name": 1})


    # 전체 선수중 타겟 선수 찾기
    for player in team_player_name:
        target_player_name = player.get("name")
        if not target_player_name:
            continue

        #영상 스크래핑 함수 호출
        clips = get_player_clips(target_player_name)

        team_collection.update_one(
            {"name": target_player_name},
            {"$set": {"player_clips": clips,
                       "team_name": team_name_input
                      }}
        )
    print(team_name_input,"저장완료")

# player_clip_list('KIA') 
# player_clip_list('롯데')
# player_clip_list('LG')
# player_clip_list('삼성')
# player_clip_list('두산')
# player_clip_list('KT')
# player_clip_list('한화')
# player_clip_list('키움')
# player_clip_list('NC')
# player_clip_list('SSG')

#DB에서 팀별 댓글 추출 API 응답하는 부분
@team_page.route('/team/<teamname>/<pid>/comment', methods=['GET'])
def get_team_comments(pId):

    # DB
    # 댓글 DB중 해당하는 팀의 댓글 추출 후 리스트화
    comments = list(db.team_comment.find({'team_id': team_id}, {'_id': False}))
    return jsonify({'result': 'success', 'comments': comments})


# 댓글 등록 api 응답하는 부분
@team_page.route('/team/<teamname>/<pid>/comment', methods =['POST'])
def post_comment(pId):
        
     # 입력받은 Comment 데이터 가져오기
    input_comment = request.form.get('comment','').strip()

    if(input_comment == ''):
        return jsonify({'result': 'fail', 'msg': '내용을 입력하세요.'})


    #세션된 ID,닉네임 가져오기
    target_user = session.get('id')
    target_nickname = session.get('nickname')

    ######### 
    # 전역변수 collections, team_name 사용 
    #
    # collections=[
    # db.kia_player, db.lotte_player, db.lg_player, db.dosan_player, db.samsung_player,
    # db.kt_player, db.hanhwa_player, db.kiwoom_player, db.nc_player, db.ssg_player]
    #
    # team_name=['KIA','롯데','LG','두산','삼성','KT','한화','키움','NC','SSG']
    ###########

    #팀의 컬렉션 위치 찾기
    idx = team_name.index(pId)
    # DB에서 해당 선수의 팀 컬렉션 찾기
    team_collection = collections[idx]
    
    # 해당 팀의 전체 선수 이름 추출 
    team_player_name =team_collection.find({}, {"name": 1})

     # 전체 선수중 타겟 선수 찾기
    for player in team_player_name:
        target_player_name = player.get("name")
        if not target_player_name:
            continue
    
    # DB의 각 팀별 컬렉션에서 해당 선수의 도큐멘트 형태로 변환
        team_collection.update_one(
            {"name": target_player_name},
             {"$set": {
                 
                'id' : target_user,
                'nickname' : target_nickname,
                'player_comment': input_comment,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                }
             }
            )
    # DB에 아이디, 닉네임과 댓글 내용 데이터 저장
    # 댓글 등록 성공 (응답 성공 반환)
    return jsonify( {'result': 'success','msg' : '댓글 등록 성공!', 'nickname' : target_nickname, 'url' : '/team/<teamname>/<pId>'})




# # 팀별 반복
#     for idx, (tid,tname) in enumerate(zip(team_id, team_name)):
#         try:
#             # 팀 버튼 클릭
#             team_btn = driver.find_element(By.XPATH, f'//li[@data-id="{tid}"]/a')
#             team_btn.click()
#             time.sleep(2)

#             # HTML 파싱
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             rows = soup.select('[class^="tNData"] tbody tr')

#             players=[]

#             # 선수 정보 뽑아옴 
#             now = time.time()
#             for row in rows:
#                 cols = row.select('td')
#                 if len(cols) >= 3:
#                     player_dict={
#                         "name": cols[1].text.strip(),     # 이름
#                         "number": cols[0].text.strip(),   # 번호
#                         "toota": cols[2].text.strip(),    # 투타
#                         "birth": cols[3].text.strip(),    # 생년월일
#                         "spec": cols[4].text.strip(),
#                         "lastUpdatedTime": now
#                     }
#                     players.append(player_dict)

#             # collections[idx].delete_many({})
#             # collections[idx].insert_many(players)

#         except Exception as e:
#             print(f"{tname} 처리 중 오류 발생: {e}")
#     driver.quit()





# 브라우저 종료
driver.quit()