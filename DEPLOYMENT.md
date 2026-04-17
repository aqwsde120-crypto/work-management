# Streamlit Cloud 배포 가이드 ☁️

## 완벽한 배포를 위한 단계별 가이드

### 사전 준비사항
- ✅ GitHub 계정
- ✅ Git 기본 지식
- ✅ 프로젝트 파일 준비 완료

---

## 📋 Step 1: GitHub 저장소 생성

### 1-1. GitHub에서 새 저장소 만들기
1. GitHub 로그인 → https://github.com
2. 우측 상단 "+" → "New repository" 클릭
3. 저장소 설정:
   - Repository name: `team-project-management`
   - Description: "팀 프로젝트 관리 시스템"
   - Public 또는 Private 선택 (Streamlit Cloud는 둘 다 지원)
   - "Create repository" 클릭

### 1-2. 로컬에서 코드 업로드
```bash
# 프로젝트 폴더로 이동
cd team-project-management

# Git 초기화
git init

# 모든 파일 추가 (.gitignore에 의해 자동 필터링)
git add .

# 커밋
git commit -m "Initial commit: 팀 프로젝트 관리 시스템"

# GitHub 저장소 연결 (YOUR_USERNAME을 실제 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/team-project-management.git

# 업로드
git branch -M main
git push -u origin main
```

---

## 🚀 Step 2: Streamlit Cloud 배포

### 2-1. Streamlit Cloud 가입 및 로그인
1. https://streamlit.io/cloud 접속
2. "Sign up" 클릭
3. GitHub 계정으로 로그인
4. 필요한 권한 승인

### 2-2. 새 앱 생성
1. Streamlit Cloud 대시보드에서 "New app" 클릭
2. 다음 정보 입력:
   ```
   Repository: YOUR_USERNAME/team-project-management
   Branch: main
   Main file path: app.py
   ```
3. "Advanced settings" 클릭

### 2-3. Secrets 설정 (중요!)
"Secrets" 섹션에 다음 내용 복사:
```toml
app_password = "your_secure_password_here"
```

**보안 팁:**
- 기본 비밀번호(team123) 절대 사용 금지!
- 강력한 비밀번호로 변경
- 예: `app_password = "MySecureP@ssw0rd2024!"`

### 2-4. Python 버전 설정 (선택사항)
`.streamlit/config.toml`이 자동으로 적용됩니다.

필요시 `runtime.txt` 파일 생성:
```
python-3.11
```

### 2-5. 배포 시작!
"Deploy!" 버튼 클릭

---

## ⏳ Step 3: 배포 진행 상황 확인

### 배포 중 로그 확인
- 실시간 로그가 표시됩니다
- 일반적으로 2-5분 소요

### 성공 메시지 확인
```
Your app is live! 🎉
```

### 배포 완료 후
- 고유 URL 생성: `https://your-app-name.streamlit.app`
- 브라우저에서 자동으로 열림

---

## 🔧 Step 4: 배포 후 설정

### 앱 URL 커스터마이징
1. Streamlit Cloud 대시보드
2. 앱 설정 → "Settings"
3. "App URL" 수정 가능
   - 예: `team-management-company.streamlit.app`

### 도메인 연결 (Pro 플랜)
- 자체 도메인 연결 가능
- 예: `projects.yourcompany.com`

---

## 📱 Step 5: 팀원들과 공유

### URL 공유
```
🎉 팀 프로젝트 관리 시스템이 배포되었습니다!

접속 주소: https://your-app.streamlit.app
비밀번호: [안전하게 전달]

사용 가이드: [GitHub README 링크]
```

### 모바일 접근
- 모바일 브라우저에서 동일한 URL 접속
- 반응형 디자인으로 자동 최적화

---

## 🔄 Step 6: 앱 업데이트

### 코드 수정 후 배포
```bash
# 코드 수정

# 변경사항 커밋
git add .
git commit -m "기능 개선: 새로운 필터 추가"

# GitHub에 푸시
git push origin main
```

**자동 재배포:**
- GitHub에 푸시하면 자동으로 재배포됨
- 1-2분 후 변경사항 반영

### 수동 재배포
1. Streamlit Cloud 대시보드
2. 앱 선택 → "Reboot" 클릭

---

## 📊 모니터링 및 관리

### 앱 상태 확인
- Streamlit Cloud 대시보드에서 실시간 상태 확인
- 리소스 사용량 모니터링

### 로그 확인
- "Manage app" → "Logs" 탭
- 에러 발생 시 디버깅 정보

### 앱 중지/재시작
- "Manage app" → "Reboot" (재시작)
- "Delete" (완전 삭제)

---

## 🎯 프로 팁

### 1. 환경 변수 사용
Secrets에 추가 설정 저장 가능:
```toml
app_password = "secure_pass"
admin_email = "admin@company.com"
max_file_size = "100"
```

앱에서 사용:
```python
admin_email = st.secrets.get("admin_email", "default@email.com")
```

### 2. 성능 최적화
- 캐싱 적극 활용: `@st.cache_data`, `@st.cache_resource`
- 대용량 데이터는 외부 DB 사용 권장
- 이미지는 압축하여 사용

### 3. 보안 강화
- Secrets에 민감 정보 저장
- `.gitignore`로 로컬 설정 파일 보호
- 정기적으로 비밀번호 변경

### 4. 백업
- GitHub에 코드 백업 자동화
- 데이터베이스는 정기적으로 export

---

## 🆘 트러블슈팅

### 배포 실패 시
**문제:** "ModuleNotFoundError"
**해결:** `requirements.txt`에 모든 패키지 명시

**문제:** "Secrets not found"
**해결:** Streamlit Cloud의 Secrets 설정 확인

**문제:** "App crashed"
**해결:** 로그 확인 → 에러 메시지 분석

### 성능 문제
**문제:** 앱이 느려요
**해결:** 
- 캐싱 추가
- 데이터 쿼리 최적화
- 리소스 사용량 확인

### 접근 불가
**문제:** URL이 작동하지 않아요
**해결:**
- Streamlit Cloud 상태 확인
- 브라우저 캐시 삭제
- 다른 브라우저에서 시도

---

## 📞 지원

### 공식 리소스
- 📚 [Streamlit 문서](https://docs.streamlit.io)
- 💬 [커뮤니티 포럼](https://discuss.streamlit.io)
- 🐛 [GitHub Issues](https://github.com/streamlit/streamlit/issues)

### 한국어 리소스
- [Streamlit 한국 사용자 그룹](https://www.facebook.com/groups/streamlitkorea)

---

## ✅ 배포 체크리스트

배포 전 확인사항:
- [ ] GitHub 저장소 생성 완료
- [ ] 모든 파일 커밋 및 푸시 완료
- [ ] `.gitignore`에 민감 파일 추가
- [ ] `requirements.txt` 정확성 확인
- [ ] Streamlit Cloud 계정 준비
- [ ] Secrets 설정 준비 (강력한 비밀번호)

배포 후 확인사항:
- [ ] 앱 정상 작동 확인
- [ ] 비밀번호 로그인 테스트
- [ ] 모바일 반응형 확인
- [ ] 모든 기능 테스트
- [ ] 팀원들에게 URL 공유

---

**성공적인 배포를 기원합니다! 🚀**

문의사항: GitHub Issues 또는 README 참조
