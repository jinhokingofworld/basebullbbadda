# DB 접속 키 `.env` 분리 계획

## Summary
- 목표는 `app.py`와 `views` 내부 Python 파일들에 하드코딩된 MongoDB URI를 제거하고, 로컬 개발용 `.env` 기반 설정으로 전환하는 것이다.
- 범위는 `views`만이 아니라 실제 노출 경로 전체인 `app.py`까지 포함한다. 현재 같은 URI가 여러 곳에 중복되어 있고, `views/player.py`도 import 체인에 포함되므로 함께 정리한다.
- 구현 방식은 각 파일 개별 치환이 아니라 공용 설정/DB 모듈을 신설해 `MONGO_URI` 로딩, 검증, `MongoClient`, `db` 객체 생성을 한 곳으로 모으는 방향으로 고정한다.

## Implementation Changes
- 루트에 공용 설정/DB 모듈을 추가한다.
  - 책임: `.env` 로드, `MONGO_URI` 읽기, 누락 시 명확한 예외 발생, `MongoClient` 1회 생성, `db = client.Splint2_Database` 제공.
  - `python app.py` 실행 방식을 유지하므로 `python-dotenv`를 도입하고 이 모듈에서 `load_dotenv()`를 호출한다.
- `app.py`, `views/user.py`, `views/teampage.py`, `views/player.py`의 하드코딩된 URI와 `MongoClient(...)` 초기화를 제거하고 공용 모듈의 `db` 또는 `client`를 import하도록 바꾼다.
- `views/__init__.py`의 `app.secret_key`는 `SECRET_KEY`를 선택적으로 읽고 없으면 기존처럼 랜덤 생성 fallback을 쓰도록 정리한다.
- 루트에 `.env.example`을 추가한다.
  - 기본 키: `MONGO_URI`
  - 선택 키: `SECRET_KEY`
- `requirements.txt`에 `python-dotenv`를 추가한다.
- `readme.md`의 실행 방법을 실제 코드 구조와 맞춘다.
  - `.env.example` 복사 단계 추가
  - `MONGO_URI` 필수 설명 추가
  - 필요 시 `SECRET_KEY` 선택 설명 추가
- 보안 후속 조치를 별도 단계로 남긴다.
  - 현재 URI가 Git 이력에 존재하므로 MongoDB 비밀번호 또는 사용자를 회전한다.
  - 공개 전에는 새 URI 발급 후 코드 반영이 우선이다.

## Test Plan
- `git log -1 --oneline`으로 체크포인트 커밋이 생성됐는지 확인한다.
- `plan.md` 생성 직후 파일 존재와 문서 섹션 구성을 확인한다.
- `rg "mongodb\\+srv|MongoClient\\(" app.py views` 결과에 하드코딩 URI가 남지 않는지 확인한다.
- `.env`가 없는 상태에서 실행하면 `MONGO_URI` 누락 오류로 즉시 종료되는지 확인한다.
- 유효한 `.env`로 `python app.py` 실행 시 서버가 import 단계까지 정상 통과하는지 확인한다.

## Assumptions
- `plan.md` 위치는 저장소 루트로 고정한다.
- 실행 시작 시 워킹트리가 clean이면 빈 커밋을 만든다.
- DB 이름 `Splint2_Database`는 유지한다.
- 기존 코드의 다른 오류는 이번 작업 범위 밖이지만, `.env` 분리 검증 과정에서 드러나면 구분해서 기록한다.
