# 빠른 시작 가이드 🚀

## 1분 만에 시작하기

### Step 1: 파일 다운로드
모든 파일을 하나의 폴더에 다운로드하세요:
- app.py
- requirements.txt
- .streamlit/ 폴더 (secrets.toml, config.toml 포함)

### Step 2: 의존성 설치
```bash
pip install -r requirements.txt
```

### Step 3: 앱 실행
```bash
streamlit run app.py
```

### Step 4: 브라우저에서 접속
자동으로 브라우저가 열립니다. 열리지 않으면:
- http://localhost:8501 접속

### Step 5: 로그인
- 기본 비밀번호: `team123`

## 주요 사용 팁

### 프로젝트 추가하기
1. 사이드바에서 "➕ 새 프로젝트/업무 추가" 클릭
2. 필수 항목(*) 입력
3. "✅ 프로젝트 추가" 버튼 클릭

### 데이터 필터링
1. "📋 프로젝트 테이블" 메뉴 선택
2. 상단 필터 사용:
   - 🔍 프로젝트명 검색
   - 👥 담당자 필터
   - 📊 상태 필터
   - 🗂️ 분류 필터

### Excel 다운로드
1. "📋 프로젝트 테이블" 메뉴
2. 하단 "📥 Excel 다운로드" 버튼 클릭
3. "📥 다운로드 시작" 클릭

### 팀원 추가
1. "👥 팀원 관리" 메뉴 선택
2. 이름과 이모지 입력
3. "➕ 추가" 버튼 클릭

## 비밀번호 변경 방법

`.streamlit/secrets.toml` 파일 수정:
```toml
app_password = "새로운비밀번호"
```

앱 재시작 후 적용됩니다.

## 문제 해결

### 앱이 실행되지 않아요
```bash
# Python 버전 확인 (3.8 이상 필요)
python --version

# 의존성 재설치
pip install --upgrade -r requirements.txt
```

### 데이터가 이상해요
```bash
# 데이터베이스 초기화
rm projects.db
streamlit run app.py
```

### 포트가 사용 중이에요
```bash
# 다른 포트에서 실행
streamlit run app.py --server.port 8502
```

## 다음 단계

1. ✅ 샘플 데이터 확인 및 테스트
2. 👥 실제 팀원 추가
3. 📋 첫 프로젝트 등록
4. 🗂️ Kanban 보드로 진행 상황 관리
5. 📊 대시보드에서 통계 확인

## 도움이 필요하세요?

- 상세 가이드: README.md 참조
- 문제 발생 시: GitHub Issues 등록

---

**즐거운 프로젝트 관리 되세요! 🎉**
