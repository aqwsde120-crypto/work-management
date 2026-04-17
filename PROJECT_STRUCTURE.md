# 📁 프로젝트 파일 구조

```
team-project-management/
│
├── 📄 app.py                      # 메인 Streamlit 애플리케이션
├── 📄 requirements.txt            # Python 패키지 의존성
├── 📄 .gitignore                  # Git 제외 파일 목록
│
├── 📂 .streamlit/                 # Streamlit 설정 폴더
│   ├── 📄 secrets.toml           # 비밀번호 설정 (로컬 전용)
│   └── 📄 config.toml            # 앱 테마 및 서버 설정
│
├── 📄 README.md                   # 프로젝트 개요 및 설치 가이드
├── 📄 QUICKSTART.md              # 빠른 시작 가이드 (1분 설치)
├── 📄 DEPLOYMENT.md              # Streamlit Cloud 배포 상세 가이드
├── 📄 FEATURES.md                # 전체 기능 상세 문서
├── 📄 PROJECT_STRUCTURE.md       # 이 파일
│
└── 📄 projects.db                # SQLite 데이터베이스 (자동 생성)
```

---

## 파일별 설명

### 📄 app.py
**역할**: 메인 애플리케이션 파일  
**크기**: ~650 줄  
**포함 기능**:
- 데이터베이스 초기화
- 5개 주요 화면 (대시보드, 테이블, 칸반, 추가, 팀원 관리)
- 커스텀 CSS 스타일
- 비밀번호 인증
- 데이터 필터링 및 Excel 내보내기

**주요 함수**:
- `init_db()`: 데이터베이스 및 샘플 데이터 생성
- `load_tasks()`: 프로젝트 데이터 로드
- `show_dashboard()`: 대시보드 화면
- `show_project_table()`: 프로젝트 테이블 화면
- `show_kanban_board()`: 칸반 보드 화면
- `show_add_project()`: 프로젝트 추가 화면
- `show_team_management()`: 팀원 관리 화면

---

### 📄 requirements.txt
**역할**: Python 패키지 의존성 정의  
**내용**:
```
streamlit==1.32.0
pandas==2.2.1
plotly==5.20.0
openpyxl==3.1.2
```

**설치 방법**:
```bash
pip install -r requirements.txt
```

---

### 📂 .streamlit/ 폴더

#### 📄 secrets.toml
**역할**: 비밀번호 및 민감 정보 저장  
**주의**: `.gitignore`에 포함되어 GitHub에 커밋되지 않음  
**내용**:
```toml
app_password = "team123"
```

**Streamlit Cloud 배포 시**:
- GitHub에 업로드하지 말 것
- Streamlit Cloud의 Secrets 섹션에 수동 입력

#### 📄 config.toml
**역할**: Streamlit 앱 테마 및 서버 설정  
**설정 항목**:
- 테마 색상 (primaryColor, backgroundColor 등)
- 서버 설정 (headless mode, CORS)
- 브라우저 설정 (통계 수집 비활성화)

---

### 📄 .gitignore
**역할**: Git 버전 관리에서 제외할 파일 지정  
**주요 제외 항목**:
- `.streamlit/secrets.toml` (비밀번호)
- `*.db` (데이터베이스)
- `__pycache__/` (Python 캐시)
- `venv/` (가상환경)
- `.DS_Store` (macOS)

---

### 📄 README.md
**역할**: 프로젝트 개요 및 종합 가이드  
**포함 내용**:
- 주요 기능 소개
- 로컬 실행 방법
- Streamlit Cloud 배포 요약
- 데이터베이스 스키마
- 커스터마이징 가이드
- 트러블슈팅

**대상 독자**: 개발자 및 프로젝트 관리자

---

### 📄 QUICKSTART.md
**역할**: 1분 안에 시작할 수 있는 간단한 가이드  
**포함 내용**:
- 3단계 설치 과정
- 주요 사용 팁
- 빠른 문제 해결
- 다음 단계 안내

