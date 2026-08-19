# Remember Me AI — Recap to my PICK Demo

세 명의 가상 고객 중 한 명을 선택해 **투자 활동 분석 → AI Investment Recap → AI 추천 목표 선택 → 개인화 my PICK**으로 연결하는 Streamlit 데모입니다.

## 사용자 흐름

```text
가상 고객 3명 중 한 명 선택
        ↓
2026년 거래·관심·콘텐츠 활동 분석
        ↓
AI가 Recap 5개 장면 생성
        ↓
AI가 my PICK용 AI 추천 목표 3개 생성
        ↓
고객이 AI 추천 목표 중 하나를 선택
        ↓
AI가 관련 리포트·뉴스·시황을 my PICK에 구성
        ↓
업데이트 안내 팝업 → 개인화된 my PICK
```

추천되는 목표는 `매월 기록하기`, `보유 기준 만들기` 같은 고객 행동 과제가 아닙니다. 다음과 같이 **my PICK이 지속적으로 찾아서 보여줄 정보의 방향**을 의미합니다.

- AI·반도체 흐름 깊이 보기 → 업황 리포트·핵심 기업 뉴스
- 시장 변동성 먼저 읽기 → 급등락 시황·리스크 해설
- 금리·채권 변화 살펴보기 → 중앙은행 뉴스·채권시장 리포트

API key가 없으면 계산된 지표에 기반한 고객별 데모 문구로 전체 흐름이 동작합니다. API key가 연결되면 Recap, AI 추천 목표, my PICK 구성을 OpenAI Responses API가 Structured Output으로 생성합니다.

## 실행

```bash
cd /Users/kook/Desktop/SamsungSecurities_AI_Recap
source .venv/bin/activate
streamlit run app.py
```

## Streamlit Secrets

Streamlit Community Cloud의 `Advanced settings → Secrets`에 입력합니다.

```toml
OPENAI_API_KEY = "sk-proj-..."
OPENAI_MODEL = "gpt-5.4-mini"
```

실제 키가 포함된 `.streamlit/secrets.toml`은 Git에 올리지 마세요.

## AI 파이프라인

Python은 가상 고객의 연간 기록에서 다음 값을 먼저 계산합니다.

- 수량 가중 FIFO 평균 보유기간
- 매수금액 기준 테마 집중도와 HHI
- 동일 급락 관찰 구간의 매수·매도·보유 행동
- 가장 자주 거래한 종목·시장
- 관심종목 및 콘텐츠 주제·체류시간

AI에는 원본 행이 아니라 검증·집계된 지표만 전달됩니다. 첫 번째 호출은 Recap과 AI 추천 목표 3개를 만들고, 고객이 목표를 고르면 두 번째 호출이 카탈로그에서 관련 리포트·뉴스·시황을 골라 my PICK을 구성합니다.

특정 종목 추천, 가격 전망, 수익 보장, 매수·매도 지시는 프롬프트에서 금지합니다.

## 주요 파일

```text
app.py                       3인 선택과 전체 Streamlit 흐름
src/activity_upload.py       가상 고객 데이터 통합
src/analytics.py             결정적 행동지표 계산
src/recap_service.py         Recap·AI 추천 목표·my PICK AI 생성
src/memory_store.py          Recap·선택 목표·my PICK JSON 저장
src/styles.py                Recap·팝업·my PICK 모바일 스타일
memory/customer_memory.json  데모용 AI Customer Memory
```

## 테스트

```bash
python -m unittest discover -s tests -v
```

> 모든 고객·거래·시장 데이터는 시연용 가상 데이터입니다. 실제 my PICK 연동 시 데모 콘텐츠 카탈로그를 삼성증권 리서치·뉴스 API로 교체해야 합니다.
