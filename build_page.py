from pathlib import Path
import json,csv
root=Path(__file__).parent
geo=json.loads((root/'data'/'geo.json').read_text(encoding='utf-8'))
enr=json.loads((root/'data'/'enriched.json').read_text(encoding='utf-8'))
html=r'''<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#03050B"><meta name="description" content="خريطة تفاعلية لأحياء مدينة الرياض. حدود الأحياء، الجهات، الطرق الرئيسية، ومؤشرات تسويقية لكل حي من مصادر رسمية ومفتوحة.">
<title>خريطة أحياء الرياض | PLAN C Urban Intelligence</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=Chakra+Petch:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#03050b;--panel:#090d17;--panel2:#0c1120;--stroke:rgba(180,193,220,.13);--muted:#8c97b0;--text:#f5f5f2;--orange:#fe5000;--blue:#6cace4;--navy:#001e60;--cream:#e5e3da;--good:#94c2ab;--warning:#e5b57e;--font:'IBM Plex Sans Arabic','Noto Sans Arabic',Tahoma,sans-serif;--mono:'IBM Plex Mono',monospace;--display:'Chakra Petch',sans-serif}
*{box-sizing:border-box}html,body{margin:0;min-height:100%;background:var(--bg);color:var(--text);font-family:var(--font)}button,input{font:inherit}button{cursor:pointer}button:focus-visible,input:focus-visible{outline:2px solid var(--orange);outline-offset:3px}a{color:inherit}.app{min-height:100dvh;display:flex;flex-direction:column;overflow:hidden;background:radial-gradient(90% 70% at 64% 110%,rgba(0,30,96,.19),transparent 74%),#03050b}
.topbar{height:76px;display:flex;align-items:center;justify-content:space-between;padding:0 30px;border-bottom:1px solid var(--stroke);background:rgba(3,5,11,.94);z-index:20;gap:16px}.brand{display:flex;align-items:center;gap:14px;white-space:nowrap}.logo-icon{height:40px;width:40px;display:block;flex:none}.logo-icon svg{display:block;width:100%;height:100%}.brandword{font:700 21px var(--display);letter-spacing:.05em;line-height:1.08;direction:ltr}.brandword span{color:var(--orange)}.brand small{display:block;color:var(--muted);font:500 9px var(--mono);letter-spacing:.15em;margin-top:6px;direction:ltr}.topcenter{display:flex;align-items:center;gap:13px;color:var(--muted);font:500 11px var(--mono);direction:ltr}.live-dot{width:8px;height:8px;background:var(--orange);box-shadow:0 0 15px rgba(254,80,0,.75);border-radius:100%}.topaction{border:1px solid var(--stroke);background:#111621;color:#ddd;padding:10px 14px;display:flex;align-items:center;gap:8px;font-size:12px}.topaction:hover,.ghost:hover{border-color:rgba(254,80,0,.6)}
.workspace{display:grid;grid-template-columns:330px minmax(0,1fr);flex:1;min-height:0;height:calc(100dvh - 76px)}.sidebar{border-left:1px solid var(--stroke);padding:28px 24px 20px;display:flex;flex-direction:column;overflow:auto;background:linear-gradient(145deg,#0b101b,#06090f 70%)}.eyebrow{color:var(--orange);font:600 10px var(--mono);letter-spacing:.17em;direction:ltr;text-align:right}.sidebar h1{font-weight:600;font-size:clamp(28px,2.7vw,40px);letter-spacing:-.055em;line-height:1.22;margin:12px 0}.sidebar h1 b{color:var(--orange);font-weight:600}.sub{font-size:12px;color:#aab3c2;line-height:1.9;margin:2px 0 22px}.searchbox{position:relative;margin-top:2px}.searchbox input{width:100%;background:#111726;border:1px solid #263048;border-radius:0;color:#fff;padding:15px 42px 15px 12px;outline:0;font-size:13px}.searchbox input::placeholder{color:#6f7f94}.searchbox input:focus{border-color:var(--orange)}.searchglyph{position:absolute;right:16px;top:14px;color:#8694ae;font-size:18px;pointer-events:none}.search-results{position:absolute;left:0;right:0;top:calc(100% + 4px);max-height:258px;overflow:auto;background:#121a2b;border:1px solid #34425b;z-index:30;box-shadow:0 20px 30px rgba(0,0,0,.4)}.suggestion{width:100%;display:flex;justify-content:space-between;align-items:center;background:none;border:0;border-bottom:1px solid #20293a;color:#f4f5f5;text-align:right;padding:10px 14px;font-size:13px}.suggestion:hover{background:#202b41}.suggestion small{color:#8d9aaa;direction:ltr}.section-label{display:flex;justify-content:space-between;align-items:center;margin:26px 0 10px;font-size:11px;color:#a3adbd}.section-label span:last-child{font:500 10px var(--mono);color:#738197;direction:ltr}.neighborhood-list{display:flex;flex-wrap:wrap;gap:7px}.neighborhood-list button{color:#bcc7da;background:#101726;border:1px solid #273249;padding:8px 10px;font-size:11px;transition:.2s}.neighborhood-list button:hover{border-color:var(--blue);color:#fff}.neighborhood-list button.active{background:rgba(254,80,0,.15);border-color:var(--orange);color:#fff}.selected-box{background:linear-gradient(115deg,rgba(254,80,0,.12),transparent 90%);border:1px solid rgba(254,80,0,.25);padding:14px;margin-top:26px;position:relative;clip-path:polygon(20px 0,100% 0,100% 100%,0 100%,0 20px)}.selected-box .subtitle{font:600 10px var(--mono);color:var(--orange);direction:ltr;text-align:right}.selected-name{font-size:19px;font-weight:600;margin:5px 0}.selected-meta{display:flex;gap:6px;color:#a6aec1;font-size:11px;margin-bottom:12px}.primary{width:100%;padding:12px 10px;border:1px solid var(--orange);background:var(--orange);color:#fff;font-size:12px;font-weight:600}.primary:hover{filter:brightness(1.12)}.primary:disabled{opacity:.35;cursor:default}.divider{height:1px;background:var(--stroke);margin:20px 0}.sidebar-footer{margin-top:auto;padding-top:26px}.source-link{font-size:11px;color:#90abcf;text-decoration:none;border-bottom:1px solid #4d658a}.source-link:hover{color:white}.source-note{color:#798498;font-size:10px;line-height:1.8;margin:8px 0 0}.import-btn{display:block;background:transparent;border:1px solid #263449;color:#d8d9dc;font-size:11px;width:100%;padding:12px;margin-top:12px;text-align:center}.import-btn:hover{border-color:var(--blue)}
.stage{position:relative;overflow:hidden;min-width:0;background:radial-gradient(60% 75% at 46% 75%,rgba(0,30,96,.27),transparent 72%),linear-gradient(160deg,#07101e 0%,#050912 45%,#03050b 100%)}.stage::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:3;opacity:.13;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 170 170' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.57' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Cpath fill='%23ffffff' filter='url(%23n)' d='M0 0h170v170H0z'/%3E%3C/svg%3E");mix-blend-mode:overlay}.stage-header{position:absolute;top:28px;right:30px;z-index:8;pointer-events:none}.map-kicker{font:500 12px var(--mono);direction:ltr;color:var(--blue);letter-spacing:.18em}.map-title{font:600 clamp(23px,3vw,40px) var(--font);margin:6px 0 0;line-height:1.4}.map-subtitle{font:500 11px var(--font);color:#8092b1;margin-top:4px}.map-number{position:absolute;top:31px;left:34px;z-index:8;direction:ltr;text-align:left}.map-number strong{display:block;font:600 36px var(--display)}.map-number small{font:500 10px var(--mono);letter-spacing:.12em;color:#8e9aad}.map-container{position:absolute;inset:0;touch-action:none;cursor:grab}.map-container.grabbing{cursor:grabbing}.map-svg{width:100%;height:100%;display:block;user-select:none}.geo-grid line{stroke:#5b7eae;stroke-opacity:.09;stroke-width:.8;vector-effect:non-scaling-stroke}.geo-grid text{fill:#456382;font-size:10px;opacity:.65;pointer-events:none;font-family:var(--mono)}.district-path{fill:#13243e;fill-opacity:.76;stroke:#5d7c9e;stroke-opacity:.53;stroke-width:1.14;vector-effect:non-scaling-stroke;cursor:pointer;transition:fill .16s,stroke .16s,filter .16s}.district-path:hover{fill:#1c5282;fill-opacity:.9;stroke:#b4d8f1;stroke-opacity:.9}.district-path.is-selected{fill:var(--orange);fill-opacity:.84;stroke:#ffdcc8;stroke-width:1.7;stroke-opacity:1;filter:drop-shadow(0 0 6px rgba(254,80,0,.52))}.district-label{fill:#dce8f8;opacity:.76;font:500 13px var(--font);text-anchor:middle;dominant-baseline:central;paint-order:stroke;stroke:#0b1830;stroke-width:2.6px;stroke-opacity:.94;pointer-events:none;user-select:none}.district-label.is-selected{fill:white;opacity:1;font-weight:700;stroke:#49200e}.map-hint{position:absolute;z-index:8;bottom:24px;right:28px;display:flex;gap:10px;align-items:center;padding:11px 14px;background:rgba(6,13,24,.83);border:1px solid var(--stroke);color:#9cacc2;font-size:11px;backdrop-filter:blur(14px)}.map-hint .square{width:12px;height:12px;background:var(--orange);border:1px solid #ffbd9c}.map-controls{position:absolute;left:25px;bottom:23px;z-index:8;display:flex;gap:7px;direction:ltr}.map-controls button{border:1px solid #34445d;background:rgba(7,13,25,.9);color:#eee;width:43px;height:43px;display:grid;place-items:center;font:500 23px var(--mono);backdrop-filter:blur(12px)}.map-controls button:hover{border-color:var(--orange)}.map-controls .text-btn{font:500 10px var(--font);width:auto;padding:0 13px;direction:rtl}.north-mark{position:absolute;top:107px;left:30px;z-index:6;font:500 11px var(--mono);color:#8099b9;display:flex;align-items:center;gap:6px;direction:ltr}.north-mark .arrow{width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-bottom:15px solid var(--blue)}.data-mode button{border:1px solid #2a394e;background:rgba(10,17,31,.82);color:#9ba9bd;padding:10px 15px;font-size:11px;backdrop-filter:blur(9px)}.data-mode button.active{border-color:#5181af;background:#10243d;color:#fff}.statusbar{position:absolute;bottom:78px;right:28px;z-index:7;font:500 10px var(--mono);color:#8395b0;direction:ltr;background:rgba(4,8,16,.75);padding:5px 9px}
.details{position:absolute;top:0;bottom:0;left:0;width:min(398px,100%);background:linear-gradient(165deg,rgba(15,23,39,.98),rgba(6,9,17,.98));z-index:12;border-right:1px solid #314059;box-shadow:20px 0 80px rgba(0,0,0,.47);transform:translateX(-105%);transition:transform .28s cubic-bezier(.2,.8,.2,1);display:flex;flex-direction:column;overflow:auto}.details.open{transform:translateX(0)}.details::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#001e60,#6cace4,#fff,#fe5000)}.details-top{padding:22px 27px 15px;display:flex;justify-content:space-between;align-items:center}.details-top .id{font:500 11px var(--mono);color:var(--blue);direction:ltr}.close{width:35px;height:35px;color:#bfc7d8;background:#172137;border:1px solid #32415a;font-size:22px;line-height:1}.details-content{padding:12px 27px 27px}.details h2{font-size:33px;line-height:1.3;font-weight:600;margin:5px 0 3px}.details .en{font:500 11px var(--mono);color:var(--muted);direction:ltr}.accent-rule{height:2px;width:50px;background:var(--orange);margin:24px 0}.section-id{display:flex;gap:12px;align-items:center;color:#9babc2;font:500 10px var(--mono);direction:ltr;justify-content:flex-end;margin-bottom:15px}.section-id b{color:var(--orange)}.fact-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.fact{min-height:109px;border:1px solid var(--stroke);background:rgba(24,35,56,.45);padding:14px;display:flex;flex-direction:column;justify-content:space-between}.fact b{font:600 24px var(--display);color:#f7f5f0;direction:ltr;text-align:right}.fact label{font-size:11px;color:#a5afc1}.fact small{font-size:10px;color:#77859a}.fact b.unknown{color:#647089}.nation-box{padding:15px;background:rgba(255,255,255,.018);border:1px solid var(--stroke)}.nation-head{display:flex;justify-content:space-between;font-size:12px;margin-bottom:15px}.nation-head strong{font:600 13px var(--mono)}.nation-track{display:flex;height:7px;background:#202a3d;gap:3px}.nation-track div{width:50%;background:repeating-linear-gradient(45deg,#28354d,#28354d 4px,#1b273a 4px,#1b273a 8px)}.nation-row{display:flex;justify-content:space-between;margin-top:11px;color:#9faac0;font-size:12px}.fact-status{border-right:2px solid var(--orange);padding:10px 13px;background:rgba(254,80,0,.07);font-size:11px;color:#aeb9ce;line-height:1.9;margin:19px 0}.city-ref{background:#101b2d;padding:14px;border:1px solid #283e5c;margin:16px 0}.city-ref h4{margin:0 0 8px;font-size:12px;color:#d9e9fc}.city-ref p{margin:0;font-size:11px;color:#91a5be;line-height:1.7}.footnote{font-size:10px;color:#8392a7;line-height:1.9}.detail-link{display:block;margin-top:12px;color:var(--blue);font-size:11px;text-decoration:none}.detail-link:hover{text-decoration:underline}
.toast{position:absolute;left:50%;bottom:27px;transform:translateX(-50%) translateY(140px);z-index:50;background:#172337;border:1px solid #3d5571;color:#e5ecf7;padding:13px 19px;font-size:12px;transition:transform .25s;pointer-events:none;white-space:nowrap}.toast.show{transform:translateX(-50%) translateY(0)}.mobile-cue{display:none}.mobile-detail-trigger{display:none}.hidden{display:none!important}
/* ---- v2: sectors, roads, metro, labels, layers, marketing panel ---- */
.map-svg.sectors-on .district-path{fill:var(--sf,#13243e);fill-opacity:.26;stroke:#050a14;stroke-opacity:.85;stroke-width:1.1}
.map-svg.sectors-on .district-path:hover{fill-opacity:.46;stroke:#fff;stroke-opacity:.9}
.map-svg .district-path.is-selected,.map-svg.sectors-on .district-path.is-selected{fill:var(--orange);fill-opacity:.88;stroke:#ffdcc8;stroke-width:1.8;stroke-opacity:1}
.district-label{font-weight:500;fill:#f3f6fb;stroke:#060b16;stroke-opacity:.92;paint-order:stroke;opacity:.95}
.map-svg.names-off #labelLayer{display:none}
.road-casing{fill:none;stroke:#03050b;stroke-opacity:.85;stroke-width:6;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;pointer-events:none}
.road-line{fill:none;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;pointer-events:none;transition:opacity .2s}
.road-group.dim{opacity:.13}.road-group.focus .road-line{stroke-width:4.6}
.road-stub{fill:none;stroke-width:2.6;stroke-dasharray:5 4;vector-effect:non-scaling-stroke;pointer-events:none}
.road-label{font:600 11px var(--font);paint-order:stroke;stroke:#03050b;stroke-opacity:.95;text-anchor:middle;dominant-baseline:central;pointer-events:none;user-select:none}
.road-label.dim{opacity:.15}
.metro-line{fill:none;stroke-width:3.4;stroke-linecap:round;stroke-dasharray:1 0;vector-effect:non-scaling-stroke;pointer-events:none;opacity:.95}
.metro-casing{fill:none;stroke:#fff;stroke-opacity:.75;stroke-width:5.6;vector-effect:non-scaling-stroke;pointer-events:none}
.metro-station{fill:#03050b;stroke:#fff;stroke-width:1.4;vector-effect:non-scaling-stroke;pointer-events:none}
.layers{position:absolute;left:25px;top:150px;z-index:9;width:250px;max-height:calc(100% - 240px);display:flex;flex-direction:column;background:rgba(6,11,22,.9);border:1px solid #2a394e;backdrop-filter:blur(12px)}
.layers-toggle{display:flex;justify-content:space-between;align-items:center;width:100%;background:transparent;border:0;border-bottom:1px solid #22304a;color:#e8edf6;padding:11px 13px;font-size:12px;font-weight:600}
.layers-toggle span:last-child{font:500 10px var(--mono);color:#7f90aa;direction:ltr}
.layers.collapsed .layers-body{display:none}.layers.collapsed .layers-toggle{border-bottom:0}
.layers-body{overflow:auto;padding:10px 13px 13px}
.lyr{display:flex;align-items:center;gap:9px;font-size:12px;color:#d7deea;padding:6px 0;cursor:pointer}
.lyr input{accent-color:var(--orange);width:15px;height:15px;margin:0}
.seg{display:flex;gap:4px;margin:4px 0 8px}.seg button{flex:1;background:#0e1626;border:1px solid #2b3a53;color:#9aa8bd;font-size:10px;padding:7px 4px}.seg button.active{border-color:var(--orange);color:#fff;background:rgba(254,80,0,.12)}
.legend{display:grid;grid-template-columns:1fr 1fr;gap:5px 10px;margin:2px 0 8px}.legend div,.road-item{display:flex;align-items:center;gap:7px;font-size:10.5px;color:#aeb9cb}
.legend i{width:11px;height:11px;border-radius:2px;flex:none;opacity:.9}.legend b{font:500 9px var(--mono);color:#6f7f97;margin-inline-start:auto}
.road-legend{display:flex;flex-direction:column;gap:1px;margin:2px 0 8px}
.road-item{width:100%;background:none;border:0;padding:5px 3px;text-align:right;font:inherit;font-size:11px;color:#c7d0de}
.road-item i{width:18px;height:4px;border-radius:2px;flex:none}.road-item:hover,.road-item.on{background:#13203a;color:#fff}
.road-item small{margin-inline-start:auto;color:#6c7c94;font-size:9.5px}
.layers .src{font-size:9.5px;color:#6e7d94;line-height:1.7;margin:6px 0 0}
.lyr-sep{height:1px;background:#1f2b40;margin:6px 0}
.chip{display:inline-flex;align-items:center;gap:6px;font-size:11px;padding:4px 9px;border:1px solid #2c3b55;background:#0f1828;color:#dbe3ef;margin:0 0 6px 6px}
.chip i{width:9px;height:9px;border-radius:2px}
.tier{display:flex;gap:3px;margin:10px 0 6px}.tier span{flex:1;height:7px;background:#1d2738}.tier span.on{background:var(--orange)}
.tier-labels{display:flex;justify-content:space-between;font-size:9.5px;color:#7a879c}
.fact-grid.three{grid-template-columns:repeat(3,1fr)}.fact-grid.three .fact{min-height:84px;padding:11px}.fact-grid.three .fact b{font-size:20px}
.insights{margin:0;padding:0;list-style:none}.insights li{position:relative;padding:9px 14px 9px 0;font-size:12px;line-height:1.85;color:#cfd7e4;border-bottom:1px dashed #223049}
.insights li::before{content:"";position:absolute;right:0;top:17px;width:6px;height:6px;background:var(--orange)}
.metro-list{margin:0;padding:0;list-style:none;font-size:12px;color:#cfd7e4}.metro-list li{padding:4px 0}
.muted{color:#7d8aa0;font-size:11px;line-height:1.8}
.src-list{margin:0;padding:0 16px 0 0;font-size:10.5px;color:#8392a7;line-height:1.9}.src-list a{color:#8fb3d9}
.sector-badge{display:inline-flex;align-items:center;gap:7px;font-size:12px;color:#dbe3ef;margin-top:10px}.sector-badge i{width:10px;height:10px;border-radius:2px}
@media(max-width:1100px){.workspace{grid-template-columns:285px minmax(0,1fr)}.sidebar{padding:23px 18px}.topbar{padding:0 18px}.stage-header{right:19px;top:19px}.map-number{left:18px}.map-controls{left:13px}.map-hint{right:13px}.details{width:360px}}
@media(max-width:760px){.topbar{height:62px;padding:0 13px}.topcenter{display:none}.brandword{font-size:17px}.logo-icon{height:32px;width:32px;font-size:17px}.brand small{font-size:7px}.topaction{font-size:10px;padding:8px}.workspace{display:block;height:calc(100dvh - 62px);min-height:700px}.sidebar{height:122px;padding:14px 14px 12px;overflow:visible;position:relative;z-index:9;border-left:0;border-bottom:1px solid var(--stroke);background:#070c16}.sidebar .eyebrow,.sidebar .sub,.sidebar .section-label,.sidebar .neighborhood-list,.sidebar .selected-box,.sidebar .divider,.sidebar .sidebar-footer{display:none}.sidebar h1{font-size:23px;margin:0 0 12px}.searchbox{max-width:none}.searchbox input{padding:11px 40px 11px 12px}.searchglyph{top:10px}.stage{height:calc(100dvh - 184px);min-height:420px}.stage-header{top:15px;right:14px}.map-title{font-size:18px}.map-subtitle{display:none}.map-kicker{font-size:8px}.map-number{top:16px;left:15px}.map-number strong{font-size:24px}.map-number small{font-size:8px}.north-mark{display:none}.data-mode{top:88px;left:12px}.data-mode button{padding:7px 9px;font-size:10px}.map-hint{bottom:15px;right:10px;padding:8px 9px;font-size:10px;max-width:55%;line-height:1.5}.map-controls{left:8px;bottom:10px;gap:5px}.map-controls button{width:35px;height:35px;font-size:19px}.map-controls .text-btn{font-size:9px;padding:0 8px}.statusbar{bottom:65px;right:10px;font-size:8px}.mobile-detail-trigger{display:block;position:absolute;bottom:63px;right:10px;z-index:9;background:var(--orange);border:0;color:white;font-size:12px;font-weight:600;padding:11px 15px;box-shadow:0 8px 25px rgba(254,80,0,.28)}.details{width:100%;top:auto;bottom:0;height:min(72dvh,590px);max-height:100%;border-top:1px solid #4b658a;border-right:0;transform:translateY(105%);border-radius:14px 14px 0 0}.details.open{transform:translateY(0)}.details h2{font-size:28px}.details-content{padding:7px 22px 30px}.details-top{padding:16px 22px}.mobile-cue{display:block;position:absolute;top:6px;left:calc(50% - 23px);height:4px;width:46px;border-radius:9px;background:#425371}.sidebar .section-label,.sidebar .neighborhood-list{display:none}.footnote{font-size:10px}.layers{top:88px;left:10px;width:min(236px,62vw);max-height:calc(100% - 175px)}.layers-toggle{padding:9px 11px;font-size:11px}.lyr{font-size:11.5px;padding:5px 0}.map-controls{flex-wrap:wrap;max-width:62%}.map-controls .text-btn{height:35px}.road-label{font-size:10px}.fact-grid.three .fact b{font-size:17px}.fact-grid.three .fact{min-height:74px;padding:9px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{transition:none!important;animation:none!important}}
</style>
</head>
<body><div class="app">
<header class="topbar"><div class="brand"><div class="logo-icon" aria-hidden="true">C</div><div><div class="brandword">PLAN<span>/</span>C</div><small>THE THIRD DIMENSION</small></div></div><div class="topcenter"><span class="live-dot"></span><span>GEOSPATIAL INTERFACE / RIYADH / 2026</span></div><button class="topaction" id="exportBtn" title="تصدير بيانات الحي المحدد">↓ &nbsp;تصدير المحدد</button></header>
<div class="workspace"><aside class="sidebar"><div class="eyebrow">01 / URBAN EXPLORER</div><h1>أحياء <b>الرياض.</b></h1><p class="sub">حدود الأحياء، الجهات، الطرق الرئيسية، ومؤشرات تسويقية لكل حي من مصادر رسمية ومفتوحة. اضغط على أي حي لتحديده، واضغط مرتين لعرض ملفه.</p><div class="searchbox"><span class="searchglyph">⌕</span><input id="search" type="search" autocomplete="off" placeholder="ابحث باسم الحي..." aria-label="البحث عن حي"><div class="search-results hidden" id="results"></div></div><div class="section-label"><span>أحياء سريعة الوصول</span><span>QUICK ACCESS</span></div><div class="neighborhood-list" id="quick"></div><div class="selected-box"><div class="subtitle">SELECTED DISTRICT</div><div id="selectedName" class="selected-name">لم يتم تحديد حي</div><div class="selected-meta" id="selectedMeta">انقر على إحدى المساحات في الخريطة</div><button class="primary" id="detailsBtn" disabled>عرض ملف الحي ↗</button></div><div class="sidebar-footer"><div class="divider"></div><div class="eyebrow">DATA INTEGRITY</div><p class="source-note">تشمل هذه النسخة <span id="countSide">145</span> حيًا (حدود OpenStreetMap)، ولا تمثل كل أحياء الرياض. كل رقم في ملف الحي محسوب من مصدر مذكور؛ الشرطة «—» تعني عدم توفر بيانات، لا صفرًا.</p><a class="source-link" href="#" id="sourcesLink">المصادر والمنهجية ↗</a><label class="import-btn" for="importCsv">+ استيراد إحصاءات الأحياء CSV</label><input id="importCsv" class="hidden" type="file" accept=".csv,text/csv"><p class="source-note" id="dataStatus">لا توجد بيانات إحصائية محلية محمّلة.</p></div></aside>
<main class="stage" id="stage" aria-label="خريطة تفاعلية لأحياء الرياض"><div class="stage-header"><div class="map-kicker">RIYADH / GIS EXPLORE</div><div class="map-title">خريطة الأحياء</div><div class="map-subtitle" id="mapSubtitle">ألوان الجهات حسب تقسيم الهيئة الملكية لمدينة الرياض</div></div><div class="map-number"><strong id="countTop">145</strong><small>MAPPED DISTRICTS</small></div><div class="north-mark"><i class="arrow"></i>N</div>
<section class="layers" id="layers" aria-label="طبقات الخريطة"><button class="layers-toggle" id="layersBtn" aria-expanded="true"><span>طبقات الخريطة ▾</span><span>LAYERS</span></button><div class="layers-body">
<label class="lyr"><input type="checkbox" id="lyrNames" checked> أسماء الأحياء</label>
<label class="lyr"><input type="checkbox" id="lyrSectors" checked> ألوان الجهات</label>
<div class="seg" id="sectorMode"><button data-mode="official" class="active">تقسيم الهيئة الملكية</button><button data-mode="geo">4 جهات جغرافية</button></div>
<div class="legend" id="sectorLegend"></div>
<div class="lyr-sep"></div>
<label class="lyr"><input type="checkbox" id="lyrRoads" checked> الطرق الرئيسية</label>
<div class="road-legend" id="roadLegend"></div>
<div class="lyr-sep"></div>
<label class="lyr"><input type="checkbox" id="lyrMetro"> مسارات مترو الرياض</label>
<p class="src">الطرق: OpenStreetMap (لقطة 11 أكتوبر 2026، مبسطة). الجهات والمترو: منصة البيانات المفتوحة للهيئة الملكية لمدينة الرياض.</p>
</div></section>
<div class="map-container" id="mapContainer"><svg class="map-svg sectors-on" id="mapSvg" role="img" aria-label="خريطة حدود أحياء الرياض، يمكن الضغط على مضلع أي حي لتحديده" viewBox="0 0 1100 1000"><defs><marker id="arrowHead" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#FDE68A"/></marker></defs><g class="geo-grid" id="geoGrid"></g><g id="districtLayer"></g><g id="metroLayer" class="hidden"></g><g id="roadLayer"></g><g id="labelLayer"></g><g id="roadLabelLayer"></g></svg></div><div class="statusbar" id="mapStatus">LOCAL VECTOR / OPEN GEODATA</div><button class="mobile-detail-trigger hidden" id="mobileDetailBtn">ملف الحي ↗</button><div class="map-hint"><span class="square"></span><span>نقرة: تحديد <span style="opacity:.6">/</span> نقرتان: الملف <span style="opacity:.6">/</span> إصبعان: تكبير</span></div><div class="map-controls"><button id="plus" aria-label="تكبير">+</button><button id="minus" aria-label="تصغير">−</button><button id="reset" class="text-btn">المدينة</button><button id="allBtn" class="text-btn">كامل النطاق</button><button id="clearBtn" class="text-btn">إزالة التحديد</button></div>
<section class="details" id="details" role="dialog" aria-modal="false" aria-labelledby="detailName"><div class="mobile-cue"></div><div class="details-top"><span class="id">02 / DISTRICT INTELLIGENCE</span><button class="close" id="closeDetails" aria-label="إغلاق التفاصيل">×</button></div><div class="details-content" id="detailBody"></div></section>
<div class="toast" id="toast"></div>
</main></div></div>
<script>
// District boundaries: OpenStreetMap via github.com/i1s1i/GIS-rcrc-map (simplified ~12 m).
// Every metric below is computed by tools/enrich.py from the sources listed in README.md.
const GEO = __GEO__;
const ENR = __ENR__;
const svgNS = 'http://www.w3.org/2000/svg';
const $ = s => document.getElementById(s);
const SECTOR_COLORS = {'الشمال':'#8EC5FF','الشرق':'#8FE0A8','الجنوب':'#F2CF8B','الغرب':'#C9B2F7','الوسط':'#E5E3DA','الدرعية':'#F2B8A0'};
const SECTOR_ORDER = ['الشمال','الشرق','الغرب','الجنوب','الوسط','الدرعية'];
const ROAD_BY_KEY = Object.fromEntries(ENR.roads.map(r => [r.key, r]));
const quickNames = ['الملقا','الياسمين','الصحافة','النرجس','حطين','العليا','الرحمانية','السليمانية','النخيل','الورود','الملز','قرطبة'];
const state = {names: true, sectors: true, sectorMode: 'official', roads: true, metro: false, focusRoad: null};
let districts = [], byName = new Map(), svgPaths = new Map(), labels = new Map(), roadLabels = [], selected = null, stats = new Map(), viewBox = null, hasMoved = false;

function notify(msg){ $('toast').textContent = msg; $('toast').classList.add('show'); clearTimeout(notify.t); notify.t = setTimeout(() => $('toast').classList.remove('show'), 2700); }
function cleanName(s){ return String(s || '').replace(/^حي\s+/, '').replace(/\s+/g, ' ').trim(); }
function esc(s){ return String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
const nf = new Intl.NumberFormat('en-US', {maximumFractionDigits: 0});
const fmt = n => n === null || n === undefined || !Number.isFinite(+n) ? '—' : nf.format(n);
function metrics(name){ return ENR.districts[name] || {}; }
function sectorOf(name){ const m = metrics(name); return state.sectorMode === 'official' ? m.sector : m.sector4; }

// ---------- projection ----------
const PX_PER_DEG = 1650, BASE_LON = 46.4, BASE_NORTH = 25.05, LON_COS = Math.cos(24.72 * Math.PI / 180), UNITS_PER_KM = PX_PER_DEG / 110.57;
const xy = p => [(p[0] - BASE_LON) * PX_PER_DEG * LON_COS, (BASE_NORTH - p[1]) * PX_PER_DEG];
const ringPath = r => r.map((p, i) => { const [x, y] = xy(p); return (i ? 'L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1); }).join('') + 'Z';
const linePath = l => l.map((p, i) => { const [x, y] = xy(p); return (i ? 'L' : 'M') + x.toFixed(1) + ' ' + y.toFixed(1); }).join('');
function createSvg(name, attrs, parent){ const el = document.createElementNS(svgNS, name); for (const k in attrs) el.setAttribute(k, attrs[k]); parent.appendChild(el); return el; }

function decorate(g, i){
  const rings = g.g.flat(1); const box = [Infinity, Infinity, -Infinity, -Infinity];
  for (const r of rings) for (const p of r){ box[0] = Math.min(box[0], p[0]); box[1] = Math.min(box[1], p[1]); box[2] = Math.max(box[2], p[0]); box[3] = Math.max(box[3], p[1]); }
  const m = ENR.districts[g.n] || {};
  return {id: i, name: g.n, rings, center: g.l, inner: Math.max(.08, g.r || .2), area: m.area || 0, bbox: box};
}

// ---------- rendering ----------
function renderGrid(){ const layer = $('geoGrid'); layer.replaceChildren(); for (let lat = 24.4; lat < 25.05; lat += .05){ const [, y] = xy([46.4, lat]); createSvg('line', {x1: 0, y1: y, x2: 1100, y2: y}, layer); } for (let lon = 46.4; lon <= 47.05; lon += .05){ const [x] = xy([lon, 25.05]); createSvg('line', {x1: x, y1: 0, x2: x, y2: 1150}, layer); } }
function renderDistricts(){
  const layer = $('districtLayer'), lab = $('labelLayer'); layer.replaceChildren(); lab.replaceChildren(); svgPaths.clear(); labels.clear();
  byName = new Map(districts.map(d => [d.name, d]));
  for (const d of districts){
    const p = createSvg('path', {d: d.rings.map(ringPath).join(''), 'fill-rule': 'evenodd', class: 'district-path', 'data-name': d.name, tabindex: '0', role: 'button', 'aria-label': 'تحديد ' + d.name}, layer);
    createSvg('title', {}, p).textContent = d.name;
    p.addEventListener('keydown', e => { if (e.key === 'Enter'){ choose(d.name); if (e.shiftKey) showDetails(d.name); } });
    svgPaths.set(d.name, p);
    const [x, y] = xy(d.center); const t = createSvg('text', {x: x.toFixed(1), y: y.toFixed(1), class: 'district-label', 'text-anchor': 'middle', 'dominant-baseline': 'central', 'data-name': d.name}, lab);
    t.textContent = d.name; labels.set(d.name, t);
  }
  applySectors(); $('countTop').textContent = districts.length; $('countSide').textContent = districts.length;
}
function renderRoads(){
  const layer = $('roadLayer'), lab = $('roadLabelLayer'); layer.replaceChildren(); lab.replaceChildren(); roadLabels = [];
  for (const r of ENR.roads){
    const g = createSvg('g', {class: 'road-group', 'data-key': r.key}, layer); const d = r.lines.map(linePath).join('');
    createSvg('path', {d, class: 'road-casing'}, g); createSvg('path', {d, class: 'road-line', stroke: r.color}, g);
    if (r.bridges && r.bridges.length) createSvg('path', {d: r.bridges.map(linePath).join(''), class: 'road-stub', stroke: r.color}, g);
    // label anchor: middle vertex of the longest piece
    const longest = r.lines.reduce((a, b) => b.length > a.length ? b : a, []); let best = longest[Math.floor(longest.length / 2)];
    if (longest.length === 2) best = [(longest[0][0] + longest[1][0]) / 2, (longest[0][1] + longest[1][1]) / 2];
    const [x, y] = xy(best); const t = createSvg('text', {x: x.toFixed(1), y: y.toFixed(1), class: 'road-label', fill: r.color, 'data-key': r.key}, lab); t.textContent = r.ar; roadLabels.push({el: t, key: r.key, x, y});
  }
  // Riyadh–Qassim: direction marker only (rural geometry is outside the bundled OSM extract)
  const kf = ENR.roads.find(r => r.key === 'kfahd'), q = ENR.qassim, last = kf.lines.flat().sort((a, b) => b[1] - a[1]);
  const a = last[0], b = last[1] || last[0]; const len = Math.hypot(a[0] - b[0], a[1] - b[1]) || 1; const end = [a[0] + (a[0] - b[0]) / len * .025, a[1] + (a[1] - b[1]) / len * .025];
  const g = createSvg('g', {class: 'road-group', 'data-key': 'qassim'}, layer);
  createSvg('path', {d: linePath([a, end]), class: 'road-stub', stroke: q.color, 'marker-end': 'url(#arrowHead)'}, g);
  const [x, y] = xy(end); const t = createSvg('text', {x: x.toFixed(1), y: (y - 6).toFixed(1), class: 'road-label', fill: q.color, 'data-key': 'qassim'}, lab);
  t.textContent = q.ar; roadLabels.push({el: t, key: 'qassim', x, y: y - 6});
}
function renderMetro(){
  const layer = $('metroLayer'); layer.replaceChildren();
  for (const l of ENR.metro){ const d = l.lines.map(linePath).join(''); createSvg('path', {d, class: 'metro-casing'}, layer); const p = createSvg('path', {d, class: 'metro-line', stroke: l.color}, layer); createSvg('title', {}, p).textContent = l.name + ' · ' + (l.ends || ''); }
  for (const s of ENR.metro_stations){ const [x, y] = xy(s.p); const c = createSvg('circle', {cx: x.toFixed(1), cy: y.toFixed(1), r: 2.2, class: 'metro-station'}, layer); createSvg('title', {}, c).textContent = 'محطة ' + s.n + ' · ' + s.l; }
}
function applySectors(){
  const svg = $('mapSvg'); svg.classList.toggle('sectors-on', state.sectors);
  for (const [n, p] of svgPaths){ const s = sectorOf(n); p.style.setProperty('--sf', SECTOR_COLORS[s] || '#13243e'); p.dataset.sector = s || ''; }
  const counts = {}; for (const d of districts){ const s = sectorOf(d.name); counts[s] = (counts[s] || 0) + 1; }
  $('sectorLegend').innerHTML = SECTOR_ORDER.filter(s => counts[s]).map(s => `<div><i style="background:${SECTOR_COLORS[s]}"></i>${esc(s)}<b>${counts[s]}</b></div>`).join('');
  $('sectorLegend').style.display = state.sectors ? '' : 'none'; $('sectorMode').style.display = state.sectors ? '' : 'none';
  $('mapSubtitle').textContent = !state.sectors ? 'حدود الأحياء حسب الإحداثيات' : state.sectorMode === 'official' ? 'ألوان الجهات حسب تقسيم الهيئة الملكية لمدينة الرياض' : 'ألوان الجهات: 4 جهات جغرافية من مركز المدينة';
}
function buildRoadLegend(){
  const box = $('roadLegend'); box.replaceChildren();
  for (const r of [...ENR.roads, ENR.qassim]){
    const b = document.createElement('button'); b.type = 'button'; b.className = 'road-item'; b.dataset.key = r.key;
    b.innerHTML = `<i style="background:${r.color}${r.key === 'qassim' ? ';opacity:.7' : ''}"></i><span>${esc(r.ar)}</span>${r.key === 'qassim' ? '<small>اتجاه فقط</small>' : ''}`;
    b.onclick = () => focusRoad(state.focusRoad === r.key ? null : r.key); box.append(b);
  }
}
function focusRoad(key){
  state.focusRoad = key; if (key && !state.roads){ state.roads = true; $('lyrRoads').checked = true; applyLayers(); }
  document.querySelectorAll('.road-group').forEach(g => { g.classList.toggle('dim', !!key && g.dataset.key !== key); g.classList.toggle('focus', g.dataset.key === key); });
  document.querySelectorAll('.road-item').forEach(b => b.classList.toggle('on', b.dataset.key === key));
  for (const l of roadLabels) l.el.classList.toggle('dim', !!key && l.key !== key);
  if (key){ const r = key === 'qassim' ? ROAD_BY_KEY.kfahd : ROAD_BY_KEY[key]; const pts = r.lines.flat().map(xy); const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]); const w = Math.max(...xs) - Math.min(...xs), h = Math.max(...ys) - Math.min(...ys); const pad = Math.max(w, h) * .18 + 25; setBox([Math.min(...xs) - pad, Math.min(...ys) - pad, w + pad * 2, h + pad * 2]); }
  refreshLabels();
}
function applyLayers(){
  $('mapSvg').classList.toggle('names-off', !state.names);
  $('roadLayer').classList.toggle('hidden', !state.roads); $('roadLabelLayer').classList.toggle('hidden', !state.roads); $('roadLegend').style.display = state.roads ? '' : 'none';
  $('metroLayer').classList.toggle('hidden', !state.metro); refreshLabels();
}

// ---------- view box ----------
function setBox(b){ viewBox = {x: b[0], y: b[1], w: b[2], h: b[3]}; updateBox(); }
function updateBox(){ $('mapSvg').setAttribute('viewBox', [viewBox.x, viewBox.y, viewBox.w, viewBox.h].map(n => +n.toFixed(2)).join(' ')); refreshLabels(); }
const fullBox = [10, 15, 1060, 1110], urbanBox = [150, 170, 600, 720];
function fitCore(){ setBox(urbanBox); }
function fitAll(){ setBox(fullBox); }
function focusDistrict(d){ const [x1, y1] = xy([d.bbox[0], d.bbox[3]]), [x2, y2] = xy([d.bbox[2], d.bbox[1]]); const w = Math.max(115, x2 - x1), h = Math.max(115, y2 - y1), s = 1.8; setBox([(x1 + x2) / 2 - w * s / 2, (y1 + y2) / 2 - h * s / 2, w * s, h * s]); }
function viewMetrics(){ const rect = $('mapSvg').getBoundingClientRect(); const k = Math.min(rect.width / viewBox.w, rect.height / viewBox.h); return {rect, k, ox: (rect.width - viewBox.w * k) / 2, oy: (rect.height - viewBox.h * k) / 2}; }

// ---------- labels: every district name, sized to its shape, collision-checked ----------
function refreshLabels(){
  if (!viewBox) return; const {rect, k, ox, oy} = viewMetrics(); if (!rect.width || !rect.height) return;
  const small = rect.width < 560, minF = small ? 7 : 7.5, maxF = small ? 12 : 13.5, occ = [];
  const hit = b => occ.some(o => !(b[2] < o[0] || b[0] > o[2] || b[3] < o[1] || b[1] > o[3]));
  const toScreen = (x, y) => [ox + (x - viewBox.x) * k, oy + (y - viewBox.y) * k];
  const order = [...districts].sort((a, b) => (b.name === selected) - (a.name === selected) || b.inner - a.inner);
  for (const d of order){
    const el = labels.get(d.name); if (!el) continue; const [x, y] = xy(d.center); const [sx, sy] = toScreen(x, y);
    if (sx < -60 || sx > rect.width + 60 || sy < -30 || sy > rect.height + 30){ el.style.display = 'none'; continue; }
    const innerPx = d.inner * UNITS_PER_KM * k, len = d.name.length;
    let f = Math.min(maxF, Math.max(minF, 2.5 * innerPx / (len * .5))); if (d.name === selected) f = Math.max(f, 11);
    const w = len * .5 * f + 4, h = f * 1.15, box = [sx - w / 2, sy - h / 2, sx + w / 2, sy + h / 2];
    if (d.name !== selected && hit(box)){ el.style.display = 'none'; continue; }
    occ.push(box); el.style.display = ''; el.style.fontSize = (f / k).toFixed(3) + 'px'; el.style.strokeWidth = (Math.max(2, f * .3) / k).toFixed(3) + 'px';
    el.classList.toggle('is-selected', d.name === selected);
  }
  if (state.roads) for (const l of roadLabels){
    const [sx, sy] = toScreen(l.x, l.y), f = small ? 9.5 : 11, w = l.el.textContent.length * .5 * f + 6, box = [sx - w / 2, sy - f * .7, sx + w / 2, sy + f * .7];
    const visible = sx > -40 && sx < rect.width + 40 && sy > -20 && sy < rect.height + 20 && (!hit(box) || state.focusRoad === l.key);
    l.el.style.display = visible ? '' : 'none'; if (visible){ occ.push(box); l.el.style.fontSize = (f / k).toFixed(3) + 'px'; l.el.style.strokeWidth = (3 / k).toFixed(3) + 'px'; }
  }
  if (state.metro) document.querySelectorAll('.metro-station').forEach(c => c.setAttribute('r', (Math.max(2.2, Math.min(4.5, 1.2 * k)) / k).toFixed(3)));
}

// ---------- selection & details ----------
function choose(name, focus = false){
  const d = byName.get(name); if (!d) return; selected = name;
  for (const [n, p] of svgPaths) p.classList.toggle('is-selected', n === name);
  const m = metrics(name); $('selectedName').textContent = name;
  $('selectedMeta').textContent = (m.sector ? 'قطاع ' + m.sector.replace(/^ال/, '') + ' · ' : '') + d.area.toFixed(2) + ' كم²';
  $('detailsBtn').disabled = false; $('mobileDetailBtn').classList.remove('hidden');
  document.querySelectorAll('.neighborhood-list button').forEach(b => b.classList.toggle('active', b.dataset.name === name));
  if (focus) focusDistrict(d); else refreshLabels();
}
const SRC = {
  osm: '<a target="_blank" rel="noopener noreferrer" href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  rcrc: '<a target="_blank" rel="noopener noreferrer" href="https://opendata.rcrc.gov.sa">الهيئة الملكية لمدينة الرياض – البيانات المفتوحة</a>',
  moj: '<a target="_blank" rel="noopener noreferrer" href="https://open.data.gov.sa">وزارة العدل – المنصة الوطنية للبيانات المفتوحة</a>'
};
const TIER_NAMES = ['أقل من الربع الأدنى', 'دون الوسيط', 'فوق الوسيط', 'الربع الأعلى'];
function median(arr){ const a = arr.filter(Number.isFinite).sort((x, y) => x - y); return a.length ? a[Math.floor(a.length / 2)] : null; }
const CITY = (() => {
  const vals = Object.values(ENR.districts);
  const dens = median(vals.map(m => m.rcrc_density).filter(v => v !== null && v !== undefined));
  const deeds = vals.map(m => m.moj && m.moj.deeds).filter(Number.isFinite).sort((a, b) => a - b);
  return {density: dens, deedsQ3: deeds[Math.floor(deeds.length * .75)]};
})();
function insightsFor(name){
  const m = metrics(name), out = [], c = m.rcrc || {};
  if (m.tier === 3) out.push('أسعار الأراضي السكنية في الربع الأعلى بين أحياء الرياض المرصودة (≥ ' + fmt(ENR.land_quartiles[2]) + ' ر.س/م²): حي مرتفع القيمة العقارية.');
  else if (m.tier === 0) out.push('أسعار الأراضي السكنية في الربع الأدنى (< ' + fmt(ENR.land_quartiles[0]) + ' ر.س/م²): حي ذو قيمة عقارية أقل من معظم الأحياء المرصودة.');
  if (m.roads && m.roads.length) out.push('يحاذي ' + m.roads.map(k => ROAD_BY_KEY[k].ar).join('، ') + ': مواقع محتملة للإعلانات الخارجية وظهور المحلات للمارّة بالسيارة.');
  if (m.metro_in && m.metro_in.length) out.push('داخل الحي ' + (m.metro_in.length === 1 ? 'محطة مترو' : m.metro_in.length + ' محطات مترو') + ': حركة تنقّل يومية يمكن استهدافها بإعلانات المحطات والمنشآت القريبة.');
  else if (m.metro_near && m.metro_near.km <= 1.5) out.push('أقرب محطة مترو (' + m.metro_near.name + ') على بعد نحو ' + m.metro_near.km.toFixed(1) + ' كم من وسط الحي.');
  if (CITY.density && m.rcrc_density !== null && m.rcrc_density !== undefined){
    if (m.rcrc_density >= CITY.density * 2) out.push('كثافة الخدمات التجارية المسجلة ' + m.rcrc_density.toFixed(1) + '/كم²، أكثر من ضعف وسيط الأحياء (' + CITY.density.toFixed(1) + '): منطقة تسوق ونشاط تجاري.');
    else if (m.rcrc_density < CITY.density / 2 && m.area > .5) out.push('كثافة تجارية منخفضة (' + m.rcrc_density.toFixed(1) + '/كم² مقابل وسيط ' + CITY.density.toFixed(1) + '): طابع سكني غالب، وقد تكون فرصة لخدمات الحي.');
  }
  if (m.moj && m.moj.deeds >= CITY.deedsQ3) out.push('نشاط صفقات عقارية مرتفع: ' + fmt(m.moj.deeds) + ' صكًا في 2025 (ر1–ر3)، ضمن أعلى 25% من الأحياء — سوق عقاري نشط.');
  if ((c.hotel || 0) >= 5) out.push('تركّز فندقي: ' + c.hotel + ' فندقًا وشققًا فندقية مسجلة — حضور ملحوظ للزوار.');
  if ((m.entertainment || 0) >= 3) out.push(m.entertainment + ' مرافق ترفيهية مسجلة لدى الهيئة الملكية.');
  return out;
}
function priceFact(label, x){
  if (!x) return `<div class="fact"><label>${label}</label><b class="unknown">—</b><small>لا صفقات مسجلة</small></div>`;
  if (!x.ppm) return `<div class="fact"><label>${label}</label><b class="unknown">—</b><small>${fmt(x.deeds)} صك · عينة لا تكفي لنشر متوسط</small></div>`;
  return `<div class="fact"><label>${label}</label><b>${fmt(x.ppm)}</b><small>ر.س/م² · ${fmt(x.deeds)} صك${x.deeds < 15 ? ' · عينة محدودة' : ''}</small></div>`;
}
function showDetails(name){
  const d = byName.get(name); if (!d) return; choose(name);
  const m = metrics(name), c = m.rcrc || {}, row = stats.get(name) || {}, validStats = !!(row.source && row.year);
  const pop = validStats && optional(row.population_estimate) !== null ? optional(row.population_estimate) : null;
  const sec = m.sector || '—', sec4 = m.sector4 || '—', moj = m.moj;
  const tierHtml = m.tier === null || m.tier === undefined ? '<p class="muted">لا يوجد متوسط منشور لسعر متر الأرض السكنية لهذا الحي في الفترة.</p>'
    : `<div class="tier">${[0, 1, 2, 3].map(i => `<span class="${i <= m.tier ? 'on' : ''}"></span>`).join('')}</div><div class="tier-labels"><span>أدنى</span><span>${TIER_NAMES[m.tier]}</span><span>أعلى</span></div>`;
  const roads = (m.roads || []).map(k => `<span class="chip"><i style="background:${ROAD_BY_KEY[k].color}"></i>${esc(ROAD_BY_KEY[k].ar)}</span>`).join('') || '<p class="muted">لا يمر بمحاذاته أي من الطرق الرئيسية الأربعة عشر المعروضة.</p>';
  const metro = m.metro_in && m.metro_in.length ? '<ul class="metro-list">' + m.metro_in.map(s => `<li>● ${esc(s)}</li>`).join('') + '</ul>' : `<p class="muted">لا محطات داخل الحي. الأقرب: ${esc(m.metro_near ? m.metro_near.name + ' (' + m.metro_near.line + ')' : '—')}${m.metro_near ? ' على بعد ' + m.metro_near.km.toFixed(1) + ' كم من وسطه' : ''}.</p>`;
  const ins = insightsFor(name);
  const how = {name: 'حسب اسم الحي في بيانات الهيئة', points: 'حسب نقاط الهيئة داخل حدوده', nearest: 'تقديري: حسب أقرب نقطة مصنفة'}[m.sector_how] || '';
  $('detailBody').innerHTML = `
  <div class="eyebrow">RIYADH · NEIGHBORHOOD PROFILE</div><h2 id="detailName">${esc(name)}</h2><div class="en">DISTRICT / ${String(d.id + 1).padStart(3, '0')}</div>
  <div class="sector-badge"><i style="background:${SECTOR_COLORS[sec] || '#555'}"></i>قطاع ${esc(sec)} · بلدية ${esc(m.submun || '—')}</div>
  <div class="accent-rule"></div>
  <div class="section-id"><b>01</b> OVERVIEW</div>
  <div class="fact-grid"><div class="fact"><label>المساحة (تقريبًا)</label><b>${d.area >= 10 ? d.area.toFixed(1) : d.area.toFixed(2)}</b><small>كم² · محسوبة من الحدود</small></div>
  <div class="fact"><label>البعد عن قصر الحكم</label><b>${m.center_km ?? '—'}</b><small>كم · خط مستقيم من وسط الحي</small></div>
  <div class="fact"><label>عدد السكان</label><b class="${pop === null ? 'unknown' : ''}">${fmt(pop)}</b><small>${pop === null ? 'غير متوفر لهذا الحي' : esc('سنة ' + row.year + ' · ' + (row.method || 'تقدير'))}</small></div>
  <div class="fact"><label>كثافة الخدمات التجارية</label><b class="${m.rcrc_density == null ? 'unknown' : ''}">${m.rcrc_density == null ? '—' : m.rcrc_density.toFixed(1)}</b><small>منشأة مسجلة لكل كم² · وسيط الأحياء ${CITY.density ? CITY.density.toFixed(1) : '—'}</small></div></div>
  <p class="muted">الجهة الجغرافية (4 جهات): ${esc(sec4)} · تصنيف الهيئة ${esc(how)}.</p>
  <div class="section-id" style="margin-top:24px"><b>02</b> REAL ESTATE · 2025 Q1–Q3</div>
  ${tierHtml}
  <div class="fact-grid" style="margin-top:12px">${priceFact('متوسط سعر متر الأرض السكنية', moj && moj.land)}${priceFact('متوسط سعر متر الفلل', moj && moj.villa)}${priceFact('متوسط سعر متر الشقق', moj && moj.apartment)}
  <div class="fact"><label>إجمالي الصفقات</label><b class="${moj ? '' : 'unknown'}">${fmt(moj && moj.deeds)}</b><small>صك بيع · كل الأنواع</small></div></div>
  <p class="muted">المصدر: ${SRC.moj}. المتوسط هو متوسط وزارة العدل المنشور لكل مجموعة، مرجّحًا بعدد الصكوك؛ تنشر الوزارة «NULL» للمجموعات الصغيرة فتُستبعد.</p>
  <div class="section-id" style="margin-top:24px"><b>03</b> COMMERCIAL ACTIVITY · RCRC 2024</div>
  <div class="fact-grid three">
   <div class="fact"><label>محطات وقود</label><b>${fmt(c.fuel || 0)}</b></div><div class="fact"><label>بقالات وأسواق</label><b>${fmt(c.grocery || 0)}</b></div><div class="fact"><label>سوبر/هايبر ماركت</label><b>${fmt(c.supermarket || 0)}</b></div>
   <div class="fact"><label>فنادق وشقق فندقية</label><b>${fmt(c.hotel || 0)}</b></div><div class="fact"><label>مراكز ومجمعات تجارية</label><b>${fmt(c.mall || 0)}</b></div><div class="fact"><label>بنوك</label><b>${fmt(c.bank || 0)}</b></div>
   <div class="fact"><label>مرافق ترفيه</label><b>${fmt(m.entertainment || 0)}</b></div><div class="fact"><label>وحدات سكنية</label><b>${fmt(c.residential_units || 0)}</b></div><div class="fact"><label>إجمالي المسجل</label><b>${fmt(c.total || 0)}</b></div></div>
  <p class="muted">${SRC.rcrc}: «الخدمات التجارية حسب الفئة والبلدية الفرعية والحي 2024» و«الخدمات الترفيهية 2024». قائمة الهيئة لا تشمل كل المحلات.</p>
  <div class="section-id" style="margin-top:24px"><b>04</b> AMENITIES · OSM</div>
  <div class="fact-grid three"><div class="fact"><label>مولات ومراكز تسوق</label><b>${fmt(m.osm_malls || 0)}</b></div><div class="fact"><label>مدارس</label><b>${fmt(m.osm_schools || 0)}</b></div><div class="fact"><label>مستشفيات وعيادات</label><b>${fmt(m.osm_hospitals || 0)}</b></div>
   <div class="fact"><label>حدائق</label><b>${fmt(m.osm_parks || 0)}</b></div><div class="fact"><label>مساجد</label><b>${fmt(m.osm_mosques || 0)}</b></div><div class="fact"><label>محطات مترو</label><b>${fmt((m.metro_in || []).length)}</b></div></div>
  <p class="muted">${SRC.osm}: تغطية تطوعية غير مكتملة؛ استخدمها للمقارنة بين الأحياء لا كعدد نهائي.</p>
  <div class="section-id" style="margin-top:24px"><b>05</b> ACCESS</div>
  <div style="margin-bottom:8px">${roads}</div>${metro}
  <div class="section-id" style="margin-top:24px"><b>06</b> MARKETING READ</div>
  ${ins.length ? '<ul class="insights">' + ins.map(t => `<li>${esc(t)}</li>`).join('') + '</ul>' : '<p class="muted">لا تبرز مؤشرات استثنائية لهذا الحي مقارنة بوسيط الأحياء.</p>'}
  <p class="muted" style="margin-top:10px">قراءة آلية من الأرقام أعلاه، وليست تقديرًا للدخل أو للجمهور.</p>
  ${validStats && (optional(row.saudi_pct) !== null || optional(row.commercial_count) !== null) ? `<div class="fact-status">بيانات مستوردة: سعوديون ${optional(row.saudi_pct) ?? '—'}% · غير سعوديين ${optional(row.non_saudi_pct) ?? '—'}% · منشآت ${fmt(optional(row.commercial_count))} — المصدر: ${esc(row.source)} (${esc(row.year)}).</div>` : ''}
  <div class="section-id" style="margin-top:24px"><b>07</b> DATA PROVENANCE</div>
  <ul class="src-list"><li>الحدود والمرافق: ${SRC.osm}</li><li>الطرق: ${SRC.osm} (Geofabrik، 11 أكتوبر 2026)</li><li>الجهات، الخدمات التجارية والترفيهية، المترو: ${SRC.rcrc}</li><li>الصفقات العقارية: ${SRC.moj}</li>${pop !== null ? '<li>السكان: ' + esc(row.source) + '</li>' : ''}</ul>
  <a class="detail-link" target="_blank" rel="noopener noreferrer" href="https://rmp.alriyadh.gov.sa/ar/gis-portal">التحقق من بوابة أمانة الرياض المكانية ↗</a>`;
  $('details').classList.add('open'); $('details').scrollTop = 0;
}
function format(n){ return fmt(n); }
function optional(v){ const n = Number(v); return v !== null && v !== undefined && String(v).trim() !== '' && Number.isFinite(n) && n >= 0 ? n : null; }
function searchSuggestions(q){ const box = $('results'); if (!q.trim()){ box.classList.add('hidden'); return; } q = cleanName(q); const hit = districts.filter(d => d.name.includes(q)).slice(0, 13); box.innerHTML = ''; if (!hit.length){ box.classList.add('hidden'); return; } for (const d of hit){ const b = document.createElement('button'); b.className = 'suggestion'; b.type = 'button'; const a = document.createElement('span'); a.textContent = d.name; const n = document.createElement('small'); n.textContent = (metrics(d.name).sector || '') + ' · ' + d.area.toFixed(1) + ' km²'; b.append(a, n); b.onclick = () => { $('search').value = d.name; box.classList.add('hidden'); choose(d.name, true); showDetails(d.name); }; box.append(b); } box.classList.remove('hidden'); }
function buildQuick(){ const box = $('quick'); box.replaceChildren(); quickNames.filter(n => byName.has(n)).forEach(name => { const b = document.createElement('button'); b.type = 'button'; b.textContent = name; b.dataset.name = name; b.onclick = () => { choose(name, true); if (window.innerWidth < 760) showDetails(name); }; box.append(b); }); }

// ---------- zoom, pan, pinch, tap ----------
function zoom(factor, anchor){ const vb = viewBox; if (!vb) return; anchor = anchor || {x: vb.x + vb.w / 2, y: vb.y + vb.h / 2}; const newW = Math.max(40, Math.min(1500, vb.w * factor)), ratio = newW / vb.w, newH = vb.h * ratio; setBox([anchor.x - (anchor.x - vb.x) * ratio, anchor.y - (anchor.y - vb.y) * ratio, newW, newH]); }
function screenWorld(evt){ const svg = $('mapSvg'), p = svg.createSVGPoint(); p.x = evt.clientX; p.y = evt.clientY; return p.matrixTransform(svg.getScreenCTM().inverse()); }
function initEvents(){
  const svg = $('mapSvg'), canvas = $('mapContainer'), pts = new Map(); let pan = null, pinch = null, lastTap = {t: 0, name: null};
  const local = e => { const r = canvas.getBoundingClientRect(); return {x: e.clientX - r.left, y: e.clientY - r.top}; };
  const worldAt = (p, vb) => { const r = svg.getBoundingClientRect(), k = Math.min(r.width / vb.w, r.height / vb.h); return {x: vb.x + (p.x - (r.width - vb.w * k) / 2) / k, y: vb.y + (p.y - (r.height - vb.h * k) / 2) / k}; };
  const startPan = e => { pan = {x: e.clientX, y: e.clientY, view: {...viewBox}, moved: false}; };
  canvas.addEventListener('pointerdown', e => {
    if (e.pointerType === 'mouse' && e.button !== 0) return; pts.set(e.pointerId, local(e));
    if (pts.size === 1){ startPan(e); hasMoved = false; }
    if (pts.size === 2){ const [a, b] = [...pts.values()]; const mid = {x: (a.x + b.x) / 2, y: (a.y + b.y) / 2}; pinch = {d: Math.hypot(a.x - b.x, a.y - b.y) || 1, view: {...viewBox}, anchor: worldAt(mid, viewBox)}; pan = null; hasMoved = true; }
  });
  canvas.addEventListener('pointermove', e => {
    if (!pts.has(e.pointerId)) return; pts.set(e.pointerId, local(e));
    if (pinch && pts.size >= 2){
      const [a, b] = [...pts.values()]; const mid = {x: (a.x + b.x) / 2, y: (a.y + b.y) / 2}, d = Math.hypot(a.x - b.x, a.y - b.y) || 1;
      const v = pinch.view, w = Math.max(40, Math.min(1500, v.w * pinch.d / d)), h = v.h * w / v.w; const r = svg.getBoundingClientRect(), k = Math.min(r.width / w, r.height / h);
      setBox([pinch.anchor.x - (mid.x - (r.width - w * k) / 2) / k, pinch.anchor.y - (mid.y - (r.height - h * k) / 2) / k, w, h]); return;
    }
    if (!pan) return; const dx = e.clientX - pan.x, dy = e.clientY - pan.y;
    if (!pan.moved && Math.hypot(dx, dy) < 6) return;
    if (!pan.moved){ pan.moved = true; hasMoved = true; canvas.classList.add('grabbing'); try { canvas.setPointerCapture(e.pointerId); } catch {} }
    const r = svg.getBoundingClientRect(), k = Math.max(pan.view.w / r.width, pan.view.h / r.height); setBox([pan.view.x - dx * k, pan.view.y - dy * k, pan.view.w, pan.view.h]);
  });
  const end = e => {
    if (!pts.has(e.pointerId)) return; pts.delete(e.pointerId); canvas.classList.remove('grabbing');
    if (pts.size < 2) pinch = null;
    if (pts.size === 1){ const [id] = pts.keys(); const p = pts.get(id), r = canvas.getBoundingClientRect(); pan = {x: p.x + r.left, y: p.y + r.top, view: {...viewBox}, moved: true}; return; }
    if (pts.size === 0){
      const tapped = e.type === 'pointerup' && !hasMoved; pan = null;
      if (tapped){
        const el = document.elementFromPoint(e.clientX, e.clientY), path = el && el.closest && el.closest('.district-path');
        if (path){ const name = path.dataset.name, now = Date.now(); choose(name); if (lastTap.name === name && now - lastTap.t < 420){ showDetails(name); lastTap = {t: 0, name: null}; } else lastTap = {t: now, name}; }
      }
      setTimeout(() => { hasMoved = false; }, 60);
    }
  };
  canvas.addEventListener('pointerup', end); canvas.addEventListener('pointercancel', end);
  svg.addEventListener('wheel', e => { e.preventDefault(); zoom(e.deltaY > 0 ? 1.15 : .87, screenWorld(e)); }, {passive: false});
  svg.addEventListener('dblclick', e => e.preventDefault());
  $('plus').onclick = () => zoom(.77); $('minus').onclick = () => zoom(1.27); $('reset').onclick = fitCore; $('allBtn').onclick = fitAll;
  $('clearBtn').onclick = () => { selected = null; svgPaths.forEach(p => p.classList.remove('is-selected')); $('selectedName').textContent = 'لم يتم تحديد حي'; $('selectedMeta').textContent = 'انقر على إحدى المساحات في الخريطة'; $('detailsBtn').disabled = true; $('mobileDetailBtn').classList.add('hidden'); $('details').classList.remove('open'); focusRoad(null); };
  $('detailsBtn').onclick = () => selected && showDetails(selected); $('mobileDetailBtn').onclick = () => selected && showDetails(selected); $('closeDetails').onclick = () => $('details').classList.remove('open');
  $('search').oninput = e => searchSuggestions(e.target.value); $('search').onkeydown = e => { if (e.key === 'Escape') $('results').classList.add('hidden'); };
  document.addEventListener('click', e => { if (!e.target.closest('.searchbox')) $('results').classList.add('hidden'); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') $('details').classList.remove('open'); });
  window.addEventListener('resize', refreshLabels); setTimeout(refreshLabels, 250);
  $('layersBtn').onclick = () => { const c = $('layers').classList.toggle('collapsed'); $('layersBtn').setAttribute('aria-expanded', String(!c)); };
  $('lyrNames').onchange = e => { state.names = e.target.checked; applyLayers(); };
  $('lyrSectors').onchange = e => { state.sectors = e.target.checked; applySectors(); };
  $('lyrRoads').onchange = e => { state.roads = e.target.checked; if (!state.roads) focusRoad(null); applyLayers(); };
  $('lyrMetro').onchange = e => { state.metro = e.target.checked; applyLayers(); };
  document.querySelectorAll('#sectorMode button').forEach(b => b.onclick = () => { state.sectorMode = b.dataset.mode; document.querySelectorAll('#sectorMode button').forEach(x => x.classList.toggle('active', x === b)); applySectors(); });
  $('sourcesLink').onclick = e => { e.preventDefault(); notify(selected ? 'المصادر في أسفل ملف الحي' : 'اختر حيًا لعرض ملفه ومصادره'); if (selected) showDetails(selected); };
  $('importCsv').onchange = async e => { const f = e.target.files?.[0]; if (!f) return; try { const rows = csvToObjects(await f.text()); const next = new Map(); let ignored = 0; for (const row of rows){ const name = cleanName(row.name_ar || row.name || ''); if (!byName.has(name) || !row.source || !row.year){ ignored++; continue; } const sa = optional(row.saudi_pct), ex = optional(row.non_saudi_pct); if (sa !== null && ex !== null && Math.abs(sa + ex - 100) > 2){ ignored++; continue; } next.set(name, row); } for (const [k, v] of next) stats.set(k, v); $('dataStatus').textContent = 'تم ربط ' + next.size + ' أحياء ببيانات الإحصاءات؛ ' + ignored + ' صف مستبعد.'; notify('تم تحميل ' + next.size + ' سجلًا موثق المصدر'); if (selected && $('details').classList.contains('open')) showDetails(selected); } catch (err){ notify('تعذر قراءة CSV: ' + err.message); } };
  $('exportBtn').onclick = exportSelected;
}
function csvToObjects(raw){ const lines = []; let fields = [], cell = '', quoted = false; raw = raw.replace(/^﻿/, ''); for (let i = 0; i < raw.length; i++){ const c = raw[i]; if (c === '"'){ if (quoted && raw[i + 1] === '"'){ cell += '"'; i++; } else quoted = !quoted; } else if (c === ',' && !quoted){ fields.push(cell); cell = ''; } else if ((c === '\n' || c === '\r') && !quoted){ if (c === '\r' && raw[i + 1] === '\n') i++; fields.push(cell); if (fields.some(x => x !== '')) lines.push(fields); fields = []; cell = ''; } else cell += c; } fields.push(cell); if (fields.some(x => x !== '')) lines.push(fields); const header = (lines.shift() || []).map(x => x.trim()); if (!header.includes('name_ar') && !header.includes('name')) throw Error('الملف يحتاج عمود name_ar'); return lines.map(line => Object.fromEntries(header.map((h, i) => [h, (line[i] || '').trim()]))); }
function exportSelected(){
  if (!selected){ notify('اختر حيًا أولًا'); return; }
  const d = byName.get(selected), m = metrics(selected), c = m.rcrc || {}, st = stats.get(selected) || {}, moj = m.moj || {};
  const cols = {name_ar: d.name, sector_rcrc: m.sector, sub_municipality: m.submun, sector_geo4: m.sector4, area_km2: d.area.toFixed(2), km_to_qasr_alhukm: m.center_km,
    population_estimate: st.population_estimate || '', population_source: st.source || '', deeds_2025_q1_q3: moj.deeds ?? '', land_res_sar_m2: moj.land?.ppm ?? '', villa_sar_m2: moj.villa?.ppm ?? '', apartment_sar_m2: moj.apartment?.ppm ?? '',
    land_price_tier_0_3: m.tier ?? '', rcrc_commercial_total: c.total || 0, fuel: c.fuel || 0, grocery_markets: c.grocery || 0, super_hyper: c.supermarket || 0, hotels: c.hotel || 0, malls_complexes: c.mall || 0, banks: c.bank || 0,
    entertainment: m.entertainment || 0, osm_malls: m.osm_malls || 0, osm_schools: m.osm_schools || 0, osm_hospitals: m.osm_hospitals || 0, osm_parks: m.osm_parks || 0, osm_mosques: m.osm_mosques || 0,
    main_roads: (m.roads || []).map(k => ROAD_BY_KEY[k].ar).join(' | '), metro_in_district: (m.metro_in || []).join(' | '), nearest_metro: m.metro_near ? m.metro_near.name + ' (' + m.metro_near.line + ') ' + m.metro_near.km + ' km' : ''};
  const q = s => '"' + String(s ?? '').replace(/"/g, '""') + '"'; const csv = Object.keys(cols).join(',') + '\n' + Object.values(cols).map(q).join(',') + '\n';
  const url = URL.createObjectURL(new Blob(['﻿' + csv], {type: 'text/csv;charset=utf-8'})); const a = document.createElement('a'); a.href = url; a.download = 'riyadh-' + d.name + '.csv'; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1500);
}
// Optional 2021 population estimates from a public ArcGIS layer (not an official census).
function fetchPopulationLayer(){
  const uri = 'https://services7.arcgis.com/co15Y7Q02mBEZqnK/ArcGIS/rest/services/Riyadh_Metro_WebMapv2_WFL1/FeatureServer/0/query?where=1%3D1&outFields=NEIGHBORHANAME%2Csum_population_per_point2021&returnGeometry=false&f=json';
  return fetch(uri, {cache: 'force-cache'}).then(r => { if (!r.ok) throw Error('population unavailable'); return r.json(); }).then(obj => {
    if (!Array.isArray(obj.features)) return; let count = 0;
    for (const feat of obj.features){ const a = feat.attributes || {}, name = cleanName(a.NEIGHBORHANAME), value = optional(a.sum_population_per_point2021); if (!name || !byName.has(name) || value === null || value < 10 || value > 1000000 || stats.has(name)) continue; stats.set(name, {population_estimate: Math.round(value), source: 'ArcGIS open layer / Riyadh Metro WebMapv2', year: '2021', method: 'تجميع تقديرات نقاط سكانية؛ ليست بيانات تعداد'}); count++; }
    if (count){ $('dataStatus').textContent = 'تقديرات سكان 2021 متاحة لـ ' + count + ' حيًا (مصدر غير رسمي).'; if (selected && $('details').classList.contains('open')) showDetails(selected); }
  });
}
function init(){
  districts = GEO.map(decorate); renderGrid(); renderDistricts(); renderMetro(); renderRoads(); buildRoadLegend(); buildQuick(); initEvents();
  if (window.innerWidth < 760) $('layers').classList.add('collapsed');
  fitCore(); applyLayers(); $('mapStatus').textContent = 'OSM GEOMETRY / RCRC + MOJ OPEN DATA';
  fetchPopulationLayer().catch(() => {});
}
init();
</script>
</body></html>'''

html=html.replace('__GEO__',json.dumps(geo,ensure_ascii=False,separators=(',',':'))).replace('__ENR__',json.dumps(enr,ensure_ascii=False,separators=(',',':')))
logo_file=root/'plan-c-mark.svg'
if logo_file.exists():
    logo_svg=logo_file.read_text(encoding='utf-8')
    html=html.replace('<div class="logo-icon" aria-hidden="true">C</div>', '<div class="logo-icon" aria-hidden="true">'+logo_svg+'</div>')
(root/'index.html').write_text(html,encoding='utf-8')
rows=[g['n'] for g in geo]
with (root/'neighborhood_stats_template.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['name_ar','population_estimate','saudi_pct','non_saudi_pct','commercial_count','source','year','method']);w.writerows([[name,'','','','','','',''] for name in rows])
print('created index',len(html),'chars; csv rows',len(rows))
