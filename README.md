# 팀 프로젝트 관리 시스템 📊

프로페셔널한 내부 팀 프로젝트 및 업무 관리 Streamlit 애플리케이션

## 🌟 주요 기능

### 1. 📊 대시보드
- 실시간 프로젝트 통계 (전체/진행 중/완료/평균 진척률)
- 담당자별 워크로드 차트
- 상태별 프로젝트 분포 파이 차트
- 지연 프로젝트 및 마감 임박 프로젝트 경고

### 2. 📋 프로젝트 테이블
- 전문적인 데이터 테이블 (진행률 바, 색상 코딩된 상태)
- 고급 필터링 (프로젝트명 검색, 담당자, 상태, 분류)
- Excel 다운로드 기능
- 승인 체크박스

### 3. 🗂️ Kanban 보드
- 4개 컬럼: 할 일 / 진행 중 / 일정 지연 / 완료
- 시각적 카드 레이아웃
- 진행률 표시 및 마감일 알림

### 4. ➕ 프로젝트 추가
- 직관적인 폼 기반 입력
- 멀티 담당자 선택
- 진행률 슬라이더

### 5. 👥 팀원 관리
- 팀원 추가/삭제
- 이모지 커스터마이징

## 🚀 로컬 실행 방법

### 필수 요구사항
- Python 3.8 이상
- pip

### 설치 및 실행

```bash
# 1. 저장소 클론 또는 파일 다운로드
git clone <repository-url>
cd team-project-management

# 2. 가상환경 생성 (선택사항이지만 권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 앱 실행
streamlit run app.py
```

### 초기 로그인
- **기본 비밀번호:** `team123`
- 비밀번호는 `.streamlit/secrets.toml` 파일에서 변경 가능

## 🌐 Streamlit Cloud 배포 방법

### 1단계: GitHub에 코드 업로드

```bash
# Git 저장소 초기화
git init
git add .
git commit -m "Initial commit"

# GitHub 저장소 생성 후
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2단계: Streamlit Cloud 배포

1. [Streamlit Cloud](https://streamlit.io/cloud) 접속 및 로그인
2. "New app" 클릭
3. GitHub 저장소 연결
4. 다음 정보 입력:
   - **Repository:** your-username/team-project-management
   - **Branch:** main
   - **Main file path:** app.py
5. "Advanced settings" 클릭
6. Secrets 섹션에서 다음 추가:
   ```toml
   app_password = "your-secure-password"
   ```
7. "Deploy!" 클릭

### 3단계: 배포 완료
- 배포 완료 후 고유 URL 생성 (예: `https://your-app.streamlit.app`)
- 팀원들과 URL 공유

## 📁 프로젝트 구조

```
team-project-management/
├── app.py                      # 메인 애플리케이션 파일
├── requirements.txt            # Python 의존성
├── README.md                   # 이 파일
├── .streamlit/
│   └── secrets.toml           # 비밀번호 설정 (로컬 전용)
└── projects.db                # SQLite 데이터베이스 (자동 생성)
```

## 🗄️ 데이터베이스 스키마

### tasks 테이블
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    assignee TEXT,
    category TEXT,
    status TEXT,
    planned_progress INTEGER,
    actual_progress INTEGER,
    completion_rate INTEGER,
    deadline DATE,
    approved INTEGER,
    created_at TIMESTAMP
)
```

### team_members 테이블
```sql
CREATE TABLE team_members (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    emoji TEXT DEFAULT '👤'
)
```

## 🎨 커스터마이징

### 상태 색상 변경
`app.py`의 `load_custom_css()` 함수에서 상태 배지 색상 수정:

```css
.status-진행중 { background-color: #4299e1; }
.status-완료 { background-color: #48bb78; }
.status-일정지연 { background-color: #f56565; }
.status-검토중 { background-color: #ed8936; }
```

### 기본 팀원 수정
`app.py`의 `init_db()` 함수에서 `default_members` 리스트 수정

### 카테고리 추가
`show_add_project()` 함수의 `category` selectbox 옵션 수정

## 🔒 보안

- 기본 비밀번호는 반드시 변경하세요
- `.streamlit/secrets.toml` 파일은 절대 GitHub에 커밋하지 마세요
- `.gitignore`에 다음 추가:
  ```
  .streamlit/secrets.toml
  projects.db
  ```

## 📊 샘플 데이터

앱 첫 실행 시 10개의 샘플 프로젝트가 자동으로 생성됩니다.
- 다양한 상태 (진행 중, 완료, 일정 지연, 검토 중)
- 실제 비즈니스 시나리오 반영
- 즉시 테스트 가능

## 🛠️ 트러블슈팅

### 데이터베이스 초기화
```bash
# 기존 데이터베이스 삭제 후 재시작
rm projects.db
streamlit run app.py
```

### 의존성 오류
```bash
# 의존성 재설치
pip install --upgrade -r requirements.txt
```

### 포트 충돌
```bash
# 다른 포트에서 실행
streamlit run app.py --server.port 8502
```

## 📝 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

## 👨‍💻 개발자

Claude + Streamlit로 개발된 프로페셔널 팀 관리 솔루션

## 🤝 기여

이슈 리포트 및 풀 리퀘스트 환영합니다!

---

**문의사항이 있으시면 이슈를 등록해주세요.**
