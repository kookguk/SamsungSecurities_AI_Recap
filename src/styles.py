CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

:root {
  --navy: #142b64;
  --navy-deep: #0b1d49;
  --blue: #2f80ed;
  --sky: #55c9ef;
  --ink: #101828;
  --muted: #667085;
  --line: #e6eaf0;
  --paper: #ffffff;
}

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
  font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
}

[data-testid="stAppViewContainer"] {
  background: #eef2f8;
}

[data-testid="stHeader"], [data-testid="stToolbar"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.stAppDeployButton { display:none; }

.block-container {
  max-width: 1180px;
  padding-top: 1.4rem;
  padding-bottom: 8rem;
}

.mpop-shell {
  background: linear-gradient(155deg, #172f69 0%, #102557 55%, #0b1c43 100%);
  color: white;
  border-radius: 30px;
  padding: 28px 30px 34px;
  box-shadow: 0 24px 70px rgba(11, 29, 73, .20);
  margin-bottom: 18px;
  overflow: hidden;
  position: relative;
}
.mpop-shell:after {
  content: ''; position:absolute; width:360px; height:360px; border-radius:50%;
  right:-180px; top:-180px; background:rgba(73,154,255,.12); pointer-events:none;
}
.mpop-top { display:flex; justify-content:space-between; align-items:center; font-size:14px; opacity:.9; margin-bottom:36px; }
.mpop-brand { font-size:22px; font-weight:600; letter-spacing:-.02em; }
.mpop-brand b { font-weight:800; }
.live-pill { display:inline-flex; gap:8px; align-items:center; background:rgba(255,255,255,.12); padding:8px 12px; border-radius:999px; font-size:12px; }
.live-dot { width:7px; height:7px; border-radius:50%; background:#52dfa5; box-shadow:0 0 0 5px rgba(82,223,165,.13); }
.hero-kicker { color:#79d9fa; font-size:15px; font-weight:700; margin-bottom:10px; }
.hero-title { font-size:44px; line-height:1.18; letter-spacing:-.055em; font-weight:800; margin:0 0 13px; max-width:700px; }
.hero-copy { color:#cad5ed; font-size:16px; line-height:1.7; max-width:680px; margin:0; }
.hero-year { color:#8fa7d6; font-weight:700; margin-right:7px; }

.section-title { font-size:24px; font-weight:800; letter-spacing:-.04em; color:#15203b; margin:30px 0 8px; }
.section-sub { color:#667085; font-size:14px; margin-bottom:18px; }
.micro-label { color:#7890bb; font-size:12px; font-weight:700; letter-spacing:.02em; }

.recap-card, .metric-card, .white-card {
  background:#fff; border:1px solid rgba(16,24,40,.06); border-radius:24px;
  box-shadow:0 10px 34px rgba(31,48,82,.07);
}
.recap-card { padding:26px; margin:10px 0; }
.pattern-chip { display:inline-flex; padding:8px 12px; border-radius:999px; background:#eaf7ff; color:#1974bc; font-size:12px; font-weight:800; }
.pattern-title { color:#101828; font-size:28px; line-height:1.28; letter-spacing:-.045em; font-weight:800; margin:18px 0 10px; }
.pattern-story { color:#475467; font-size:15px; line-height:1.75; margin:0 0 20px; }
.evidence-row { display:flex; flex-wrap:wrap; gap:8px; }
.evidence { background:#f4f6fa; color:#46546c; border-radius:10px; padding:8px 10px; font-size:12px; font-weight:600; }

.metric-grid { display:grid; grid-template-columns:repeat(4, 1fr); gap:12px; margin:16px 0 4px; }
.metric-card { padding:18px 17px; }
.metric-icon { font-size:19px; margin-bottom:15px; }
.metric-value { color:#142b64; font-weight:800; font-size:23px; letter-spacing:-.03em; }
.metric-label { color:#667085; font-size:12px; margin-top:4px; }

.split-note { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:14px; }
.note { border-radius:18px; padding:17px; min-height:118px; }
.note.good { background:#effaf6; }.note.watch { background:#fff7e8; }
.note-label { font-size:12px; font-weight:800; color:#526070; margin-bottom:8px; }
.note-text { color:#344054; font-size:14px; line-height:1.6; }

.crm-card { border-radius:24px; padding:25px; min-height:214px; box-shadow:0 12px 34px rgba(31,48,82,.08); position:relative; overflow:hidden; }
.crm-card.mint { background:linear-gradient(145deg,#daf7f1,#eefcf8); }
.crm-card.lavender { background:linear-gradient(145deg,#e8e5ff,#f5f3ff); }
.crm-card.peach { background:linear-gradient(145deg,#fff0df,#fff8ee); }
.crm-eyebrow { color:#526070; font-size:12px; font-weight:800; }
.crm-title { color:#101828; font-size:22px; line-height:1.35; font-weight:800; letter-spacing:-.04em; margin:14px 56px 9px 0; }
.crm-body { color:#536071; font-size:13px; line-height:1.65; margin-right:12px; }
.crm-icon { position:absolute; right:22px; top:22px; font-size:36px; }
.crm-cta { display:inline-block; margin-top:18px; color:#1459c4; font-size:13px; font-weight:800; }

.compare-card { background:#fff; border-radius:24px; padding:22px; min-height:510px; border-top:6px solid var(--accent); box-shadow:0 10px 34px rgba(31,48,82,.07); }
.compare-avatar { width:46px; height:46px; border-radius:16px; display:flex; align-items:center; justify-content:center; font-size:23px; background:var(--soft); }
.compare-name { font-size:22px; font-weight:800; color:#101828; margin-top:15px; }
.compare-type { font-size:13px; color:var(--accent); font-weight:800; margin:4px 0 18px; }
.compare-headline { font-size:18px; line-height:1.4; font-weight:800; color:#1d2939; margin:18px 0 8px; }
.compare-story { font-size:13px; line-height:1.65; color:#667085; min-height:108px; }
.compare-metrics { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin:16px 0; }
.compare-metric { background:#f5f7fa; border-radius:12px; padding:11px; }
.compare-metric b { display:block; color:#1d2939; font-size:16px; }.compare-metric span { color:#7b8799; font-size:10px; }
.goal-badge { display:block; border-radius:12px; background:var(--soft); color:#344054; padding:11px; font-size:12px; font-weight:700; }

.memory-box { background:#0d1b38; color:#cce5ff; border-radius:20px; padding:20px; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:12px; white-space:pre-wrap; overflow:auto; }
.data-note { background:#fff; border-left:4px solid #65c9ef; border-radius:14px; padding:14px 16px; color:#526070; font-size:12px; line-height:1.6; margin-top:14px; }

[data-testid="stRadio"] > label { display:none; }
[data-testid="stRadio"] [role="radiogroup"] { gap:8px; background:#dfe5ef; padding:5px; border-radius:14px; }
[data-testid="stRadio"] [role="radio"] { background:transparent; border-radius:10px; padding:7px 13px; }
[data-testid="stRadio"] [aria-checked="true"] { background:#fff; box-shadow:0 3px 10px rgba(31,48,82,.10); }
[data-testid="stRadio"] [role="radio"] > div:first-child { display:none; }
[data-testid="stSelectbox"] { max-width:300px; margin:0 0 4px auto; }

.stButton > button { border-radius:14px; min-height:46px; border:0; font-weight:800; }
.stButton > button[kind="primary"] { background:#1966d5; color:#fff; box-shadow:0 8px 18px rgba(25,102,213,.22); }
[data-testid="stExpander"] { background:#fff; border-radius:16px; border:1px solid #e6eaf0; overflow:hidden; }

.ticker { position:fixed; bottom:64px; left:0; right:0; z-index:999; height:36px; background:#f9fafb; border-top:1px solid #e5e7eb; display:flex; align-items:center; justify-content:center; gap:20px; font-size:12px; }
.ticker b { color:#15203b; }.ticker .down { color:#2788e6; font-weight:800; }.ticker .closed { color:#98a2b3; }
.bottom-nav { position:fixed; bottom:0; left:0; right:0; z-index:999; height:64px; background:#151c2b; display:flex; align-items:center; justify-content:center; gap:46px; color:#8f9bb0; font-size:12px; }
.bottom-nav span:first-child { color:#fff; font-weight:800; }

@media (max-width: 760px) {
  .block-container { padding:0 0 8rem; }
  .mpop-shell { border-radius:0 0 28px 28px; padding:22px 20px 28px; }
  .mpop-top { margin-bottom:26px; }.mpop-brand { font-size:18px; }
  .hero-title { font-size:34px; }.hero-copy { font-size:14px; }
  .metric-grid { grid-template-columns:1fr 1fr; }
  .split-note { grid-template-columns:1fr; }
  .section-title, .section-sub, .recap-card, .metric-grid, .data-note { margin-left:16px; margin-right:16px; }
  [data-testid="stSelectbox"] { max-width:none; margin:0 16px 4px; }
  .recap-card { padding:21px; }.pattern-title { font-size:24px; }
  .bottom-nav { gap:24px; }.ticker { gap:10px; }
}
</style>
"""
