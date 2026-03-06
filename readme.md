# ⚾ BaseBullBBaDDa — KBO Fan Platform
KBO 팀 · 선수 · 뉴스 · 순위를 한곳에서 확인할 수 있는 야구 팬 맞춤형 웹 플랫폼

크래프톤 정글 웹 개발 캠프 Sprint 2 Project | 팀 베이스불빠따

---

## 📌 목차
- [기획 배경](#-기획-배경)
- [프로젝트 목표](#-프로젝트-목표)
- [핵심 기능](#-핵심-기능)
- [서비스 개요](#️-서비스-개요)
- [시스템 구조](#️-시스템-구조)
- [주요 페이지](#-주요-페이지)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [실행 방법](#-실행-방법)
- [API 요약](#-api-요약)
- [기대 효과](#-기대-효과)
- [향후 확장 방향](#-향후-확장-방향)
- [팀원](#-팀원)

---

## 🚨 기획 배경
“야구 팬이 원하는 정보는 흩어져 있고, 한 번에 보기 어렵다.”

KBO 팬들은 보통  
- 팀 순위는 공식 홈페이지에서  
- 선수 정보는 별도 검색으로  
- 관련 뉴스는 포털이나 기사 페이지에서  
- 관심 콘텐츠 저장은 개인적으로 따로 관리해야 합니다  

이처럼 정보가 여러 채널에 분산되어 있어  
**팀 정보, 선수 정보, 뉴스, 순위, 개인 관심 콘텐츠를 한곳에서 확인할 수 있는 통합형 서비스**가 필요하다고 판단했습니다.

👉 **베이스불빠따는 KBO 팬을 위한 종합 정보 플랫폼**을 목표로 기획되었습니다.

---

## 🎯 프로젝트 목표
| 목표 | 설명 |
|------|------|
| 📊 실시간 리그 정보 제공 | KBO 팀 순위를 크롤링하여 최신 순위 제공 |
| 🧢 팀 중심 정보 탐색 | 구단별 상세 정보, 뉴스, 경기 일정 확인 |
| 🧍 선수 중심 정보 탐색 | 팀별 선수 목록 및 선수 상세 정보 제공 |
| 📰 뉴스 통합 제공 | 팀/선수 관련 뉴스를 한 페이지에서 확인 |
| 👤 사용자 맞춤 기능 | 로그인, 마이페이지, 좋아요 기사 저장 기능 제공 |

---

## ✨ 핵심 기능

### 1️⃣ KBO 팀 순위 조회
- KBO 공식 홈페이지의 팀 순위를 크롤링
- DB에 저장 후 일정 주기로 갱신
- 메인 페이지에서 순위 테이블 형태로 제공

### 2️⃣ 팀 상세 페이지
- 구단별 상세 정보 제공
  - 팀명
  - 연고지
  - 감독
  - 우승 횟수
  - 팀 컬러
  - 공식 홈페이지 링크
- 팀 관련 뉴스 기사 표시
- 경기 일정 확인 가능

### 3️⃣ 선수 목록 / 선수 상세 페이지
- 팀별 선수 목록 제공
- 선수 카드 클릭 시 상세 페이지 이동
- 선수별 기본 정보와 관련 뉴스 확인 가능

### 4️⃣ 사용자 계정 기능
- 회원가입 / 로그인 / 로그아웃
- 세션 기반 로그인 상태 유지
- 닉네임 변경
- 회원 탈퇴
- 좋아하는 팀 설정

### 5️⃣ 마이페이지
- 사용자 정보 확인
- 좋아요한 기사 목록 저장 및 조회
- 개인화된 관심 콘텐츠 관리 가능

### 6️⃣ 기사 즐겨찾기
- 사용자가 원하는 기사 URL 저장
- 마이페이지에서 다시 확인 가능

---

## 🖥️ 서비스 개요

```text
사용자
  │
  ├── 메인 페이지 접속
  │       └── KBO 팀 순위 확인
  │
  ├── 팀 선택
  │       └── 팀 정보 / 뉴스 / 경기 일정 확인
  │
  ├── 선수 페이지 이동
  │       └── 팀별 선수 목록 및 선수 상세 정보 확인
  │
  └── 로그인
          ├── 좋아하는 팀 설정
          ├── 기사 즐겨찾기 저장
          └── 마이페이지에서 개인화 정보 확인
```

---

## 🏗️ 시스템 구조

```text
[Frontend]
HTML / CSS / JavaScript / jQuery / Bootstrap
        │
        ▼
[Backend]
Flask Blueprint 기반 웹 서버
        │
        ├── 사용자 기능 처리
        ├── 팀 / 선수 페이지 라우팅
        ├── 세션 관리
        └── 크롤링 데이터 API 제공
        │
        ▼
[Database]
MongoDB
        │
        ├── user
        ├── ranking
        ├── teams
        └── player collections
        │
        ▼
[External Source]
KBO 공식 홈페이지 / 네이버 검색 / 뉴스 페이지
```

---

## 📄 주요 페이지

### `/`
- 메인 페이지
- 사이트 소개
- KBO 리그 순위 테이블 출력

### `/team/<team_id>`
- 팀 상세 페이지
- 팀 소개
- 관련 뉴스
- 경기 일정

### `/playerlist`
- 선수 리스트 페이지
- 팀별 선수 목록 출력

### `/team/<team_id>/playerId=<player_id>`
- 선수 상세 페이지
- 선수 상세 정보
- 관련 뉴스 확인

### `/user/login`
- 로그인 페이지

### `/user/signup`
- 회원가입 페이지

### `/user/<id>`
- 마이페이지
- 사용자 정보
- 저장한 기사 목록
- 닉네임 수정 / 탈퇴

---

## 🛠 기술 스택

| 분류 | 기술 |
|------|------|
| Backend | Flask, Jinja2 |
| Frontend | HTML, CSS, JavaScript, jQuery, Bootstrap |
| Database | MongoDB |
| Crawling | requests, BeautifulSoup, Selenium |
| Runtime | Python |
| Session | Flask Session |

---

## 📂 프로젝트 구조

```bash
basebullbbadda-main/
├── app.py
├── requirements.txt
├── readme.md
├── static/
│   ├── css/
│   │   └── index.css
│   ├── img/
│   │   ├── backgroundpage.png
│   │   ├── logo.png
│   │   └── logoImg.png
│   └── js/
│       └── index.js
├── templates/
│   ├── header.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── myPage.html
│   ├── player.html
│   ├── playerlist.html
│   └── teampage.html
└── views/
    ├── __init__.py
    ├── user.py
    ├── player.py
    └── teampage.py
```

---

## 🚀 실행 방법

### 1. 저장소 클론
```bash
git clone <repository_url>
cd basebullbbadda-main
```

### 2. 가상환경 생성 및 실행

#### Windows Git Bash 환경
```bash
python -m venv .venv
source .venv/Scripts/activate
```

#### Mac / Linux 환경
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 서버 실행
```bash
python app.py
```

기본 실행 주소
```bash
http://127.0.0.1:5000
```

---

## 🔌 API 요약

### 세션 확인
```http
GET /api/session
```

### 팀 순위 조회
```http
GET /api/ranking
```

### 사용자 프로필 이미지 조회
```http
GET /api/getUserImg
```

### 팀별 선수 목록 조회
```http
GET /players/api/<teamName>
```

### 회원가입
```http
POST /user/api/signup
```

### 로그인
```http
POST /user/api/login
```

### 로그아웃
```http
GET /user/api/logout
POST /user/api/logout
```

### 닉네임 변경
```http
POST /user/api/updateNick
```

### 좋아하는 팀 설정
```http
POST /user/api/idol
```

### 기사 즐겨찾기 저장
```http
POST /user/api/likes
```

### 즐겨찾기 목록 조회
```http
GET /user/api/getLikes
```

### 회원 탈퇴
```http
POST /user/api/delete
```

---

## 📈 기대 효과
- KBO 팬이 필요한 정보를 하나의 플랫폼에서 탐색 가능
- 팀 중심 / 선수 중심으로 모두 접근 가능
- 뉴스와 일정까지 함께 제공해 탐색 효율 향상
- 사용자 계정 기반 기능으로 개인화 경험 제공
- 향후 커뮤니티, 응원 기능, 경기 예측 기능 등으로 확장 가능

---

## 🚀 향후 확장 방향
- 예외 처리 및 데이터 검증 로직 고도화
- 주기적 데이터 수집 자동화
- 검색 기능 고도화
- 커뮤니티 기능 확장(답글, 게시글, 좋아요 등)
- 배포 환경 구성 및 운영 자동화

---

## ⚠️ 실행 전 참고
현재 프로젝트 코드에는 DB 접속 정보가 직접 작성되어 있으므로,  
공개 저장소로 운영할 경우 반드시 환경변수 방식으로 수정하는 것을 권장합니다.

예시:
```bash
MONGO_URI=your_mongodb_uri
SECRET_KEY=your_secret_key
```

코드 예시:
```python
import os

uri = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY")
```

---

## 👥 팀원
| 이름 | 역할 |
|------|------|
| 권소윤 | Frontend / Backend / 데이터 연동 / 크롤링 |
| 김진호 | Frontend / Backend / 서버 최적화 |
| 손명완 | Frontend / Backend |

---

## 🏁 한 줄 소개
**“지금 가장 핫한 KBO 정보를 한자리에!”**  
베이스불빠따는 팀, 선수, 뉴스, 순위를 모아 보여주는 **KBO 팬 맞춤형 통합 웹 플랫폼**입니다.
