# Remember Me AI — CSV to my PICK Demo

고객의 2026년 연간 투자 활동 CSV를 읽어 **AI Investment Recap → AI 추천 목표 → 개인화 my PICK**으로 연결하는 Streamlit 데모입니다.

## 사용자 흐름

```text
연간 활동 CSV 업로드
        ↓
Python 스키마 검증·행동지표 계산
        ↓
AI가 Recap 5개 장면과 2027 목표 3개 생성
        ↓
고객이 AI 추천 목표 중 하나를 직접 선택
        ↓
AI가 Recap·목표에 맞는 my PICK 모듈 구성
        ↓
“새롭게 업데이트된 my PICK을 확인해볼까요?” 팝업
        ↓
개인화된 my PICK 페이지
```

API key가 없으면 계산된 지표에 기반한 데모 문구로 전체 흐름이 동작합니다. API key가 연결되면 Recap의 모든 카피, 세 가지 목표, my PICK 구성을 OpenAI Responses API가 Structured Output으로 생성합니다.

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

실제 키가 포함된 `.streamlit/secrets.toml`은 Git에 올리지 마세요. 앱의 `AI 연결 설정`에 키를 입력하면 현재 세션에서만 사용할 수도 있습니다.

## 통합 CSV 스키마

앱 첫 화면에서 완성된 샘플과 빈 템플릿을 다운로드할 수 있습니다.

| 열 | 설명 | 이벤트별 필수 여부 |
|---|---|---|
| `customer_id` | 가상 고객 ID | 권장 |
| `customer_name` | 화면 표시 이름 | 권장 |
| `event_date` | `YYYY-MM-DD` | 필수 |
| `event_type` | `TRADE`, `INTEREST`, `CONTENT` | 필수 |
| `symbol`, `asset_name` | 종목 코드·이름 | TRADE |
| `market` | 국내, 미국 등 | TRADE/INTEREST |
| `side` | `BUY` 또는 `SELL` | TRADE |
| `quantity`, `price` | 체결 수량·가격 | TRADE |
| `theme` | AI·반도체, 채권 등 | 권장 |
| `content_type`, `content_topic` | 콘텐츠 형식·주제 | CONTENT |
| `dwell_seconds`, `completed` | 체류시간·완료 여부 | CONTENT |

기존 `data/trades.csv`처럼 `trade_date`를 사용하는 거래 전용 CSV도 호환됩니다.

## 계산과 AI의 역할 분리

Python이 먼저 다음 값을 결정적으로 계산합니다.

- 수량 가중 FIFO 평균 보유기간
- 매수금액 기준 테마 집중도와 HHI
- 동일 급락 관찰 구간의 매수·매도·보유 행동
- 가장 자주 거래한 종목·시장
- 관심종목 및 콘텐츠 주제·체류시간

AI에는 원본 CSV가 아니라 검증·집계된 지표만 전달됩니다. AI는 이 근거를 바탕으로 다음 항목을 생성합니다.

- 감성적이지만 사실에 근거한 Recap 5개 장면
- 고객 행동과 연결된 새로운 2027 목표 3개
- 고객이 고른 목표에 맞는 my PICK 관심종목·시장요약·콘텐츠·루틴 구성

특정 종목 추천, 가격 전망, 수익 보장, 매수·매도 지시는 프롬프트에서 금지합니다.

## 주요 파일

```text
app.py                       전체 Streamlit 상태 흐름과 UI
src/activity_upload.py       CSV 검증·통합·샘플 생성
src/analytics.py             결정적 행동지표 계산
src/recap_service.py         2단계 OpenAI 생성과 폴백
src/memory_store.py          Recap·선택 목표·my PICK JSON 저장
src/styles.py                Recap·팝업·my PICK 모바일 스타일
memory/customer_memory.json  데모용 AI Customer Memory
```

## 테스트

```bash
python -m unittest discover -s tests -v
```

> 모든 고객·거래·시장 데이터는 시연용 가상 데이터입니다. Streamlit Community Cloud의 로컬 JSON은 영구 저장이 보장되지 않으므로 실제 서비스에서는 외부 DB로 교체해야 합니다.