**대상 독자**: 빠르게 시작하고 싶은 사용자

---

### 📄 DEPLOYMENT.md
**역할**: Streamlit Cloud 배포 완벽 가이드  
**포함 내용**:
- GitHub 저장소 생성 및 업로드
- Streamlit Cloud 회원가입 및 설정
- Secrets 설정 방법
- 배포 후 관리 및 업데이트
- 상세 트러블슈팅
- 프로 팁 및 최적화

**대상 독자**: 클라우드 배포를 원하는 사용자

---

### 📄 FEATURES.md
**역할**: 전체 기능 상세 문서  
**포함 내용**:
- 각 화면별 기능 상세 설명
- 기술적 특징 및 구조
- 데이터베이스 스키마 설명
- 사용 시나리오
- 향후 개선 가능한 기능

**대상 독자**: 심화 사용자 및 기능 확장 개발자

---

### 📄 projects.db
**역할**: SQLite 로컬 데이터베이스  
**생성 시점**: 앱 첫 실행 시 자동 생성  
**테이블**:
1. `tasks`: 프로젝트/업무 데이터 (13개 필드)
2. `team_members`: 팀원 정보 (3개 필드)

**샘플 데이터**: 10개의 실제 비즈니스 시나리오 프로젝트

**주의사항**:
- `.gitignore`에 포함되어 GitHub에 업로드되지 않음
- 백업 필요 시 별도로 저장
- 초기화: `rm projects.db` 후 앱 재시작

---

## 필수 파일 체크리스트

### 로컬 실행용
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `.streamlit/secrets.toml`
- ✅ `.streamlit/config.toml`

### 배포용 (GitHub)
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `.gitignore`
- ✅ `README.md`
- ✅ `.streamlit/config.toml`
- ❌ `.streamlit/secrets.toml` (제외! Streamlit Cloud에서 수동 설정)
- ❌ `projects.db` (제외!)

### 문서 (선택사항)
- 📘 `QUICKSTART.md`
- 📗 `DEPLOYMENT.md`
- 📕 `FEATURES.md`
- 📙 `PROJECT_STRUCTURE.md`

---

## 디렉토리 권장 사항

### 개발 환경
```
my-workspace/
└── team-project-management/
    ├── app.py
    ├── requirements.txt
    ├── .gitignore
    ├── .streamlit/
    │   ├── secrets.toml
    │   └── config.toml
    ├── venv/                    # 가상환경 (생성 후)
    ├── projects.db              # 자동 생성
    └── [문서 파일들]
```

### 프로덕션 (GitHub)
```
team-project-management/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── .streamlit/
│   └── config.toml
└── [문서 파일들]
```

---

## 파일 크기 참고

| 파일 | 예상 크기 |
|------|-----------|
| app.py | ~25 KB |
| requirements.txt | ~100 B |
| .gitignore | ~200 B |
| README.md | ~8 KB |
| QUICKSTART.md | ~4 KB |
| DEPLOYMENT.md | ~12 KB |
| FEATURES.md | ~15 KB |
| .streamlit/secrets.toml | ~50 B |
| .streamlit/config.toml | ~300 B |
| projects.db | ~20 KB |

**전체 프로젝트**: ~85 KB (데이터베이스 제외)

---

## 버전 관리 (Git) 권장사항

### 커밋 메시지 예시
```bash
git commit -m "Initial commit: 프로젝트 구조 설정"
git commit -m "feat: 대시보드 차트 추가"
git commit -m "fix: Excel 다운로드 오류 수정"
git commit -m "docs: README 업데이트"
git commit -m "style: CSS 스타일 개선"
```

### 브랜치 전략
```
main            # 프로덕션 (Streamlit Cloud 배포)
└── develop     # 개발 브랜치
    ├── feature/dashboard-improvements
    ├── feature/kanban-drag-drop
    └── fix/excel-export-bug
```

---

**프로젝트 구조에 대한 문의: GitHub Issues**
