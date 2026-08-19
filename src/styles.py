CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

:root {
  --navy:#142b64; --deep:#0c1e4a; --blue:#176ee8; --sky:#dff5ff;
  --ink:#101828; --muted:#667085; --line:#e6ebf2; --paper:#fff;
}
html, body, [class*="css"], [data-testid="stAppViewContainer"] {
  font-family:'Noto Sans KR',-apple-system,BlinkMacSystemFont,sans-serif;
}
[data-testid="stAppViewContainer"] { background:#eef3f9; }
[data-testid="stHeader"], [data-testid="stToolbar"] { background:transparent; }
#MainMenu, footer, .stAppDeployButton { display:none!important; }
.block-container { max-width:580px; padding:18px 18px 120px; }

.app-wordmark { display:flex; align-items:center; justify-content:space-between; color:#526070; font-size:13px; margin:2px 2px 16px; }
.app-wordmark b { color:#17316d; font-size:15px; }.app-wordmark em { color:#1989ee; font-style:normal; }
.flow-progress { display:grid; grid-template-columns:repeat(4,1fr); gap:5px; background:#fff; border:1px solid var(--line); border-radius:16px; padding:8px; margin-bottom:14px; box-shadow:0 6px 20px rgba(31,48,82,.05); }
.flow-step { display:flex; flex-direction:column; align-items:center; gap:4px; color:#a4acb9; font-size:10px; white-space:nowrap; }
.flow-step i { width:22px; height:22px; border-radius:50%; display:flex; align-items:center; justify-content:center; background:#eef1f5; font-style:normal; font-weight:800; }
.flow-step.done, .flow-step.active { color:#176ee8; font-weight:800; }.flow-step.done i { background:#dff2ff; }.flow-step.active i { color:#fff; background:#176ee8; box-shadow:0 4px 12px rgba(23,110,232,.3); }

.upload-hero, .recap-hero { position:relative; overflow:hidden; text-align:center; border-radius:30px; padding:34px 24px; box-shadow:0 22px 60px rgba(47,89,140,.13); }
.upload-hero { background:radial-gradient(circle at 85% 18%,#fff 0,#e9f8ff 32%,#d6f1ff 65%,#eaf9ff 100%); }
.upload-hero:before { content:''; position:absolute; width:180px; height:180px; border:1px solid rgba(37,138,225,.16); border-radius:50%; left:-95px; top:-80px; }
.year-label { color:#377ebc; font-size:11px; letter-spacing:.1em; font-weight:800; }
.upload-hero h1, .recap-hero h1 { color:#132b67; font-size:34px; line-height:1.25; letter-spacing:-.055em; margin:18px 0 12px; }
.upload-hero h1 strong { color:#1777e5; }.upload-hero p, .recap-hero p { color:#60708b; font-size:14px; line-height:1.65; margin:0; }
.upload-orbit { width:96px; height:96px; margin:24px auto 6px; border-radius:28px; background:linear-gradient(145deg,#1f75eb,#735ee9); color:#fff; display:flex; align-items:center; justify-content:center; position:relative; box-shadow:0 18px 30px rgba(43,91,218,.25); transform:rotate(-4deg); }
.upload-orbit b { font-size:27px; }.upload-orbit span,.upload-orbit i { position:absolute; font-style:normal; color:#7ddcff; font-size:21px; }.upload-orbit span { left:-20px; top:7px; }.upload-orbit i { right:-24px; bottom:6px; }
.section-heading { color:#142b64; font-size:20px; font-weight:800; letter-spacing:-.035em; margin:27px 2px 13px; }
.customer-card { --accent:#176ee8; --soft:#e6f2ff; display:grid; grid-template-columns:52px 1fr auto; gap:14px; align-items:center; background:#fff; border:1px solid #e7edf5; border-radius:20px; padding:17px; margin:12px 0 7px; box-shadow:0 8px 24px rgba(31,48,82,.06); }
.customer-card.green { --accent:#078f71; --soft:#e3f7f0; }.customer-card.orange { --accent:#dd713f; --soft:#fff0e7; }
.customer-avatar { width:52px; height:52px; border-radius:17px; background:var(--soft); display:flex; align-items:center; justify-content:center; font-size:25px; }
.customer-card span { color:var(--accent); font-size:10px; font-weight:800; }.customer-card h3 { color:#18233a; font-size:19px; margin:2px 0 3px; }.customer-card p { color:#758195; font-size:11px; margin:0; }.customer-card i { color:var(--accent); font-size:25px; font-style:normal; }

[data-testid="stFileUploader"] { background:#fff; border:1px dashed #9fc7eb; border-radius:20px; padding:8px; }
[data-testid="stFileUploaderDropzone"] { background:#f7fbff; border:0; border-radius:15px; }
[data-testid="stTextInput"] input, [data-testid="stSelectbox"] div[data-baseweb="select"] > div { border-radius:13px; border-color:#dce3ed; background:#fff; }
.stButton > button, .stDownloadButton > button { min-height:47px; border-radius:14px; border:1px solid #dce4ef; font-weight:800; }
.stButton > button[kind="primary"] { color:#fff; border:0; background:linear-gradient(90deg,#176ee8,#1398ed); box-shadow:0 9px 22px rgba(23,110,232,.24); }
.or-divider { display:flex; align-items:center; gap:12px; color:#98a2b3; font-size:11px; margin:22px 0 12px; }.or-divider:before,.or-divider:after { content:''; height:1px; background:#dce3ec; flex:1; }
.privacy-note { display:flex; gap:10px; background:#edf8ff; border-radius:16px; padding:14px; margin:18px 0 12px; color:#526070; font-size:11px; line-height:1.55; }.privacy-note b { color:#1769bd; white-space:nowrap; }.privacy-note span { display:block; }
[data-testid="stExpander"] { background:#fff; border:1px solid var(--line); border-radius:16px; overflow:hidden; }

.recap-hero { background:linear-gradient(155deg,#def6ff,#f5fbff 55%,#e2efff); padding-bottom:28px; }
.recap-trophy { width:112px; height:90px; border-radius:45% 45% 38% 38%; background:linear-gradient(145deg,#274be4,#7156e5); margin:23px auto 12px; box-shadow:0 18px 34px rgba(43,72,208,.23); display:flex; align-items:center; justify-content:center; color:white; position:relative; }
.recap-trophy b { font-size:28px; }.recap-trophy i,.recap-trophy span { position:absolute; font-style:normal; color:#70d8ff; font-size:20px; }.recap-trophy i { left:-12px; top:3px; }.recap-trophy span { right:-16px; top:5px; }
.recap-hero h1 { font-size:30px; margin-top:12px; }
.metric-strip { display:grid; grid-template-columns:repeat(3,1fr); background:#fff; border-radius:20px; margin:-7px 14px 18px; position:relative; z-index:2; box-shadow:0 12px 30px rgba(31,48,82,.1); }
.metric-strip div { padding:15px 6px; text-align:center; border-right:1px solid #edf0f4; }.metric-strip div:last-child { border:0; }.metric-strip b { display:block; color:#176ee8; font-size:20px; }.metric-strip span { color:#7c8798; font-size:10px; }

.story-card { position:relative; overflow:hidden; background:#fff; border-radius:24px; padding:25px 24px; margin:12px 0; min-height:190px; box-shadow:0 10px 30px rgba(31,48,82,.07); }
.story-card:after { content:''; position:absolute; width:150px; height:150px; border-radius:50%; right:-62px; bottom:-75px; background:var(--soft); }
.story-1 { --accent:#3d70dd; --soft:#e5efff; }.story-2 { --accent:#7355d9; --soft:#eee8ff; }.story-3 { --accent:#ed7c41; --soft:#fff0e7; }.story-4 { --accent:#087f9f; --soft:#dff7fa; }.story-5 { --accent:#087b62; --soft:#def7ef; }
.story-number { position:absolute; top:20px; right:20px; font-size:38px; font-weight:800; color:var(--soft); }.story-icon { width:42px; height:42px; border-radius:14px; background:var(--soft); color:var(--accent); display:flex; align-items:center; justify-content:center; font-weight:900; margin-bottom:17px; }
.story-kicker { color:var(--accent); font-size:11px; font-weight:800; letter-spacing:.05em; }.story-card h2 { color:#17223a; font-size:23px; line-height:1.35; letter-spacing:-.045em; margin:7px 40px 9px 0; }.story-card p { color:#626f82; font-size:13px; line-height:1.7; margin:0 26px 15px 0; position:relative; z-index:2; }.story-evidence { display:inline-flex; background:#f4f6f9; color:#536071; border-radius:9px; padding:7px 9px; font-size:10px; font-weight:700; position:relative; z-index:2; }

.goal-intro { text-align:center; padding:34px 14px 14px; }.goal-intro span { color:#1673df; font-size:11px; font-weight:800; letter-spacing:.12em; }.goal-intro h2 { color:#142b64; font-size:26px; line-height:1.35; letter-spacing:-.05em; margin:9px 0; }.goal-intro p { color:#788599; font-size:12px; line-height:1.6; }
.goal-card { display:flex; gap:15px; background:#fff; border-radius:20px; padding:18px; margin-top:11px; border:1px solid #e8edf4; box-shadow:0 8px 22px rgba(31,48,82,.05); }.goal-icon { flex:0 0 44px; height:44px; border-radius:14px; background:#e6f2ff; color:#176ee8; display:flex; align-items:center; justify-content:center; font-size:20px; font-weight:800; }.goal-card span { color:#2f79c6; font-size:10px; font-weight:800; }.goal-card h3 { color:#18233a; margin:3px 0 5px; font-size:18px; letter-spacing:-.035em; }.goal-card p { color:#697588; font-size:12px; line-height:1.55; margin:0; }

[data-testid="stDialog"] > div { border-radius:28px; }
.modal-art { width:90px; height:75px; margin:3px auto 18px; background:linear-gradient(145deg,#e0f5ff,#eef0ff); border-radius:26px; display:flex; align-items:center; justify-content:center; position:relative; color:#2778dc; font-size:38px; }.modal-art i { position:absolute; right:8px; top:3px; font-style:normal; color:#7e62e7; font-size:24px; }.modal-eyebrow { text-align:center; color:#2c79c7; font-size:10px; font-weight:800; letter-spacing:.08em; }.modal-title { text-align:center; color:#15295c; font-size:24px; line-height:1.35; letter-spacing:-.045em; }.modal-body { text-align:center; color:#68758a; font-size:13px; line-height:1.65; }.modal-goal { background:#eff7ff; color:#2369b3; border-radius:12px; text-align:center; padding:11px; font-size:11px; font-weight:800; margin:14px 0 18px; }

.mypick-shell { background:linear-gradient(150deg,#193772,#10295f 55%,#0b1d49); color:#fff; padding:28px 24px 30px; border-radius:0 0 30px 30px; margin:-18px -18px 0; box-shadow:0 18px 50px rgba(9,29,72,.2); }.mypick-top { display:flex; justify-content:space-between; align-items:center; font-size:18px; }.mypick-top span { background:rgba(255,255,255,.12); border-radius:999px; padding:6px 9px; font-size:9px; color:#6de1ff; }.mypick-date { color:#78d4f5; font-size:12px; margin-top:35px; }.mypick-date i { font-style:normal; }.mypick-shell h1 { font-size:28px; letter-spacing:-.05em; margin:8px 0 16px; }.remember-chip { display:inline-flex; background:rgba(255,255,255,.1); color:#d7e5ff; border-radius:10px; padding:9px 11px; font-size:10px; }
.mypick-section-title { color:#fff; background:#142b64; font-size:21px; font-weight:800; letter-spacing:-.04em; margin:0 -18px; padding:28px 22px 13px; }.watch-card,.market-card,.content-card { background:#fff; border-radius:20px; margin:0 -3px 12px; padding:18px; box-shadow:0 8px 24px rgba(31,48,82,.07); }.watch-card { display:grid; grid-template-columns:50px 1fr auto; gap:13px; align-items:start; }.stock-logo { width:50px; height:50px; background:#e6f2ff; color:#1673df; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:900; }.stock-copy b { display:block; color:#17223a; font-size:17px; }.stock-copy span { color:#98a2b3; font-size:11px; }.stock-copy p { color:#68758a; font-size:11px; line-height:1.55; margin:8px 0 0; }.stock-tag { color:#1673df; background:#e9f4ff; border-radius:9px; padding:6px 7px; font-size:9px; font-weight:800; }
.market-card { display:flex; gap:14px; background:#fffdf3; }.market-icon { width:48px; height:48px; border-radius:15px; background:#fff3c7; display:flex; align-items:center; justify-content:center; font-size:24px; }.market-card h3,.content-card h3 { color:#18233a; font-size:17px; line-height:1.4; margin:0 0 7px; }.market-card p,.content-card p { color:#727e90; font-size:11px; line-height:1.55; margin:0 0 10px; }.market-card span,.content-card b { color:#196fd2; font-size:10px; }
.content-card { display:flex; gap:14px; }.content-icon { width:46px; height:46px; flex:0 0 46px; border-radius:14px; background:#e8f4ff; color:#1673df; display:flex; align-items:center; justify-content:center; font-size:20px; font-weight:900; }.content-card span { color:#e16450; font-size:10px; font-weight:800; }.content-card h3 { margin-top:3px; }
.routine-card { background:linear-gradient(145deg,#e1f8f2,#effcf8); border-radius:22px; padding:22px; margin:18px 0; }.routine-card > div { float:right; font-size:28px; color:#0b9477; }.routine-card span { color:#0a9074; font-size:10px; font-weight:800; letter-spacing:.08em; }.routine-card h3 { color:#153c36; font-size:20px; margin:7px 30px 6px 0; }.routine-card p { color:#58726d; font-size:12px; line-height:1.55; }.routine-card small { color:#0a9074; font-weight:800; }.compliance-note { color:#7c8798; font-size:10px; line-height:1.55; padding:8px 10px 18px; }

.ticker { position:fixed; left:0; right:0; bottom:60px; height:34px; z-index:998; background:#fff; border-top:1px solid #e4e8ed; display:flex; align-items:center; justify-content:center; gap:18px; font-size:11px; }.ticker span { color:#2282df; font-weight:800; }.ticker em { color:#98a2b3; font-style:normal; }.bottom-nav { position:fixed; left:0; right:0; bottom:0; height:60px; z-index:999; background:#151d2c; display:flex; justify-content:center; align-items:center; gap:48px; color:#8d98aa; }.bottom-nav b,.bottom-nav span { display:flex; flex-direction:column; align-items:center; font-size:17px; }.bottom-nav b { color:#fff; }.bottom-nav small { font-size:9px; margin-top:2px; }

@media (max-width:600px) {
  .block-container { padding:12px 12px 120px; }
  .upload-hero,.recap-hero { border-radius:25px; padding-left:17px; padding-right:17px; }
  .upload-hero h1 { font-size:30px; }.recap-hero h1 { font-size:27px; }
  .mypick-shell { margin:-12px -12px 0; }.mypick-section-title { margin-left:-12px; margin-right:-12px; }
  .story-card h2 { font-size:21px; }.goal-intro h2 { font-size:23px; }
  .bottom-nav { gap:34px; }
}
</style>
"""
