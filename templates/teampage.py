import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

uri="mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true"
client=MongoClient("mongodb+srv://gksqkf0824:iIb12ywrv7wlB0BP@kwonsoyun.xkcilez.mongodb.net/?retryWrites=true&w=majority&appName=KWONSOYUN&tlsAllowInvalidCertificates=true")
db=client.Splint2_Database
teams_col=db.teams

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

#동적 반복
for team_name in team_homepage.keys():
   
    query=f"{team_name}"
    uri=f"https://search.naver.com/search.naver?query={query}"
    headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    res=requests.get(uri,headers=headers)
    soup=BeautifulSoup(res.text,'html.parser')

    doc={
        "team_name":team_name,
        "homepage":team_homepage[team_name],
        "region":team_location[team_name]
    }

#팀 이미지 가져오기
    team_image=soup.select_one('.api_cs_wrap .thmb img')
    if team_image and team_image.has_attr('src'):
        doc["image"]=team_image['src']
    else:
        doc["image"]=""

#팀당 감독 들고오기
    team_manage=soup.select_one('.detail .class_etcinfo_sportsgame_managerTitle + dd a')
    if team_manage:
        doc["manager"]=team_manage.get_text(strip=True)
    else:
        doc["manager"]=""
  
# #팀 경기일정 
#     team_code=team_name.split()[0]
#     schedule_url=f"https://www.koreabaseball.com/Schedule/Schedule.aspx"
#     res_schedule=requests.get(schedule_url, headers=headers)
#     soup_schedule=BeautifulSoup(res_schedule.text,'html.parser')
#     schedule_rows=soup_schedule.select('.tbl tbody tr')
#     schedule_list=[]

#     for row in schedule_rows:
#         cols=row.select('td')
#         if len(cols)>=3:
#             date=cols[0].text.strip()
#             time_=cols[1].text.strip()
#             match=cols[2].text.strip()
#             schedule_list.append({
#                 "date":date,
#                 "time":time_,
#                 "match":match
#             })
            
#     print(schedule_list)

# doc["schedule"]=schedule_list


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

doc={
    "team_win":team_win,
    "team_color":team_color
}
