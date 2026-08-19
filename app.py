from __future__ import annotations

import html
import json
from typing import Any

import streamlit as st

from src.activity_upload import parse_activity_csv, sample_activity_csv
from src.memory_store import load_memories, save_journey_memory
from src.recap_service import (
    fallback_journey,
    fallback_mypick,
    generate_journey,
    generate_mypick_plan,
    get_api_key,
    get_model,
)
from src.styles import CSS


st.set_page_config(
    page_title="Remember me AI | 2026 mPOP Recap",
    page_icon="💙",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(CSS, unsafe_allow_html=True)


SLIDE_ICONS = {"taste": "✦", "stock": "◎", "market": "⌁", "pattern": "AI", "journey": "➜"}
GOAL_ICONS = {"compass": "⌖", "habit": "↻", "balance": "◫", "study": "▤", "shield": "◇", "calendar": "▦"}
CONTENT_ICONS = {"report": "▥", "news": "N", "lesson": "▤", "market": "⌁", "etf": "◫", "tax": "₩", "routine": "↻"}


def safe(value: object) -> str:
    return html.escape(str(value))


def initialize_state() -> None:
    defaults = {
        "flow_stage": "upload",
        "analysis_package": None,
        "journey": None,
        "selected_goal": None,
        "mypick_plan": None,
        "flow_notice": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def reset_flow() -> None:
    for key in ("analysis_package", "journey", "selected_goal", "mypick_plan", "flow_notice"):
        st.session_state[key] = None
    st.session_state["flow_stage"] = "upload"
    st.rerun()


def progress_bar(active: int) -> None:
    labels = ["AI 투자 활동 분석", "AI Recap", "AI 추천 목표", "my PICK"]
    steps = "".join(
        f'<div class="flow-step {"done" if index < active else "active" if index == active else ""}"><i>{index + 1}</i><span>{label}</span></div>'
        for index, label in enumerate(labels)
    )
    st.markdown(f'<div class="flow-progress">{steps}</div>', unsafe_allow_html=True)


def app_wordmark(back_label: str = "mPOP") -> None:
    st.markdown(
        f'<div class="app-wordmark"><span>‹ &nbsp;{safe(back_label)}</span><b>Remember Me <em>AI</em></b></div>',
        unsafe_allow_html=True,
    )


def run_customer_analysis(customer_id: str, customer_name: str) -> None:
    try:
        with st.status("투자 기록을 읽고 있어요", expanded=True) as status:
            st.write(f"{customer_name}님의 연간 거래·관심·콘텐츠 기록을 불러오는 중...")
            package = parse_activity_csv(sample_activity_csv(customer_id), customer_name)
            st.write("관심 종목·테마를 불러오는 중...")
            api_key = get_api_key(secrets=st.secrets)
            model = get_model(st.secrets)
            if api_key:
                st.write("AI가 Recap과 다음 해 목표를 생성하는 중...")
                try:
                    journey = generate_journey(package["customer"], package["metrics"], api_key, model)
                except Exception as error:
                    journey = fallback_journey(package["customer"], package["metrics"])
                    st.session_state["flow_notice"] = f"OpenAI 호출이 완료되지 않아 근거 기반 데모 문구를 사용했습니다: {error}"
            else:
                journey = fallback_journey(package["customer"], package["metrics"])
                st.session_state["flow_notice"] = "API key가 없어 근거 기반 데모 문구로 진행했습니다. Secrets 연결 후에는 AI가 모든 문구를 새로 생성합니다."
            status.update(label="2026 Investment Recap이 준비됐어요", state="complete", expanded=False)
        package["source_name"] = f"virtual_customer_{customer_id}_2026"
        st.session_state["analysis_package"] = package
        st.session_state["journey"] = journey
        st.session_state["flow_stage"] = "recap"
        st.rerun()
    except ValueError as error:
        st.error(str(error))
    except Exception as error:
        st.error(f"투자 활동 분석 중 오류가 발생했습니다: {error}")


def upload_view() -> None:
    app_wordmark("mPOP")
    progress_bar(0)
    st.markdown(
        """
        <section class="upload-hero">
          <div class="year-label">2026 MY INVESTMENT RECAP</div>
          <div class="upload-orbit"><span>✦</span><b>AI</b><i>⌁</i></div>
          <h1>한 해의 투자 기록을<br><strong>나만의 이야기</strong>로</h1>
          <p>가상 고객을 선택하면 연간 거래·관심·콘텐츠 기록에서<br>AI가 투자 행동을 읽고 Recap을 만들어요.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-heading">분석할 고객을 선택해주세요</div>', unsafe_allow_html=True)
    customers = [
        {"id": "C001", "name": "김준호", "type": "테마 집중형", "icon": "🚀", "summary": "AI·반도체 관심과 급락기 분할매수", "tone": "blue"},
        {"id": "C002", "name": "이서연", "type": "장기 루틴형", "icon": "🌿", "summary": "글로벌 ETF·채권 중심의 꾸준한 루틴", "tone": "green"},
        {"id": "C003", "name": "박민수", "type": "민감 반응형", "icon": "⚡", "summary": "뉴스와 시장 변동에 빠르게 반응", "tone": "orange"},
    ]
    for customer in customers:
        st.markdown(
            f"""
            <article class="customer-card {customer['tone']}">
              <div class="customer-avatar">{safe(customer['icon'])}</div>
              <div><span>{safe(customer['type'])}</span><h3>{safe(customer['name'])}</h3><p>{safe(customer['summary'])}</p></div>
              <i>›</i>
            </article>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"{customer['name']} 고객 분석하기", key=f"analyze_{customer['id']}", use_container_width=True):
            run_customer_analysis(customer["id"], customer["name"])
    st.markdown(
        '<div class="privacy-note"><b>가상 고객 데이터</b><span>세 고객의 거래·관심·콘텐츠 기록은 모두 데모용으로 Streamlit 클라우드 DB에 저장되어 있습니다.</span></div>',
        unsafe_allow_html=True,
    )


def recap_hero(journey: dict[str, Any]) -> None:
    st.markdown(
        f"""
        <section class="recap-hero">
          <div class="year-label">2026 MY INVESTMENT RECAP</div>
          <div class="recap-trophy"><i>✦</i><b>AI</b><span>↗</span></div>
          <h1>{safe(journey['recap_title'])}</h1>
          <p>{safe(journey['recap_subtitle'])}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def metric_strip(metrics: dict[str, Any]) -> None:
    st.markdown(
        f"""
        <div class="metric-strip">
          <div><b>{metrics['active_days']}</b><span>투자 활동일</span></div>
          <div><b>{metrics['avg_holding_days']:.0f}일</b><span>평균 보유</span></div>
          <div><b>{metrics['top_theme_share']:.0f}%</b><span>상위 테마</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def story_card(slide: dict[str, Any], index: int) -> None:
    icon = SLIDE_ICONS.get(slide["icon"], "✦")
    st.markdown(
        f"""
        <article class="story-card story-{index}">
          <div class="story-number">{index}</div>
          <div class="story-icon">{safe(icon)}</div>
          <div class="story-kicker">{safe(slide['kicker'])}</div>
          <h2>{safe(slide['headline'])}</h2>
          <p>{safe(slide['body'])}</p>
          <div class="story-evidence">{safe(slide['evidence'])}</div>
        </article>
        """,
        unsafe_allow_html=True,
    )


def choose_goal(goal: dict[str, Any]) -> None:
    package = st.session_state["analysis_package"]
    journey = st.session_state["journey"]
    customer, metrics = package["customer"], package["metrics"]
    api_key = get_api_key(secrets=st.secrets)
    model = get_model(st.secrets)
    with st.spinner("선택한 AI 추천 목표에 맞는 리포트와 뉴스를 my PICK에 연결하고 있어요..."):
        if api_key:
            try:
                plan = generate_mypick_plan(customer, metrics, journey, goal, api_key, model)
            except Exception as error:
                plan = fallback_mypick(customer, metrics, journey, goal)
                st.session_state["flow_notice"] = f"my PICK AI 호출이 완료되지 않아 데모 구성을 사용했습니다: {error}"
        else:
            plan = fallback_mypick(customer, metrics, journey, goal)
    st.session_state["selected_goal"] = goal
    st.session_state["mypick_plan"] = plan
    save_journey_memory(customer, journey, goal, plan)
    st.session_state["flow_stage"] = "ready"
    st.rerun()


def goal_cards(journey: dict[str, Any]) -> None:
    st.markdown(
        """
        <section class="goal-intro">
          <span>AI NEXT GOAL</span>
          <h2>2027년 my PICK에서 무엇을 더 보고 싶나요?</h2>
          <p>올해의 Recap을 바탕으로 만든 AI 추천 목표 3개예요.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    for index, goal in enumerate(journey["goals"], start=1):
        icon = GOAL_ICONS.get(goal["icon"], "⌖")
        st.markdown(
            f"""
            <article class="goal-card">
              <div class="goal-icon">{safe(icon)}</div>
              <div><span>AI 추천 목표 {index}</span><h3>{safe(goal['title'])}</h3><p>{safe(goal['reason'])}</p></div>
            </article>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"‘{goal['title']}’ 선택", key=f"choose_{goal['goal_id']}", use_container_width=True):
            choose_goal(goal)


def recap_view(show_dialog: bool = False) -> None:
    package = st.session_state["analysis_package"]
    journey = st.session_state["journey"]
    app_wordmark("mPOP")
    progress_bar(3 if show_dialog else 1)
    recap_hero(journey)
    metric_strip(package["metrics"])
    notice = st.session_state.get("flow_notice")
    if notice:
        st.info(notice)
    st.markdown('<div class="section-heading">AI가 발견한 나의 투자 이야기</div>', unsafe_allow_html=True)
    for index, slide in enumerate(journey["slides"], start=1):
        story_card(slide, index)
    goal_cards(journey)
    with st.expander("분석 근거 확인"):
        st.json(package["metrics"], expanded=False)
        st.caption(f"데이터: {package['source_name']} · 전체 {package['row_count']}개 활동 · 제외 {package['skipped_count']}개")
    if st.button("다른 고객 분석하기", use_container_width=True):
        reset_flow()
    if show_dialog:
        mypick_ready_dialog()


@st.dialog("Stay With Me", width="small")
def mypick_ready_dialog() -> None:
    plan = st.session_state["mypick_plan"]
    goal = st.session_state["selected_goal"]
    st.markdown(
        f"""
        <div class="modal-art"><span>★</span><i>↗</i></div>
        <div class="modal-eyebrow">RECAP에서 my PICK으로</div>
        <h2 class="modal-title">{safe(plan['popup_title'])}</h2>
        <p class="modal-body">업데이트된 my PICK을 확인하고 내년에도 열심히 투자해봐요</p>
        <div class="modal-goal">2027 AI 추천 목표 · {safe(goal['title'])}</div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("새로운 my PICK 보러가기", type="primary", use_container_width=True, key="open_mypick"):
        st.session_state["flow_stage"] = "mypick"
        st.rerun()
    if st.button("Recap 더 보기", use_container_width=True, key="close_mypick"):
        st.session_state["flow_stage"] = "recap"
        st.rerun()


def mypick_header(customer: dict[str, Any], goal: dict[str, Any]) -> None:
    st.markdown(
        f"""
        <section class="mypick-shell">
          <div class="mypick-top">‹ &nbsp;<b>my PICK</b><span>✦ AI UPDATE</span></div>
          <div class="mypick-date">2027년 1월 1일 <i>▥</i></div>
          <h1>{safe(customer['name'])}님의 투자 이야기</h1>
          <div class="remember-chip">다가오는 해의 목표 · {safe(goal['title'])}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def mypick_view() -> None:
    package = st.session_state["analysis_package"]
    customer, metrics = package["customer"], package["metrics"]
    goal, plan = st.session_state["selected_goal"], st.session_state["mypick_plan"]
    progress_bar(3)
    mypick_header(customer, goal)
    st.markdown('<div class="mypick-section-title">내가 살펴본 종목</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <article class="watch-card">
          <div class="stock-logo">{safe(plan['watch_symbol'][:2])}</div>
          <div class="stock-copy"><b>{safe(plan['watch_title'])}</b><span>{safe(plan['watch_symbol'])}</span><p>{safe(plan['watch_reason'])}</p></div>
          <div class="stock-tag">올해의 관심</div>
        </article>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="mypick-section-title">오늘의 시황 요약</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <article class="market-card">
          <div class="market-icon">☾</div>
          <div><h3>{safe(plan['market_title'])}</h3><p>{safe(plan['market_body'])}</p><span>내 관심 기반 요약 ›</span></div>
        </article>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="mypick-section-title">관심있을 만한 소식</div>', unsafe_allow_html=True)
    for card in plan["content_cards"]:
        icon = CONTENT_ICONS.get(card["icon"], "▤")
        st.markdown(
            f"""
            <article class="content-card">
              <div class="content-icon">{safe(icon)}</div>
              <div><span>#{safe(card['category'])}</span><h3>{safe(card['title'])}</h3><p>{safe(card['description'])}</p><b>{safe(card['cta'])} ›</b></div>
            </article>
            """,
            unsafe_allow_html=True,
        )
    st.markdown(
        f"""
        <article class="routine-card">
          <div>↻</div><span>PERSONALIZED FEED</span><h3>{safe(plan['update_title'])}</h3>
          <p>{safe(plan['update_body'])}</p><small>{safe(plan['update_frequency'])}</small>
        </article>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="compliance-note">이 페이지는 연말 Recap과 고객이 선택한 AI 추천 목표에 맞춰 새롭게 구성된 my PICK 페이지입니다.</div>',
        unsafe_allow_html=True,
    )
    with st.expander("저장된 AI Memory 확인"):
        st.json(load_memories().get("customers", {}).get(customer["customer_id"], {}), expanded=False)
    cols = st.columns(2)
    with cols[0]:
        if st.button("Recap 다시 보기", use_container_width=True):
            st.session_state["flow_stage"] = "recap"
            st.rerun()
    with cols[1]:
        if st.button("새 고객 선택", type="primary", use_container_width=True):
            reset_flow()
    bottom_navigation()


def bottom_navigation() -> None:
    st.markdown(
        """
        <div class="ticker"><b>KOSPI</b><span>2,842.17</span><em>장종료</em></div>
        <div class="bottom-nav"><b>⌂<small>홈</small></b><span>☆<small>관심종목</small></span><span>⌁<small>종합차트</small></span><span>☰<small>메뉴</small></span></div>
        """,
        unsafe_allow_html=True,
    )


initialize_state()
stage = st.session_state["flow_stage"]
if stage == "upload":
    upload_view()
elif stage == "recap":
    recap_view()
elif stage == "ready":
    recap_view(show_dialog=True)
elif stage == "mypick":
    mypick_view()
else:
    reset_flow()
