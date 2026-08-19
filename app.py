from __future__ import annotations

import html
import json

import streamlit as st

from src.analytics import calculate_metrics, evidence_lines
from src.data_loader import DATA_DIR, customer_slice, load_demo_data
from src.memory_store import crm_card, load_memories, save_goal, selected_goal
from src.recap_service import fallback_recap, generate_recap, get_api_key, get_model
from src.styles import CSS


st.set_page_config(
    page_title="Remember Me AI | mPOP Demo",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(CSS, unsafe_allow_html=True)


def safe(value: object) -> str:
    return html.escape(str(value))


@st.cache_data
def demo_data() -> dict:
    return load_demo_data()


def metrics_for(data: dict, customer_id: str) -> dict:
    return calculate_metrics(customer_slice(data, customer_id))


def ensure_state(data: dict) -> None:
    st.session_state.setdefault("recaps", {})
    st.session_state.setdefault("recap_sources", {})
    st.session_state.setdefault("session_api_key", "")
    for customer in data["customers"]:
        cid = customer["customer_id"]
        st.session_state["recaps"].setdefault(cid, fallback_recap(cid))
        st.session_state["recap_sources"].setdefault(cid, "Demo narrative")


def header(customer_name: str | None = None) -> None:
    title = f"{safe(customer_name)}님의 투자 이야기" if customer_name else "세 사람, 세 가지 투자 이야기"
    st.markdown(
        f"""
        <section class="mpop-shell">
          <div class="mpop-top">
            <div class="mpop-brand">‹ &nbsp; <b>my PICK</b></div>
            <div class="live-pill"><i class="live-dot"></i> Remember Me AI</div>
          </div>
          <div class="hero-kicker"><span class="hero-year">2026</span> INVESTMENT RECAP ✦</div>
          <h1 class="hero-title">{title}</h1>
          <p class="hero-copy">거래·관심·콘텐츠 기록을 하나의 이야기로 연결하고,<br>내가 고른 다음 목표까지 기억해요.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def metric_cards(metrics: dict) -> None:
    cards = [
        ("🗓️", f"{metrics['avg_holding_days']:.0f}일", "평균 보유기간"),
        ("🎯", f"{metrics['top_theme_share']:.0f}%", f"{metrics['top_theme']} 집중도"),
        ("🌊", metrics["crash"]["label"].replace("급락기에 ", ""), "4월 급락기 행동"),
        ("📚", f"{metrics['content']['top_topic_minutes']}분", f"{metrics['content']['top_topic']} 관심"),
    ]
    inner = "".join(
        f'<div class="metric-card"><div class="metric-icon">{icon}</div><div class="metric-value">{safe(value)}</div><div class="metric-label">{safe(label)}</div></div>'
        for icon, value, label in cards
    )
    st.markdown(f'<div class="metric-grid">{inner}</div>', unsafe_allow_html=True)


def recap_card(metrics: dict, recap: dict, source: str) -> None:
    evidence = "".join(f'<span class="evidence">{safe(line)}</span>' for line in evidence_lines(metrics))
    source_label = "OPENAI GENERATED" if source.startswith("OpenAI") else "GROUNDED DEMO"
    st.markdown(
        f"""
        <article class="recap-card">
          <div class="pattern-chip">✦ AI PATTERN · {source_label}</div>
          <div class="pattern-title">{safe(recap['headline'])}</div>
          <p class="pattern-story">{safe(recap['story'])}</p>
          <div class="evidence-row">{evidence}</div>
          <div class="split-note">
            <div class="note good"><div class="note-label">잘 이어온 점</div><div class="note-text">{safe(recap['strength'])}</div></div>
            <div class="note watch"><div class="note-label">함께 점검할 점</div><div class="note-text">{safe(recap['watchout'])}</div></div>
          </div>
        </article>
        """,
        unsafe_allow_html=True,
    )


def crm_html(card: dict) -> str:
    return f"""
      <article class="crm-card {safe(card['tone'])}">
        <div class="crm-icon">{safe(card['icon'])}</div>
        <div class="crm-eyebrow">{safe(card['eyebrow'])}</div>
        <div class="crm-title">{safe(card['title'])}</div>
        <div class="crm-body">{safe(card['body'])}</div>
        <span class="crm-cta">{safe(card['cta'])} &nbsp;›</span>
      </article>
    """


def ai_settings(customer: dict, metrics: dict) -> None:
    with st.expander("AI 데모 설정 · OpenAI API 연결", expanded=False):
        st.caption("키는 현재 Streamlit 세션에서만 사용하며 파일에 저장하지 않습니다.")
        key = st.text_input(
            "OpenAI API key",
            type="password",
            value=st.session_state.get("session_api_key", ""),
            placeholder="sk-... (미입력 시 준비된 데모 문구 사용)",
        )
        st.session_state["session_api_key"] = key
        model = get_model(st.secrets)
        left, right = st.columns([1, 2])
        with left:
            generate_clicked = st.button("AI Recap 다시 만들기", type="primary", use_container_width=True)
        with right:
            st.caption(f"Responses API · {model} · 정형 지표만 전송")
        if generate_clicked:
            api_key = get_api_key(key, st.secrets)
            if not api_key:
                st.warning("API key를 입력하거나 .streamlit/secrets.toml에 설정해주세요.")
                return
            try:
                with st.spinner("2026년 행동을 고객의 이야기로 바꾸는 중..."):
                    recap = generate_recap(customer, metrics, api_key, model)
                st.session_state["recaps"][customer["customer_id"]] = recap
                st.session_state["recap_sources"][customer["customer_id"]] = f"OpenAI · {model}"
                st.success("근거 지표를 바탕으로 새 Recap을 만들었습니다.")
                st.rerun()
            except Exception as error:
                st.error(f"OpenAI 호출에 실패했습니다. 준비된 데모 문구를 유지합니다. ({error})")


def personal_view(data: dict) -> None:
    customer_names = [item["name"] for item in data["customers"]]
    current_name = st.session_state.get("customer_selector", customer_names[0])
    customer = next(item for item in data["customers"] if item["name"] == current_name)
    header(customer["name"])
    name = st.selectbox(
        "고객 선택",
        customer_names,
        key="customer_selector",
        label_visibility="collapsed",
    )
    customer = next(item for item in data["customers"] if item["name"] == name)
    cid = customer["customer_id"]
    metrics = metrics_for(data, cid)
    recap = st.session_state["recaps"][cid]
    source = st.session_state["recap_sources"][cid]

    st.markdown('<div class="section-title">올해의 투자 리듬</div><div class="section-sub">숫자를 나열하지 않고, 반복된 행동을 먼저 보여드려요.</div>', unsafe_allow_html=True)
    metric_cards(metrics)
    recap_card(metrics, recap, source)

    st.markdown('<div class="section-title">2027년, 무엇을 이어가고 싶나요?</div><div class="section-sub">직접 고른 목표만 Memory에 저장하고 다음 콘텐츠에 반영합니다.</div>', unsafe_allow_html=True)
    current_goal = selected_goal(cid, customer["default_goal"])
    default_index = customer["goal_options"].index(current_goal) if current_goal in customer["goal_options"] else 0
    goal = st.radio(
        "2027 목표",
        customer["goal_options"],
        index=default_index,
        horizontal=True,
        key=f"goal_{cid}",
        label_visibility="collapsed",
    )
    if st.button("이 목표를 기억해줘", type="primary", use_container_width=True, key=f"save_{cid}"):
        save_goal(cid, customer["name"], goal)
        st.success(f"{customer['name']}님의 2027 목표를 Memory JSON에 저장했어요.")
        st.rerun()

    goal = selected_goal(cid, customer["default_goal"])
    card = crm_card(customer, metrics, goal)
    st.markdown('<div class="section-title">Stay With Me</div><div class="section-sub">저장된 목표와 올해 행동을 연결한 다음 CRM 카드예요.</div>', unsafe_allow_html=True)
    st.markdown(crm_html(card), unsafe_allow_html=True)
    st.markdown(
        '<div class="data-note"><b>설계 원칙</b> · 이 화면은 투자 조언이나 종목 추천이 아니라, 과거 행동을 객관적으로 돌아보고 고객이 직접 다음 목표를 선택하도록 돕는 데모입니다.</div>',
        unsafe_allow_html=True,
    )
    ai_settings(customer, metrics)


def compare_view(data: dict) -> None:
    header(None)
    st.markdown('<div class="section-title">같은 시장, 서로 다른 Memory</div><div class="section-sub">모두 4월 −8.4% 급락을 겪었지만 행동·관심·목표에 따라 Recap과 CRM이 달라집니다.</div>', unsafe_allow_html=True)
    columns = st.columns(3)
    for column, customer in zip(columns, data["customers"]):
        cid = customer["customer_id"]
        metrics = metrics_for(data, cid)
        recap = st.session_state["recaps"][cid]
        goal = selected_goal(cid, customer["default_goal"])
        card = crm_card(customer, metrics, goal)
        with column:
            st.markdown(
                f"""
                <article class="compare-card" style="--accent:{safe(customer['accent'])};--soft:{safe(customer['soft'])}">
                  <div class="compare-avatar">{safe(customer['avatar'])}</div>
                  <div class="compare-name">{safe(customer['name'])}</div>
                  <div class="compare-type">{safe(customer['persona'])} · {safe(recap['pattern_name'])}</div>
                  <div class="compare-headline">{safe(recap['headline'])}</div>
                  <div class="compare-story">{safe(recap['story'])}</div>
                  <div class="compare-metrics">
                    <div class="compare-metric"><b>{metrics['avg_holding_days']:.0f}일</b><span>평균 보유</span></div>
                    <div class="compare-metric"><b>{metrics['top_theme_share']:.0f}%</b><span>상위 테마</span></div>
                    <div class="compare-metric"><b>{safe(metrics['crash']['code'].upper())}</b><span>급락기 행동</span></div>
                    <div class="compare-metric"><b>{metrics['content']['top_topic_minutes']}분</b><span>상위 콘텐츠</span></div>
                  </div>
                  <span class="goal-badge">2027 목표 · {safe(goal)}</span>
                </article>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(crm_html(card), unsafe_allow_html=True)

    st.markdown(
        '<div class="data-note"><b>동일 이벤트 통제</b> · 세 고객 모두 2026-04-07~10의 동일한 기술주 급락 구간으로 분석했습니다. 차이는 시장이 아니라 그 구간의 매수·매도·보유 행동에서 나옵니다.</div>',
        unsafe_allow_html=True,
    )


def memory_view(data: dict) -> None:
    header("Memory")
    st.markdown('<div class="section-title">AI Customer Memory</div><div class="section-sub">고객이 직접 제공한 목표(Zero-party Data)가 장기 CRM 연결점이 됩니다.</div>', unsafe_allow_html=True)
    memories = load_memories()
    st.markdown(f'<div class="memory-box">{safe(json.dumps(memories, ensure_ascii=False, indent=2))}</div>', unsafe_allow_html=True)
    st.download_button(
        "Memory JSON 다운로드",
        data=json.dumps(memories, ensure_ascii=False, indent=2),
        file_name="customer_memory.json",
        mime="application/json",
        use_container_width=True,
    )
    st.markdown('<div class="section-title">가상 고객 원천 데이터</div><div class="section-sub">데모 재현을 위해 거래·관심·콘텐츠 데이터를 분리했습니다.</div>', unsafe_allow_html=True)
    download_columns = st.columns(3)
    files = [
        ("거래 CSV", "trades.csv", "text/csv"),
        ("관심 CSV", "interest_events.csv", "text/csv"),
        ("콘텐츠 CSV", "content_events.csv", "text/csv"),
    ]
    for column, (label, filename, mime) in zip(download_columns, files):
        with column:
            st.download_button(label, (DATA_DIR / filename).read_bytes(), filename, mime, use_container_width=True)
    calculated = {
        customer["customer_id"]: metrics_for(data, customer["customer_id"])
        for customer in data["customers"]
    }
    export_columns = st.columns(2)
    with export_columns[0]:
        st.download_button(
            "고객 설정 JSON",
            (DATA_DIR / "customers.json").read_bytes(),
            "customers.json",
            "application/json",
            use_container_width=True,
        )
    with export_columns[1]:
        st.download_button(
            "계산 지표 JSON",
            json.dumps(calculated, ensure_ascii=False, indent=2),
            "behavior_metrics.json",
            "application/json",
            use_container_width=True,
        )
    st.markdown(
        '<div class="data-note"><b>데모 데이터</b> · 화면의 고객·거래·관심·콘텐츠 기록은 모두 가상이며 실제 고객정보를 포함하지 않습니다. 실제 적용 시 데이터 보존기간, 동의, 설명 가능성, 준법 검토가 필요합니다.</div>',
        unsafe_allow_html=True,
    )


def footer_nav() -> None:
    st.markdown(
        """
        <div class="ticker"><b>KOSPI</b><span class="down">▼ 2,842.17&nbsp; 1.18%</span><span class="closed">장종료</span></div>
        <div class="bottom-nav"><span>⌂ 홈</span><span>☆ 관심종목</span><span>⌁ 종합차트</span><span>☰ 메뉴</span></div>
        """,
        unsafe_allow_html=True,
    )


data = demo_data()
ensure_state(data)
navigation = st.radio(
    "페이지",
    ["나의 리캡", "3인 비교", "Memory JSON"],
    horizontal=True,
    label_visibility="collapsed",
)

if navigation == "나의 리캡":
    personal_view(data)
elif navigation == "3인 비교":
    compare_view(data)
else:
    memory_view(data)

footer_nav()
