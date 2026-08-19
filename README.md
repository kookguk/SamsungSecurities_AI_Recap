# Remember Me AI — mPOP Streamlit Demo

삼성증권 mPOP 안의 개인화 페이지를 가정한 **AI Investment Memory** 데모입니다. 세 가상 고객의 2026년 거래·관심·콘텐츠 행동을 Python으로 계산하고, OpenAI가 근거 기반 Recap과 AI Pattern 문구를 생성합니다. 고객이 선택한 2027 목표는 JSON에 저장되어 다음 CRM 카드에 반영됩니다.

## 데모에서 볼 수 있는 것

- `나의 리캡`: 고객별 행동지표, AI Pattern, 근거, 2027 목표 설정, Stay With Me CRM
- `3인 비교`: 동일한 4월 급락 상황에서도 서로 다른 행동·Recap·목표·CRM 비교
- `Memory JSON`: 저장된 Zero-party 목표와 원천 CSV 다운로드
- API key가 없어도 준비된 문구로 전체 흐름 실행
- API key를 넣으면 OpenAI Responses API로 Recap 실시간 재생성

## 실행

Python 3.11 이상 환경에서 실행할 수 있습니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속합니다.

## OpenAI API key 설정

가장 간단한 방법은 앱 하단의 `AI 데모 설정 · OpenAI API 연결`을 열고 키를 붙여넣는 것입니다. 키는 현재 Streamlit 세션에서만 사용되며 파일에 저장되지 않습니다.

환경변수 방식:

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-5.4-mini"
streamlit run app.py
```

Streamlit secrets 방식:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

복사한 파일에 키를 입력하세요. 실제 `secrets.toml`은 Git에서 제외됩니다.

## 데이터와 계산 기준

```text
data/customers.json          고객 페르소나·목표 후보
data/trades.csv              주문 체결 이벤트
data/interest_events.csv     관심종목·시세·리서치 조회
data/content_events.csv      콘텐츠 주제·체류·완료
data/market_events.json      동일 급락 관찰 구간
memory/customer_memory.json  고객이 직접 선택한 2027 목표
```

- 평균 보유기간: 종목별 FIFO, 수량 가중. 연말 미매도 물량은 2026-12-31까지 포함
- 테마 집중도: 매수금액 기준 상위 테마 비중과 HHI
- 급락기 행동: 2026-04-07~10 매수·매도 금액 비교 (`added` / `held` / `reduced`)
- 콘텐츠 관심: 주제별 체류시간, 완료 수, 선호 포맷

LLM에는 원천 거래내역 대신 계산된 정형 지표를 보내며, JSON Schema Structured Output을 사용합니다. 프롬프트는 수익률 예측·종목 추천·매매 지시를 금지하고 관찰 가능한 과거 행동만 설명하도록 제한합니다.

## 테스트

```bash
python -m unittest discover -s tests -v
```

> 모든 고객 및 시장 데이터는 시연용 가상 데이터입니다. 실제 서비스 적용에는 개인정보 동의·보존기간·투자권유·준법 검토가 필요합니다.
