/*! Messibot: the Messify website chat assistant (scripted, no AI, no server).
 *
 * Install: add this line before </body> on every page (path relative to the page):
 *   <script src="/assets/js/messibot.js" defer></script>
 * Open it from any button or link:  <a href="#" data-messibot="catering">Get a quote</a>   (or "meals")
 * From code:  Messibot.open("meals" | "catering")   Messibot.close()
 *
 * Images come from /assets/img/ next to this file. Leads are emailed to info@messify.me through FormSubmit
 * (the same service as the site's forms). WhatsApp taps fire a Meta Pixel "Lead" and a GA4 "generate_lead" event
 * when those tags are on the page.
 * Edit prices, areas and answers in CONFIG and FAQ below.
 */
(function () {
"use strict";
if (window.Messibot) return;
const ASSETS = ((document.currentScript && document.currentScript.src) || "/assets/js/messibot.js").replace(/js\/messibot\.js.*$/, "");
const IMG = ASSETS + "img/";
const FORM_ENDPOINT = "https://formsubmit.co/ajax/info@messify.me";

const host = document.createElement("div");
host.id = "messibot";
host.dataset.mode = "meals";
const root = host.attachShadow({ mode: "open" });
root.innerHTML = "<style>" + ":host{\n  --bg:#FAF6EE; --surface:#FFFFFF; --surface-2:#F2ECDF; --fg:#17181C; --muted:#67625A; --line:#E6DECE; --line-strong:#CFC5B1;\n  --accent:#38B6FF; --accent-ink:#0A6CA8; --accent-soft:#E2F2FC; --btn-bg:#38B6FF; --btn-bg-hover:#1FA6F3; --btn-fg:#081A2A;\n  --mark:#38B6FF; --bubble-me:#D7EFFD; --bubble-me-fg:#0B2236; --warn:#8A4B06; --warn-bg:#FBEBD3; --wa:#1F9D55; --wa-hover:#178A49;\n  --font-body:\"Poppins\",ui-sans-serif,system-ui,-apple-system,\"Segoe UI\",Roboto,Arial,sans-serif;\n  --font-serif:\"Cormorant Garamond\",\"Iowan Old Style\",\"Palatino Linotype\",Georgia,serif;\n  --font-display:var(--font-body); --display-weight:600; --display-tracking:-0.025em; --display-scale:1;\n  --ease:cubic-bezier(.2,.7,.2,1);\n  \n}\n:host([data-mode=\"catering\"]){\n  --bg:#120F0D; --surface:#1C1714; --surface-2:#251F1A; --fg:#F3ECE2; --muted:#B3A797; --line:#2F2721; --line-strong:#4A3D33;\n  --accent:#C49A6C; --accent-ink:#D8B48A; --accent-soft:#2A2119; --btn-bg:#F3ECE2; --btn-bg-hover:#FFFFFF; --btn-fg:#120F0D;\n  --mark:#F3ECE2; --bubble-me:#2E251E; --bubble-me-fg:#F3ECE2; --warn:#F2C08A; --warn-bg:#2E2216;\n  --font-display:var(--font-serif); --display-weight:500; --display-tracking:-0.01em; --display-scale:1.22;\n  \n}\n\n:host{all:initial}\n*{box-sizing:border-box}\nbutton{font:inherit}\n.wrap{font-family:var(--font-body);font-size:14px;line-height:1.55;color:var(--fg);-webkit-font-smoothing:antialiased}\n.launcher{position:fixed;right:20px;bottom:calc(20px + env(safe-area-inset-bottom,0px));z-index:2147483000;display:flex;align-items:center;gap:10px;\n  padding:7px 18px 7px 7px;border-radius:999px;border:1px solid #E6DECE;background:#FFFFFF;color:#17181C;cursor:pointer;\n  font:600 14px/1 \"Poppins\",system-ui,-apple-system,\"Segoe UI\",sans-serif;box-shadow:0 14px 34px -14px rgba(23,24,28,.45);transition:transform .25s var(--ease),box-shadow .25s}\n.launcher:hover{transform:translateY(-2px);box-shadow:0 18px 40px -14px rgba(23,24,28,.5)}\n.launcher img{width:40px;height:40px;border-radius:50%;background:#F2ECDF;padding:3px}\n.launcher .x{display:none;width:40px;height:40px;border-radius:50%;background:#17181C;color:#fff;place-items:center}\n.launcher.open{padding:7px}\n.launcher.open img,.launcher.open .lbl{display:none}\n.launcher.open .x{display:grid}\n.launcher:focus-visible{outline:3px solid #38B6FF;outline-offset:3px}\n.teaser{position:fixed;right:20px;bottom:calc(84px + env(safe-area-inset-bottom,0px));z-index:2147483000;max-width:260px;padding:12px 34px 12px 14px;border-radius:18px 18px 6px 18px;\n  background:#FFFFFF;color:#17181C;border:1px solid #E6DECE;box-shadow:0 14px 34px -16px rgba(23,24,28,.45);font:500 13px/1.45 \"Poppins\",system-ui,sans-serif;cursor:pointer;animation:pop .45s var(--ease) both}\n.teaser b{font-weight:600}\n.teaser button{position:absolute;top:6px;right:6px;width:24px;height:24px;border:0;border-radius:50%;background:#F2ECDF;color:#67625A;cursor:pointer;font-size:14px;line-height:1}\n@keyframes pop{from{opacity:0;transform:translateY(8px) scale(.96)}}\n.panel{position:fixed;right:20px;bottom:calc(88px + env(safe-area-inset-bottom,0px));z-index:2147483000;width:400px;height:min(720px,calc(100vh - 120px));height:min(720px,calc(100dvh - 120px));\n  border-radius:28px;overflow:hidden;border:1px solid var(--line);box-shadow:0 30px 80px -30px rgba(23,24,28,.55);\n  transform-origin:bottom right;transition:opacity .3s var(--ease),transform .35s var(--ease)}\n.panel[hidden]{display:block!important;opacity:0;transform:translateY(12px) scale(.96);pointer-events:none;visibility:hidden}\n.closebtn{display:none}\n@media (max-width:560px){\n  .panel{inset:0;width:auto;height:100%;border-radius:0;border:0}\n  .launcher.open{display:none}\n  .closebtn{display:grid}\n  .launcher .lbl{display:none}\n  .launcher{padding:7px}\n  .teaser{bottom:calc(76px + env(safe-area-inset-bottom,0px))}\n}\n.hbtns{display:flex;gap:6px;justify-self:end}\n.eyebrow{font-size:.72rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-ink);margin:0}\n.chead{grid-template-columns:40px 1fr auto}\n/* ---------- chat widget ---------- */\n.chat{position:relative;isolation:isolate;background:var(--bg);display:flex;flex-direction:column;height:100%;overflow:hidden;transition:background-color .6s}\n\n.chead{display:grid;grid-template-columns:40px 1fr 40px;align-items:center;gap:10px;padding:12px 14px;background:var(--surface);border-bottom:1px solid var(--line);transition:background-color .6s,border-color .6s}\n.chead .av-lg{width:38px;height:38px;border-radius:50%;background:var(--surface-2);padding:3px}\n.brand{text-align:center;min-width:0}\n.brand .t{font-weight:600;font-size:.78rem;letter-spacing:.36em;padding-left:.36em;line-height:1.3}\n.brand .s{font-size:.7rem;color:var(--muted);display:flex;align-items:center;justify-content:center;gap:5px;white-space:nowrap}\n.dot{width:6px;height:6px;border-radius:50%;background:#2BC46B}\n.iconbtn{width:38px;height:38px;border-radius:12px;border:1px solid var(--line);background:transparent;color:var(--fg);cursor:pointer;display:grid;place-items:center;justify-self:end}\n.iconbtn:hover{border-color:var(--accent);color:var(--accent-ink)}\n\n/* topic switch, same as the site's top bar */\n.switch{position:relative;display:grid;grid-template-columns:1fr 1fr;padding:4px;margin:10px 14px 0;border-radius:999px;background:var(--surface-2);border:1px solid var(--line);flex-shrink:0;transition:background-color .6s,border-color .6s}\n.switch button{position:relative;z-index:1;border:0;background:none;cursor:pointer;min-height:36px;border-radius:999px;font-size:.82rem;font-weight:600;color:var(--muted);transition:color .3s}\n.switch button[aria-pressed=\"true\"]{color:var(--btn-fg)}\n.switch__thumb{position:absolute;top:4px;bottom:4px;left:4px;width:calc(50% - 4px);border-radius:999px;background:var(--btn-bg);transition:transform .45s var(--ease),background-color .6s}\n:host([data-mode=\"catering\"]) .switch__thumb{transform:translateX(100%)}\n\n.switch[hidden]{display:none}\n.msgs{flex:1;overflow-y:auto;padding:14px 14px 16px;display:flex;flex-direction:column;gap:10px;scroll-behavior:smooth}\n\n/* doors: the opening choice */\n.gatehead{display:flex;flex-direction:column;align-items:center;text-align:center;gap:4px;padding:8px 6px 4px}\n.gatehead img{width:56px;height:56px;border-radius:50%;background:var(--surface);padding:4px;box-shadow:0 0 0 1px var(--line),0 12px 26px -14px rgba(23,24,28,.4)}\n.gatehead h3{font-size:1.25rem;font-weight:600;letter-spacing:-.02em;margin-top:6px}\n.gatehead p{margin:0;color:var(--muted);font-size:.86rem}\n.doors{display:flex;gap:8px;height:360px;flex-shrink:0}\n.door{position:relative;flex:1 1 0;min-width:0;border:0;padding:0;border-radius:22px;overflow:hidden;cursor:pointer;text-align:left;color:#fff;display:flex;align-items:flex-end;\n  background:#0D0B0A;transition:flex-grow .7s var(--ease)}\n.door img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease)}\n.door__shade{position:absolute;inset:0}\n.door--meals .door__shade{background:linear-gradient(to top,rgba(6,14,24,.9) 0%,rgba(6,14,24,.5) 45%,rgba(6,14,24,.05) 80%)}\n.door--catering .door__shade{background:linear-gradient(to top,rgba(14,9,6,.94) 0%,rgba(14,9,6,.58) 48%,rgba(14,9,6,.12) 82%)}\n.door__copy{position:relative;padding:16px 14px 16px;display:flex;flex-direction:column;align-items:flex-start;gap:7px;width:100%}\n.door__tag{display:inline-flex;align-items:center;gap:7px;font-size:.6rem;font-weight:600;letter-spacing:.16em;text-transform:uppercase}\n.door__tag::before{content:\"\";width:16px;height:2px;border-radius:2px;background:currentColor}\n.door--meals .door__tag{color:#7FD0FF}\n.door--catering .door__tag{color:#D8B48A}\n.door__title{line-height:.95}\n.door--meals .door__title{font-family:var(--font-body);font-weight:600;letter-spacing:-.035em;font-size:1.65rem}\n.door--catering .door__title{font-family:var(--font-serif);font-style:italic;font-weight:500;font-size:2.05rem}\n.door__text{font-size:.74rem;line-height:1.4;color:rgba(255,255,255,.86)}\n.door__cta{display:inline-flex;align-items:center;gap:8px;min-height:34px;padding:0 13px;border-radius:999px;font-weight:600;font-size:.76rem;margin-top:3px;transition:gap .25s var(--ease)}\n.door__cta svg{width:15px;height:15px}\n.door--meals .door__cta{background:#38B6FF;color:#081A2A}\n.door--catering .door__cta{color:#F3ECE2;box-shadow:inset 0 0 0 1px rgba(243,236,226,.6)}\n.door:hover .door__cta,.door:focus-visible .door__cta{gap:13px}\n.door:hover img{transform:scale(1.05)}\n.door:focus-visible{outline:3px solid var(--accent);outline-offset:2px}\n@media (hover:hover) and (pointer:fine){ .doors:hover .door{flex-grow:.8} .doors .door:hover{flex-grow:1.3} }\n.gatefoot{display:flex;justify-content:center;gap:16px;color:var(--muted);font-size:.74rem;padding-top:2px}\n.gatefoot b{color:var(--fg);font-weight:600}\n\n/* conversation intro */\n.intro{display:flex;flex-direction:column;align-items:flex-start;gap:4px;padding:6px 4px 4px}\n.intro h3{font-family:var(--font-display);font-weight:var(--display-weight);letter-spacing:var(--display-tracking);font-size:calc(1.55rem * var(--display-scale));line-height:1.05}\n:host([data-mode=\"catering\"]) .intro h3 em{font-style:italic}\n.intro h3 em{font-style:normal;color:var(--accent-ink)}\n.facts{display:flex;gap:0;margin-top:8px;border-top:1px solid var(--line);width:100%}\n.facts div{flex:1;padding:8px 8px 0 0;min-width:0}\n.facts div + div{padding-left:10px;border-left:1px solid var(--line)}\n.facts b{display:block;font-family:var(--font-display);font-weight:var(--display-weight);font-size:calc(.98rem * var(--display-scale));line-height:1.1;font-variant-numeric:tabular-nums}\n.facts span{display:block;color:var(--muted);font-size:.68rem;line-height:1.3;margin-top:2px}\n\n.row{display:flex;align-items:flex-end;gap:8px;max-width:92%;align-self:flex-start}\n.av{width:28px;height:28px;border-radius:50%;flex-shrink:0;background:var(--surface);padding:2px;box-shadow:0 0 0 1px var(--line)}\n.b{max-width:86%;padding:10px 14px;border-radius:18px;white-space:pre-wrap;overflow-wrap:anywhere;font-size:.9rem;line-height:1.5;transition:background-color .6s}\n.b.bot{background:var(--surface);border:1px solid var(--line);border-bottom-left-radius:6px}\n.row .b{max-width:100%}\n.b.me{align-self:flex-end;background:var(--bubble-me);color:var(--bubble-me-fg);border-bottom-right-radius:6px}\n.typing{display:flex;gap:4px;padding:14px}\n.typing i{width:7px;height:7px;border-radius:50%;background:var(--muted);animation:bl 1s infinite}\n.typing i:nth-child(2){animation-delay:.15s}.typing i:nth-child(3){animation-delay:.3s}\n@keyframes bl{0%,100%{opacity:.25}50%{opacity:1}}\n@keyframes rise{from{opacity:0;transform:translateY(10px)}}\n.row,.b.me,.chips,.handoff,.glimpse,.intro{animation:rise .45s var(--ease) both}\n\n.chips{display:flex;flex-wrap:wrap;gap:6px;align-self:flex-start;max-width:100%;padding-left:36px}\n.chip{border:1px solid var(--line-strong);background:transparent;color:var(--fg);border-radius:999px;min-height:36px;padding:0 14px;font-size:.82rem;font-weight:500;cursor:pointer;transition:background-color .2s,border-color .2s}\n.chip:hover{background:var(--accent-soft);border-color:var(--accent)}\n\n/* photo strip */\n.glimpse{display:grid;gap:8px;margin-top:6px;flex-shrink:0}\n.glimpse header{display:flex;justify-content:space-between;align-items:baseline;padding:0 2px}\n.glimpse header small{font-size:.62rem;letter-spacing:.26em;text-transform:uppercase;color:var(--muted);font-weight:600}\n.glimpse header a{font-size:.72rem;color:var(--muted);text-underline-offset:3px}\n.glimpse header a:hover{color:var(--accent-ink)}\n.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:4px;border-radius:16px;overflow:hidden}\n.tile{position:relative;padding:0;border:0;aspect-ratio:3/4;overflow:hidden;cursor:zoom-in;background:var(--surface-2)}\n.tile img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s var(--ease)}\n.tile:hover img{transform:scale(1.06)}\n.tile span{position:absolute;inset:auto 0 0 0;padding:18px 6px 6px;font-size:.62rem;font-weight:600;color:#fff;text-align:left;line-height:1.2;background:linear-gradient(transparent,rgba(10,8,6,.72));opacity:0;transition:opacity .25s}\n.tile:hover span,.tile:focus-visible span{opacity:1}\n.tile:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}\n\n/* handoff */\n.handoff{align-self:stretch;margin-left:36px;background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:16px;display:grid;gap:12px}\n.handoff small.k{font-size:.62rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-ink)}\n.brief{margin:0;font-family:var(--font-serif);font-size:1.4rem;line-height:1.18;text-wrap:balance}\n.brief em{font-style:italic;color:var(--accent-ink)}\n.handoff pre{margin:0;white-space:pre-wrap;font-family:var(--font-body);font-size:.78rem;background:var(--surface-2);border-radius:12px;padding:10px 12px;color:var(--fg)}\n.wa{display:flex;align-items:center;justify-content:center;gap:8px;background:var(--wa);color:#fff;font-weight:600;text-decoration:none;border-radius:999px;min-height:46px;font-size:.9rem}\n.wa:hover{background:var(--wa-hover)}\n.handoff .fine{color:var(--muted);font-size:.72rem}\n.handoff .fine a{color:var(--fg)}\n\n/* composer */\n.cfoot{margin:6px 12px calc(12px + env(safe-area-inset-bottom,0px));display:grid;gap:8px;background:var(--surface);border:1px solid var(--line);border-radius:22px;padding:12px 12px 10px 16px;\n  box-shadow:0 14px 30px -22px rgba(23,24,28,.45);transition:background-color .6s,border-color .6s}\n.cfoot:focus-within{border-color:var(--accent)}\n.cfoot input{width:100%;min-width:0;border:0;background:transparent;color:var(--fg);padding:4px 0;font:inherit;font-size:.95rem}\n.cfoot input::placeholder{color:var(--muted)}\n.cfoot input:focus{outline:none}\n.cbar{display:flex;align-items:center;gap:6px;flex-wrap:wrap}\n.qa{border:1px solid var(--line-strong);background:transparent;color:var(--fg);border-radius:999px;min-height:32px;padding:0 12px;font-size:.78rem;font-weight:500;cursor:pointer}\n.qa:hover{background:var(--accent-soft)}\n.send{margin-left:auto;width:40px;height:40px;flex-shrink:0;border-radius:50%;border:0;background:var(--btn-bg);color:var(--btn-fg);cursor:pointer;display:grid;place-items:center;transition:background-color .3s}\n.send:hover{background:var(--btn-bg-hover)}\n.send:disabled{opacity:.45;cursor:default}\n.err{font-size:.76rem;color:var(--warn);align-self:center;text-align:center}\n\n/* photo viewer */\n.viewer{position:absolute;inset:0;z-index:20;background:rgba(10,8,6,.88);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:20px}\n.viewer img{max-width:100%;max-height:70%;border-radius:18px;object-fit:contain}\n.viewer p{margin:0;color:#F3ECE2;font-family:var(--font-display);font-weight:var(--display-weight);font-size:calc(1rem * var(--display-scale))}\n.viewer nav{display:flex;gap:8px}\n.viewer button{border:0;border-radius:999px;min-height:36px;padding:0 14px;font-size:.8rem;cursor:pointer;background:rgba(255,255,255,.14);color:#fff}\n.viewer button.close{background:var(--btn-bg);color:var(--btn-fg);font-weight:600}\n:focus-visible{outline:3px solid var(--accent);outline-offset:2px}\n.switch[hidden]{display:none}\n@media (prefers-reduced-motion:reduce){\n  .chat,.switch__thumb,.door,.door img,.tile img{transition:none}\n  .row,.b.me,.chips,.handoff,.glimpse,.intro{animation:none}\n  .typing i{animation:none;opacity:.6}\n}\n" + "</style>" + `
<div class="wrap">
  <div class="teaser" id="teaser" hidden role="button" tabindex="0"><b>Hi, I'm Messibot.</b> Questions about meal plans or catering? Ask me.<button type="button" id="teaser-x" aria-label="Dismiss">×</button></div>
  <section class="panel" id="panel" hidden role="dialog" aria-label="Chat with Messibot">
    <section class="chat" aria-label="Messibot chat">
      <div class="chead">
        <img class="av-lg" src="${IMG}coin.webp" alt="">
        <div class="brand"><div class="t">MESSIBOT</div><div class="s"><span class="dot"></span>by messify. · replies instantly</div></div>
        <div class="hbtns">
          <button class="iconbtn" id="restart" type="button" aria-label="Start over"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg></button>
          <button class="iconbtn closebtn" id="close" type="button" aria-label="Close chat"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button>
        </div>
      </div>
      <nav class="switch" id="switch" aria-label="Choose a topic" hidden>
        <span class="switch__thumb" aria-hidden="true"></span>
        <button type="button" data-go="meals" aria-pressed="true">Meal plans</button>
        <button type="button" data-go="catering" aria-pressed="false">Catering</button>
      </nav>
      <div class="msgs" id="msgs" aria-live="polite"></div>
      <form class="cfoot" id="form" autocomplete="off">
        <input id="box" placeholder="Ask about meal plans or catering…" aria-label="Your message" maxlength="600">
        <div class="cbar"><button type="button" class="qa" id="qa-1">See plans</button><button type="button" class="qa" id="qa-wa">Chat on WhatsApp</button>
        <button class="send" id="send" aria-label="Send"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M6 11l6-6 6 6"/></svg></button></div>
      </form>
    </section>
  </section>
  <button class="launcher" id="launcher" type="button" aria-expanded="false" aria-controls="panel">
    <img src="${IMG}coin.webp" alt=""><span class="lbl">Chat with Messibot</span>
    <span class="x" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></span>
  </button>
</div>`;
(document.body || document.documentElement).appendChild(host);
const $ = s => root.querySelector(s);
const AV = IMG + "coin.webp";
const msgs = $("#msgs"), box = $("#box"), sendBtn = $("#send");

/* ===== Messify config: edit here ===== */
const CONFIG = {
  whatsapp: "971502513033",
  whatsappDisplay: "+971 50 251 3033",
  email: "info@messify.me",
  areas: ["Academic City", "Dubai Silicon Oasis", "International City", "Dubai Festival City"],
  emirates: ["Dubai", "Sharjah", "Ajman", "Abu Dhabi"],
  daysPerWeek: 7, daysPerMonth: 26,
  plans: [
    { mpd: 1, weekly: 215, weeklyWas: 300,  monthly: 715,  monthlyWas: 1000 },
    { mpd: 2, weekly: 415, weeklyWas: 600,  monthly: 1400, monthlyWas: 2000 },
    { mpd: 3, weekly: 610, weeklyWas: 900,  monthly: 1999, monthlyWas: 3000 }
  ],
  appStore: "https://apps.apple.com/ae/app/my-messify/id6749799177",
  playStore: "https://play.google.com/store/apps/details?id=com.messifyfzc.messify"
};
/* ===================================== */


const fmt = n => "AED " + n.toLocaleString("en-US");
const per = (p, len) => p[len] / (p.mpd * (len === "weekly" ? CONFIG.daysPerWeek : CONFIG.daysPerMonth));
const ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';


/* ---------- topics ---------- */
const TOPICS = {
  meals: {
    label: "Meal plans",
    placeholder: "What can we cook for you this week?",
    qa: ["See plans", "What plans do you have?"],
    eyebrow: "Meal plans · Dubai",
    title: "Your meals, <em>handled.</em>",
    facts: [["From AED 25","per meal"],["1 bag","every morning"],["Daily","new menu"]],
    greeting: { reply: "Hey! I'm Messibot. Meal plans start from AED 25 a meal, delivered together every morning. Are you a student or a working professional?",
      quick_replies: ["Student", "Working professional"] },
    stripLabel: "A taste of the menu",
    photos: [
      { src:IMG + "bag-bowls.webp", thumb:IMG + "bag-bowls-640.webp", name:"Kebab & rice bowls", alt:"Two kebab and rice bowls with vegetables packed in a Messify thermal bag" },
      { src:IMG + "wrap.webp", thumb:IMG + "wrap.webp", name:"Fresh wraps", alt:"A fresh wrap held in a gloved hand, roast potatoes beside" },
      { src:IMG + "pasta-dish.webp", thumb:IMG + "pasta-dish.webp", name:"Grilled chicken penne", alt:"Grilled chicken over creamy penne, finished with parmesan" },
      { src:IMG + "biryani.webp", thumb:IMG + "biryani.webp", name:"Paneer makhani & saffron rice", alt:"Paneer in red gravy with saffron rice" }
    ],
    fields: [["name","Name"],["segment","Who"],["area","Area"],["meals_per_day","Meals / day"],["plan","Plan"],["objection","Objection"],["notes","Notes"]],
    stages: [["qualify","Qualifying"],["recommend","Plan pitched"],["objection","Objection"],["close","Ready to close"]],
    panelTitle: "Turns visitors into <em>WhatsApp-ready</em> meal plan buyers.",
    panelLede: "Chat with it like a customer would. It asks what they need, recommends a plan with real per-meal numbers, handles objections, then hands a summarised lead to your WhatsApp.",
    playbook: [
      ["Qualify in three questions","Student or professional, delivery area, meals a day. One question at a time."],
      ["Recommend one plan, with the math","Monthly first: AED 25.6–27.5 a meal against AED 29–31 weekly. 26 days of meals, to use within 30 days."],
      ["Handle the usual objections","Bored → menu changes daily. Skipping days → the token stays until the plan ends. Is it hot? → blast-chilled, quick reheat. Halal → 100%."],
      ["Close on WhatsApp","Pre-filled summary to " + CONFIG.whatsappDisplay + ". Out of area: logged as a waitlist lead."]
    ]
  },
  catering: {
    label: "Catering",
    placeholder: "Tell us about your event…",
    qa: ["Get a quote", "I'd like a catering quote"],
    eyebrow: "Messify Catering",
    title: "Your event, <em>fed properly.</em>",
    facts: [["5,000+","meals a day capacity"],["4","emirates covered"],["100%","custom menus"]],
    greeting: { reply: "Welcome to Messify Catering. We cater corporate events, university events, weddings and bulk orders across Dubai, Sharjah, Ajman and Abu Dhabi, with a menu built around you. What's the occasion?",
      quick_replies: ["Corporate / office", "University event", "Wedding", "Bulk catering"] },
    stripLabel: "From our events",
    photos: [
      { src:IMG + "cat-chef.webp", thumb:IMG + "cat-chef-640.webp", name:"Live carving station", alt:"A chef carving at a buffet station while guests serve themselves at an evening event" },
      { src:IMG + "cat-serving.webp", thumb:IMG + "cat-serving-640.webp", name:"Hot buffet service", alt:"A gloved server lifting the lid of a gold chafing dish at a catered buffet" },
      { src:IMG + "cat-canapes.webp", thumb:IMG + "cat-canapes.webp", name:"Canapé trays", alt:"Trays of canapés on slate boards at a catered event" },
      { src:IMG + "cat-buffet.webp", thumb:IMG + "cat-buffet.webp", name:"Dessert & tartlet table", alt:"A buffet table set with tartlets, skewers and desserts" }
    ],
    fields: [["name","Name"],["company","Company"],["event_type","Event"],["guests","Guests"],["emirate","Emirate"],["date","Date"],["courses","Courses"],["flavours","Flavours"],["dietary","Dietary"]],
    stages: [["qualify","Event details"],["brief","Menu brief"],["close","Ready to quote"]],
    panelTitle: "Turns event enquiries into <em>quote-ready</em> briefs.",
    panelLede: "The catering side asks what a good events manager would: the occasion, headcount, emirate, date and menu. Then it hands your team a complete brief on WhatsApp, so the first reply can be a quote.",
    playbook: [
      ["Understand the event","Occasion, guest count, emirate and date. One question at a time."],
      ["Shape the menu","Courses and flavours from your builder: Indian, Arabic, Continental, Italian, Chinese."],
      ["Reassure on scale","5,000+ meals a day, centralised kitchen, on-time delivery across four emirates."],
      ["Hand over a brief","Never quotes a price. Sends the full brief to " + CONFIG.whatsappDisplay + " for your team to quote."]
    ]
  }
};


/* ---------- state ---------- */
let topic = null, lead = {}, turns = [], busy = false, ctl = null, stage = "qualify", logged = false;
const T = () => TOPICS[topic || "meals"];

function setTheme(t){
  host.dataset.mode = t;
  const C = TOPICS[t];
  box.placeholder = topic ? C.placeholder : "Ask about meal plans or catering…";
  $("#qa-1").textContent = C.qa[0];
  root.querySelectorAll("#switch button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.go === t)));
}

function renderLead(){}
function mergeLead(n){ if (!n || typeof n !== "object") return; for (const [k,v] of Object.entries(n)) if (v !== null && v !== undefined && v !== "") lead[k] = v; }

function scroll(){ msgs.scrollTop = msgs.scrollHeight; }
function clearChips(){ msgs.querySelectorAll(".chips").forEach(c => c.remove()); }
function botRow(){ const r = document.createElement("div"); r.className = "row"; const a = document.createElement("img"); a.className = "av"; a.src = AV; a.alt = ""; r.append(a); return r; }
function addBubble(text, who){
  const d = document.createElement("div"); d.className = "b " + who; d.textContent = text;
  if (who === "bot") { const r = botRow(); r.append(d); msgs.append(r); } else msgs.append(d);
  scroll(); return d;
}
function addChips(list){
  clearChips(); if (!list || !list.length) return;
  const c = document.createElement("div"); c.className = "chips";
  for (const q of list.slice(0,4)) { const b = document.createElement("button"); b.type = "button"; b.className = "chip"; b.textContent = q; b.onclick = () => send(q); c.append(b); }
  msgs.append(c); scroll();
}
function typing(on){
  const t = msgs.querySelector(".typing-row");
  if (on && !t){ const r = botRow(); r.classList.add("typing-row"); const d = document.createElement("div"); d.className = "b bot typing"; d.innerHTML = "<i></i><i></i><i></i>"; d.setAttribute("aria-label","Messibot is typing"); r.append(d); msgs.append(r); scroll(); }
  if (!on && t) t.remove();
}

/* ---------- handoff ---------- */
function briefText(){
  const c = lead.courses || "A custom menu", f = lead.flavours ? ` in ${lead.flavours} flavours` : "";
  const g = lead.guests ? `${lead.guests} guests` : "your guests", e = lead.emirate || "the UAE";
  return { plain: `${c}${f}, for ${g} in ${e}${lead.date ? ", " + lead.date : ""}.`,
           html: `${esc(c)}${f ? " in <em>" + esc(lead.flavours) + "</em> flavours" : ""}, for <em>${esc(g)}</em> in ${esc(e)}${lead.date ? ", " + esc(lead.date) : ""}.` };
}
function esc(s){ return String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }
function waText(){
  let L;
  if (topic === "catering") {
    L = ["Hi Messify! I'd like a catering quote."];
    if (lead.name) L.push("Name: " + lead.name);
    if (lead.company) L.push("Company: " + lead.company);
    if (lead.event_type) L.push("Event: " + lead.event_type);
    if (lead.guests) L.push("Guests: " + lead.guests);
    if (lead.emirate) L.push("Emirate: " + lead.emirate);
    if (lead.date) L.push("Date: " + lead.date);
    if (lead.courses) L.push("Courses: " + lead.courses);
    if (lead.flavours) L.push("Flavours: " + lead.flavours);
    if (lead.dietary) L.push("Dietary: " + lead.dietary);
  } else {
    L = [lead.in_area === false ? "Hi Messify! Please add me to the waitlist for my area." : "Hi Messify! I'd like to start a meal plan."];
    if (lead.name) L.push("Name: " + lead.name);
    if (lead.segment) L.push("I'm a: " + lead.segment);
    if (lead.area) L.push("Area: " + lead.area);
    if (lead.meals_per_day) L.push("Meals per day: " + lead.meals_per_day);
    if (lead.plan) L.push("Plan: " + lead.plan);
  }
  if (lead.notes) L.push("Notes: " + lead.notes);
  L.push("(from website chat)");
  return L.join("\n");
}
function showHandoff(){
  msgs.querySelector(".handoff")?.remove();
  const t = waText(), cat = topic === "catering";
  const d = document.createElement("div"); d.className = "handoff";
  d.innerHTML = (cat ? `<small class="k">Your brief</small><p class="brief">${briefText().html}</p>` : `<small class="k">Your summary</small><pre></pre>`) +
    `<a class="wa" target="_blank" rel="noopener" href="https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(t)}">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.4 14.2c-.2.6-1.3 1.2-1.8 1.3-.5 0-1 .2-3.3-.7-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>
    ${cat ? "Send brief on WhatsApp" : "Continue on WhatsApp"}</a>
    <span class="fine">Opens WhatsApp to ${CONFIG.whatsappDisplay} with this ${cat ? "brief" : "summary"}. Your answers are shared with the Messify team.${cat ? "" : ` Prefer the app? <a href="${CONFIG.appStore}" target="_blank" rel="noopener">iOS</a> · <a href="${CONFIG.playStore}" target="_blank" rel="noopener">Android</a>`}</span>`;
  if (!cat) d.querySelector("pre").textContent = t;
  d.querySelector(".wa").addEventListener("click", () => track("whatsapp_click"));
  msgs.append(d); scroll();
  logLead(t);
}


/* ---------- lead log + ad tracking ---------- */
function track(kind){
  try {
    if (kind === "whatsapp_click") {
      if (typeof window.fbq === "function") window.fbq("track", "Lead", { content_name: topic === "catering" ? "Catering brief" : "Meal plan" });
      if (typeof window.gtag === "function") window.gtag("event", "generate_lead", { method: "messibot_whatsapp", topic: topic });
    } else if (kind === "message" && typeof window.gtag === "function") {
      window.gtag("event", "messibot_message", { topic: topic });
    }
  } catch (e) {}
}
function logLead(summary){
  if (logged || !lead.phone) return; logged = true; // no number = nothing to follow up; the WhatsApp message itself is the lead
  const data = { _subject: (topic === "catering" ? "Messibot catering brief" : (lead.in_area === false ? "Messibot waitlist" : "Messibot meal plan lead")) + (lead.name ? " · " + lead.name : "") + " · " + lead.phone,
    _template: "table", _captcha: "false", Topic: topic === "catering" ? "Catering" : "Meal plans", Summary: summary, Page: location.href };
  for (const [k, v] of Object.entries(lead)) if (v !== "" && v != null) data[k] = String(v);
  try { fetch(FORM_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(data), keepalive: true }).catch(() => {}); } catch (e) {}
}
/* ---------- scripted engine ----------
   How it works: each topic is a short list of steps (the questions we need answered).
   Every message is (1) checked for a hand-off or topic switch, (2) used to fill the current step,
   (3) scanned for answers to later steps so people can skip ahead, and (4) checked against the FAQ
   library. A question gets answered, then the bot re-asks the current step, so the chat always moves forward. */
let lastHit = null;
const norm = s => " " + s.toLowerCase().replace(/[’']/g, "").replace(/[^a-z0-9+؀-ۿ ]/g, " ").replace(/\s+/g, " ").trim() + " ";
const isQuestion = (raw, t) => /\?/.test(raw) || /^ (what|how|is|are|do|does|can|could|when|where|will|which|who|why|any) /.test(t);
const cap = s => s.replace(/\b\w/g, c => c.toUpperCase());
const sentence = s => s.charAt(0).toUpperCase() + s.slice(1);
const plural = n => n + " meal" + (n > 1 ? "s" : "");
function planFor(m){ return CONFIG.plans.find(p => p.mpd === m) || CONFIG.plans[0]; }
function pitchText(){ const p = planFor(lead.meals_per_day || 1);
  return `For ${plural(p.mpd)} a day, I'd go monthly: ${fmt(p.monthly)} for ${p.mpd * 26} meals, about AED ${per(p, "monthly").toFixed(1)} a meal, and you get 30 days to use them. Want to try it first? Weekly is ${fmt(p.weekly)} for ${p.mpd * 7} meals, to use within 9 days.`; }
const AREA_KEYS = [["Academic City", / academic /], ["Dubai Silicon Oasis", / silicon | dso /], ["International City", / international | intl city | warsan /], ["Dubai Festival City", / festival | dfc | al badia | badia /]];
function areaMatch(t){ const hit = AREA_KEYS.find(([, re]) => re.test(t)); return hit ? hit[0] : undefined; }
function mealsIn(t, cur){
  if (!cur && !/ meal| meals | a day | per day /.test(t)) return;
  if (/ (3|three) /.test(t) || /breakfast.*lunch.*dinner| all three | all meals /.test(t)) return 3;
  if (/ (2|two) /.test(t) || / lunch and dinner | breakfast and lunch | breakfast and dinner /.test(t)) return 2;
  if (/ (1|one|single) /.test(t) || (cur && / just | only | lunch | dinner | breakfast /.test(t))) return 1;
}
const EMIRATES = [["Dubai", / dubai | dxb /], ["Sharjah", / sharjah | shj /], ["Ajman", / ajman /], ["Abu Dhabi", / abu ?dhabi | auh /]];
const CUISINES = [["Indian", / indian | desi | biryani /], ["Arabic", / arab| lebanese | emirati | khaleeji | middle eastern /], ["Continental", / continental | western /], ["Italian", / italian | pasta /], ["Chinese", / chinese | asian /]];
const COURSES = [["appetisers", / appeti| starter| canape/], ["main course", / main/], ["salads", / salad/], ["desserts", / dessert| sweet/], ["beverages", / beverage| drink| juice| coffee | tea /]];
const listJoin = a => a.length < 2 ? a.join("") : a.slice(0, -1).join(", ") + " and " + a[a.length - 1];

let phoneTries = 0;
const PHONE_STEP = { key: "phone", label: "WhatsApp number",
  ask: () => phoneTries ? "That doesn't look like a phone number. Type it like 050 123 4567, or tap Skip." : "And your WhatsApp number, so the team can reach you even if the chat doesn't open? You can skip this.",
  chips: () => ["Skip"],
  grab: (t, cur) => { if (cur && /^ (skip|no|no thanks|nah) $/.test(t)) return ""; const m = t.replace(/[ -]/g, "").match(/\+?\d{8,15}/); return m ? m[0] : undefined; },
  free: (raw, t) => { if (/ skip | no /.test(t)) { lead.phone = ""; } else { phoneTries++; } return true; },
  set: v => { lead.phone = v; }, ack: () => lead.phone ? "Got it, thanks." : "" };

const SCRIPTS = {
  meals: {
    steps: [
      { key: "segment", label: "Student or professional",
        ask: () => "Are you a student or a working professional?", chips: () => ["Student", "Working professional"],
        grab: t => / student | uni | university | college | campus /.test(t) ? "student" : / work | working | professional | job | employee | office worker /.test(t) ? "professional" : undefined,
        free: raw => { lead.segment = raw.length < 30 ? raw : "professional"; return true; },
        set: v => { lead.segment = v; },
        ack: () => lead.segment === "student" ? "Nice, no cooking between lectures then." : "Nice, busy workdays are exactly what we're built for." },
      { key: "area", label: "Delivery area",
        ask: () => "Where should we deliver?", chips: () => [...CONFIG.areas, "Somewhere else"],
        grab: t => areaMatch(t), set: v => { lead.area = v; lead.in_area = true; },
        free: (raw, t) => { lead.area = / somewhere else | other | outside /.test(t) ? "Outside current areas" : raw; lead.in_area = false; if (!("meals_per_day" in lead)) lead.meals_per_day = ""; if (!("plan" in lead)) lead.plan = ""; return true; },
        ack: () => lead.in_area === false ? "We're not delivering there yet, but we're expanding. Leave your details and you'll be first to know when we reach you." : `Great, we deliver to ${lead.area}.` },
      { key: "meals_per_day", label: "Meals a day",
        ask: () => "How many meals a day do you want handled?", chips: () => ["1 meal", "2 meals", "3 meals"],
        grab: (t, cur) => mealsIn(t, cur), set: v => { lead.meals_per_day = v; stage = "recommend"; } },
      { key: "plan", label: "Plan chosen",
        ask: pitchText, reask: () => "Shall I set you up on monthly, or would you like to try a week first?",
        chips: () => ["Start monthly", "Try weekly first", "Is it delivered hot?"],
        grab: (t, cur) => { if (!cur) return;
          if (/ month/.test(t)) return "monthly"; if (/ week| try /.test(t)) return "weekly";
          if (/ yes | yeah | yep | sure | ok | okay | start | sign | go | book | lets | perfect | sounds good | done /.test(t)) return "monthly"; },
        set: v => { lead.plan = plural(lead.meals_per_day || 1) + "/day " + v; stage = "close"; },
        ack: () => lead.plan.endsWith("weekly") ? "Good call, a week is the easiest way to try us." : "Great choice, that's the best price per meal." },
      { key: "name", label: "First name",
        ask: () => "Last thing: what's your first name, so the team knows who's messaging?", chips: () => ["Skip"],
        grab: (t, cur) => { if (cur && /^ (skip|no|no thanks|nah) $/.test(t)) return ""; const m = t.match(/ (?:my name is|this is|call me) ([a-z]+) /); return m ? cap(m[1]) : undefined; },
        free: (raw, t) => { lead.name = / skip | no /.test(t) ? "" : cap(raw.split(/\s+/).slice(0, 3).join(" ")); return true; },
        set: v => { lead.name = v; } },
      PHONE_STEP
    ],
    done: () => ({ reply: lead.in_area === false
      ? `Thanks${lead.name ? ", " + lead.name : ""}! You're on the waitlist. Tap below to send it on WhatsApp too, and the team will message you when we reach your area.`
      : `Thanks${lead.name ? ", " + lead.name : ""}! Tap below to send this to our team on WhatsApp. They'll confirm your start date and get you set up in minutes.`, handoff: true })
  },
  catering: {
    steps: [
      { key: "event_type", label: "Occasion",
        ask: () => "What's the occasion?", chips: () => ["Corporate / office", "University event", "Wedding", "Bulk catering"],
        grab: t => / corporate | office | company | conference | meeting | seminar /.test(t) ? "Corporate / office"
          : / university | campus | college | uni | society | orientation | graduation /.test(t) ? "University event"
          : / wedding | nikah | engagement | mehendi | reception /.test(t) ? "Wedding"
          : / bulk | labour | labor | site | institution | daily supply /.test(t) ? "Bulk catering"
          : / birthday | party | family | private | eid | iftar | ramadan | gathering /.test(t) ? "Private event" : undefined,
        free: raw => { lead.event_type = raw; return true; }, set: v => { lead.event_type = v; },
        ack: () => lead.event_type === "Wedding" ? "Congratulations!" : "Lovely." },
      { key: "guests", label: "Guest count",
        ask: () => "Roughly how many guests are you expecting?", chips: () => ["Under 50", "50 to 200", "200 to 500", "500+"],
        grab: (t, cur) => { if (!cur && !/ guest| people | pax | persons | person | heads | attendees /.test(t)) return;
          const n = t.match(/ (under |over |around |about )?(\d[\d,]*)(\+| to \d[\d,]*)? /); if (n) return n[0].trim();
          if (cur && / hundred | thousand /.test(t)) return t.trim(); },
        set: v => { lead.guests = v; },
        ack: () => /500|\d{4}|thousand/.test(lead.guests || "") ? "Big numbers are where we shine: our kitchen runs 5,000+ meals a day." : "" },
      { key: "emirate", label: "Emirate",
        ask: () => "Which emirate is the event in?", chips: () => CONFIG.emirates,
        grab: t => { const e = EMIRATES.find(([, re]) => re.test(t)); return e ? e[0] : undefined; },
        free: raw => { lead.emirate = raw; lead.notes = "Location outside the four emirates, check coverage"; return true; },
        set: v => { lead.emirate = v; stage = "brief"; },
        ack: () => CONFIG.emirates.includes(lead.emirate) ? "" : "We cover Dubai, Sharjah, Ajman and Abu Dhabi, and the team will confirm if we can reach you." },
      { key: "date", label: "Date",
        ask: () => "When is it?", chips: () => ["This week", "This month", "Date not fixed yet"],
        grab: (t, cur) => { const M = "(january|jan|february|feb|march|mar|april|apr|may|june|jun|july|jul|august|aug|september|sept|sep|october|oct|november|nov|december|dec)";
          const m = t.match(new RegExp(" \\d{1,2}(st|nd|rd|th)? (of )?" + M + " ")) || t.match(new RegExp(" " + M + " \\d{1,2}(st|nd|rd|th)? "))
            || t.match(/ (january|february|march|april|june|july|august|september|october|november|december) /) || t.match(/ (next|this) (week|month|weekend) | tomorrow | \d{1,2} \d{1,2}( \d{2,4})? /);
          if (m) return m[0].trim(); if (cur && / not fixed | not sure | tbc | dont know /.test(t)) return "Not fixed yet"; },
        free: raw => { lead.date = raw; return true; }, set: v => { lead.date = sentence(v); } },
      { key: "flavours", label: "Flavours",
        ask: () => "Every menu is fully custom. Which flavours suit your guests?", chips: () => ["Indian", "Arabic", "Continental", "A mix"],
        grab: (t, cur) => { const f = CUISINES.filter(([, re]) => re.test(t)).map(([n]) => n); if (f.length) return listJoin(f); if (cur && / mix | mixed | variety | all /.test(t)) return "a mix of"; },
        free: raw => { lead.flavours = raw; return true; }, set: v => { lead.flavours = v; } },
      { key: "courses", label: "Courses",
        ask: () => "And which courses? We do appetisers, mains, salads, desserts and beverages.", chips: () => ["Main course & desserts", "Full spread", "Mains only"],
        grab: (t, cur) => { if (/ full | everything | all courses /.test(t)) return "Appetisers, main course, salads, desserts and beverages";
          if (!cur && !/ course| starter| dessert| salad| appeti/.test(t)) return;
          const c = COURSES.filter(([, re]) => re.test(t)).map(([n]) => n); if (c.length) return sentence(listJoin(c)); },
        free: raw => { lead.courses = raw; return true; }, set: v => { lead.courses = v; } },
      { key: "dietary", label: "Dietary needs",
        ask: () => "Any dietary needs we should note, like vegetarian options or allergies?", chips: () => ["None", "Vegetarian options", "Allergies to note"],
        grab: (t, cur) => { if (!cur) return; if (/ none | no | nope | nothing /.test(t)) return "None";
          if (t.trim().length > 1 && !/^ (what|how|is|are|do|does|can|could|will) /.test(t)) return sentence(t.trim()); },
        set: v => { lead.dietary = v; }, ack: () => lead.dietary !== "None" ? "Noted, the team will confirm the specifics." : "" },
      { key: "name", label: "Name & company",
        ask: () => "Who should the team address the quote to? Your name, and company if it's for one.", chips: () => ["Skip"],
        grab: (t, cur) => { if (cur && /^ (skip|no|no thanks|nah) $/.test(t)) return ""; const m = t.match(/ (?:my name is|this is|call me) ([a-z]+) /); return m ? cap(m[1]) : undefined; },
        free: (raw, t) => { lead.name = / skip | no /.test(t) ? "" : raw; return true; }, set: v => { lead.name = v; } },
      PHONE_STEP
    ],
    done: () => ({ reply: `Thank you${lead.name ? ", " + lead.name.split(/[ ,]/)[0] : ""}. That's everything the team needs. Here's your brief: tap below to send it on WhatsApp and they'll come back with a quote.`, handoff: true })
  }
};

/* FAQ library: answered at any point, then the bot returns to the current step.
   "end": hands off or switches topic immediately. */
const FAQ = {
  meals: [
    { id: "human", label: "Talk to a person", re: / human | agent | real person | talk to | speak to | call me | phone | whatsapp /, end: () => ({ reply: "Sure. Tap below and you'll be chatting with our team on WhatsApp.", handoff: true }) },
    { id: "catering", label: "Catering → switch", re: / cater| event | wedding | party | conference | bulk /, end: () => ({ reply: "That sounds like one for our catering team. Switching you over.", switch: "catering" }) },
    { id: "office", label: "Office team plans", re: / office plan| for my team | for our team | for my office | colleagues | company plan | corporate plan | employees /, end: () => ({ reply: "We do monthly office meal plans for teams too. Tap below and the team will set one up for you.", handoff: true, lead: { notes: "Office / team meal plan" } }) },
    { id: "price", label: "Prices", re: / price| cost | costs | how much | plans | pricing | rates | expensive | cheap | aed /, ans: () => {
        if (lead.meals_per_day) { const p = planFor(lead.meals_per_day); return `${plural(p.mpd)} a day is ${fmt(p.monthly)} a month for ${p.mpd * 26} meals (about AED ${per(p, "monthly").toFixed(1)} a meal, 30 days to use them), or ${fmt(p.weekly)} a week for ${p.mpd * 7} meals.`; }
        return "Plans start from AED 25 a meal. Monthly plans give you 26 days of meals to use within 30 days: 1 meal a day AED 715, 2 meals AED 1,400, 3 meals AED 1,999. Weekly plans start at AED 215."; } },
    { id: "trial", label: "Trying it first", re: / trial | sample | test it | first time /, ans: () => "The weekly plan is the easiest way to try us: 7 days, from AED 215, no long commitment." },
    { id: "expiry", label: "Token expiry", re: / expire| expiry| valid| roll over| rollover| carry over| carry forward| unused /, ans: () => "Monthly plans give you 30 days to use 26 days of meals, and weekly plans give you 9 days to use 7. Plan to use them within that window: spare tokens are perfect for doubling up or ordering for a friend." },
    { id: "tokens", label: "How tokens work", re: / token| messicon| coin| how does it work | how it works /, ans: () => "Every meal on your plan is one token. You pick tomorrow's meals in the app and each one uses a token, for breakfast, lunch or dinner. Unused tokens last until your plan ends." },
    { id: "skip", label: "Skipping days", re: / skip| pause| travel| holiday| vacation| away | miss /, ans: () => "Skip a meal or a whole day in the app and the token stays in your wallet. Spare days are built in: monthly plans give you 30 days to use 26 days of meals, weekly plans 9 days for 7." },
    { id: "extra", label: "Extra meals", re: / extra| friend| double| more food | hungry /, ans: () => "Hungry or friends coming over? Use extra tokens to order more meals that day." },
    { id: "hot", label: "Hot or chilled", re: / hot | cold | warm | fresh| reheat| microwave| chill| heat /, ans: () => "Meals are blast-chilled after cooking for safety and arrive chilled with an ice pack. A few minutes of reheating and they're almost as fresh as just cooked." },
    { id: "areas", label: "Delivery areas", re: / where | area| location| do you cover | available in | deliver to /, ans: () => `We deliver to ${listJoin(CONFIG.areas)} right now, and we're expanding.` },
    { id: "delivery", label: "Delivery time", re: / deliver| what time | when | morning| arrive| timing/, ans: () => "One delivery every morning: all your meals for the day together in a Messify thermal bag. Want to know the delivery window for your building? The team can confirm it on WhatsApp." },
    { id: "halal", label: "Halal", re: / halal| haram| pork /, ans: () => "Yes, everything we serve is 100% halal." },
    { id: "allergy", label: "Allergies", re: / allerg| gluten| nut | nuts | dairy| lactose| shellfish| intoleran/, ans: () => "Tell the team about any allergies on WhatsApp before you start, and they'll confirm which dishes are safe for you." },
    { id: "veg", label: "Vegetarian", re: / veg| vegetarian| vegan| meat free| no meat | plant based/, ans: () => "Yes, there's a vegetarian option every day, for every meal. For vegan, the team can confirm what fits." },
    { id: "menu", label: "Menu & variety", re: / menu| dish| food | cuisine| options | variety| bored | same food /, ans: () => "Balanced, home-style meals cooked fresh every day in our partner kitchen, with a new menu daily. You see tomorrow's meals in the app and pick yours." },
    { id: "diet", label: "Diets & nutrition", re: / keto| diet| calori| protein| macro| healthy/, ans: () => "Our meals are balanced and the menu changes every day. For a specific diet, the team can tell you what fits on WhatsApp before you start." },
    { id: "app", label: "App & ordering", re: / app | download| how do i order | ordering | ios | android | iphone /, ans: () => "Everything runs through the Messify app on iPhone and Android: pick your meals, skip days and top up tokens." },
    { id: "pay", label: "Payment", re: / pay| card | cash | apple pay /, ans: () => "You pay by card, right in the Messify app." },
    { id: "cancel", label: "Cancel / refund → team", re: / cancel| refund| money back /, end: () => ({ reply: "Our team handles cancellations and refunds directly. Tap below to message them on WhatsApp.", handoff: true, lead: { notes: "Asked about cancellation / refunds" } }) },
    { id: "about", label: "What is Messify", re: / what is messify | who are you | what do you do | about messify /, ans: () => "Messify is a Dubai meal plan: balanced meals, a new menu every day, all delivered together each morning." },
    { id: "hello", label: "Greetings", re: /^ (hi|hello|hey|salam|assalam[a-z ]*|good morning|good evening|yo) $/, ans: () => "Hey!" },
    { id: "thanks", label: "Thanks", re: / thank| shukran| cheers /, ans: () => "Anytime!" }
  ],
  catering: [
    { id: "human", label: "Talk to a person", re: / human | agent | real person | talk to | speak to | call me | phone | whatsapp /, end: () => ({ reply: "Of course. Tap below and you'll be chatting with our events team on WhatsApp.", handoff: true }) },
    { id: "meals", label: "Meal plans → switch", re: / meal plan| subscription| for myself | daily meals | token/, end: () => ({ reply: "Sounds like a personal meal plan. Switching you over.", switch: "meals" }) },
    { id: "price", label: "Price & quotes", re: / price| cost | how much | quote | per head | per person | budget | rate /, ans: () => "Every quote is built around your headcount and menu, so the team prices it exactly. A few quick details and I'll put your brief together." },
    { id: "capacity", label: "Capacity", re: / capacity | how many can | large | big event | thousands | scale /, ans: () => "Our centralised kitchen can produce 5,000+ meals a day, with the same quality control on every batch." },
    { id: "areas", label: "Areas covered", re: / where | area| emirates | location| do you cover /, ans: () => "We cater across Dubai, Sharjah, Ajman and Abu Dhabi, with on-time bulk delivery." },
    { id: "menu", label: "Menu options", re: / menu| cuisine| dish| options | what food /, ans: () => "Menus are fully custom. Pick from appetisers, mains, salads, desserts and beverages, in Indian, Arabic, Continental, Italian, Chinese or other flavours." },
    { id: "service", label: "Staff, setup, timing", re: / staff | server| waiter| setup | set up | equipment| chafing| buffet | live station| tasting| lead time| notice | minimum /, ans: () => "Good one for the team: they'll confirm service staff, setup, timings and any minimums with your quote." },
    { id: "halal", label: "Halal", re: / halal| haram| pork /, ans: () => "Yes, all our food is 100% halal." },
    { id: "diet", label: "Diets & allergies", re: / veg| vegan| allerg| gluten| diet/, ans: () => "We'll note any dietary needs in your brief and the team will confirm options." },
    { id: "hello", label: "Greetings", re: /^ (hi|hello|hey|salam|assalam[a-z ]*|good morning|good evening) $/, ans: () => "Hello!" },
    { id: "thanks", label: "Thanks", re: / thank| shukran| cheers /, ans: () => "My pleasure." }
  ]
};

function currentStep(){ return SCRIPTS[topic].steps.find(s => !(s.key in lead)); }
function runScript(raw){
  const S = SCRIPTS[topic], t = norm(raw), cur = currentStep(), q = isQuestion(raw, t);
  const f = FAQ[topic].find(x => x.re.test(t));
  if (f && f.end) { lastHit = { kind: "faq", f }; return f.end(); }
  let filled = [], acks = [];
  if (cur) { const v = cur.grab && cur.grab(t, true); if (v != null) { cur.set(v); filled.push(cur); } }
  for (const s of S.steps) if (s !== cur && !(s.key in lead) && s.grab) { const v = s.grab(t, false); if (v != null) { s.set(v); filled.push(s); } }
  if (!filled.length && cur && cur.free && !f && !q && raw.length > 1) { cur.free(raw, t); filled.push(cur); }
  for (const s of filled) { const a = s.ack && s.ack(); if (a) acks.push(a); }
  for (const s of S.steps) { if ((s.key in lead) && s.stop) { const r = s.stop(); if (r) { lastHit = { kind: "step", filled }; return r; } } }
  const nx = currentStep();
  const faqAns = f && f.ans && (!filled.length || q) && !(f.id === "price" && nx && nx.key === "plan") ? f.ans() : "";
  if (!filled.length && !faqAns) {
    lastHit = { kind: "miss", nx };
    return { reply: "Sorry, I didn't quite catch that. " + (nx ? nx.ask() : "Tap below to talk to the team."), quick_replies: nx ? [...nx.chips().slice(0, 3), "Talk to the team"] : ["Talk to the team"], handoff: !nx };
  }
  lastHit = filled.length ? { kind: "step", filled, f: faqAns ? f : null } : { kind: "faq", f, nx };
  if (!nx) { const d = S.done(); if (faqAns) d.reply = faqAns + " " + d.reply; return d; }
  const askText = (!filled.length && nx.reask) ? nx.reask() : nx.ask();
  const parts = [faqAns, acks.join(" "), askText].filter(Boolean);
  return { reply: faqAns ? parts[0] + "\n\n" + parts.slice(1).join(" ") : parts.join(" "), quick_replies: nx.chips() };
}


/* ---------- send ---------- */
async function send(text){
  text = (text || "").trim(); if (!text || busy) return;
  if (!topic) { openTopic(/cater|event|wedding|bulk|party|conference|guests/i.test(text) ? "catering" : "meals", true); }
  busy = true; sendBtn.disabled = true; clearChips();
  msgs.querySelectorAll(".err").forEach(e => e.remove());
  addBubble(text, "me"); box.value = "";
  turns.push({ role:"user", content:text });
  typing(true);
  let out;
  try {
    out = runScript(text); await new Promise(r => setTimeout(r, 420 + Math.min(out.reply.length * 6, 700)));
  } catch (e) {
    typing(false);
    if (e && e.code === "cancelled") { busy=false; sendBtn.disabled=false; return; }
      turns.pop();
      const er = document.createElement("div"); er.className = "err";
      er.textContent = e && e.code === "rate_limited" ? "Too many messages at once. Wait a moment, then send again." : "That reply didn't come through. Send your message again.";
      msgs.append(er); scroll(); busy=false; sendBtn.disabled=false; box.value = text; return;
  }
  typing(false);
  busy = false; sendBtn.disabled = false;
  if (out.switch && out.switch !== topic && TOPICS[out.switch]) {
    addBubble(out.reply, "bot");
    setTimeout(() => openTopic(out.switch), 700);
    return;
  }
  mergeLead(out.lead); if (out.stage) stage = out.stage; if (out.handoff) stage = "close";
  turns.push({ role:"assistant", content: JSON.stringify({ reply: out.reply, quick_replies: out.quick_replies || [] }) });
  addBubble(out.reply, "bot");
  if (out.handoff) showHandoff(); else addChips(out.quick_replies);
  renderLead();
  if (matchMedia("(hover:hover)").matches) box.focus();
  if (!logged) track("message");
}


/* ---------- photo strip + viewer ---------- */
function glimpseHTML(){
  const C = T();
  return `<section class="glimpse" aria-label="${C.stripLabel}"><header><small>${C.stripLabel}</small><a href="https://www.instagram.com/messify.me" target="_blank" rel="noopener">@messify.me ↗</a></header><div class="grid">${
    C.photos.map((f,i)=>`<button type="button" class="tile" data-i="${i}" aria-label="View ${f.name}"><img src="${f.thumb}" alt="${f.alt}"><span>${f.name}</span></button>`).join("")
  }</div></section>`;
}
let viewI = 0;
function openView(i){
  closeView(); const P = T().photos; viewI = (i + P.length) % P.length; const f = P[viewI];
  const v = document.createElement("div"); v.className = "viewer"; v.setAttribute("role","dialog"); v.setAttribute("aria-label", f.name);
  v.innerHTML = `<img src="${f.src}" alt="${f.alt}"><p></p><nav><button type="button" data-d="-1" aria-label="Previous photo">Prev</button><button type="button" class="close">Back to chat</button><button type="button" data-d="1" aria-label="Next photo">Next</button></nav>`;
  v.querySelector("p").textContent = f.name;
  v.querySelectorAll("[data-d]").forEach(b => b.onclick = () => openView(viewI + +b.dataset.d));
  v.querySelector(".close").onclick = closeView;
  v.addEventListener("click", e => { if (e.target === v) closeView(); });
  $(".chat").append(v); v.querySelector(".close").focus();
}
function closeView(){ root.querySelector(".viewer")?.remove(); }
root.addEventListener("keydown", e => { if (!root.querySelector(".viewer")) return; if (e.key==="Escape") closeView(); if (e.key==="ArrowRight") openView(viewI+1); if (e.key==="ArrowLeft") openView(viewI-1); });


/* ---------- screens ---------- */
function showDoors(){
  ctl?.abort(); lastHit = null; topic = null; lead = {}; turns = []; stage = "qualify"; busy = false; sendBtn.disabled = false;
  $("#switch").hidden = true; setTheme("meals");
  msgs.innerHTML = `<div class="gatehead"><img src="${AV}" alt=""><h3>Hi, I'm Messibot</h3><p>What can I help you with today?</p></div>
  <div class="doors">
    <button type="button" class="door door--meals" data-go="meals"><img src="${IMG}bag-bowls-640.webp" alt=""><span class="door__shade"></span>
      <span class="door__copy"><span class="door__tag">For every day</span><span class="door__title">Meal plans</span><span class="door__text">All your meals, delivered every morning. From AED 25 a meal.</span><span class="door__cta">Explore ${ARROW}</span></span></button>
    <button type="button" class="door door--catering" data-go="catering"><img src="${IMG}cat-chef-640.webp" alt=""><span class="door__shade"></span>
      <span class="door__copy"><span class="door__tag">For events</span><span class="door__title">Catering</span><span class="door__text">Corporate, university, weddings and bulk, across four emirates.</span><span class="door__cta">Explore ${ARROW}</span></span></button>
  </div>
  <div class="gatefoot"><span><b>Daily</b> new menu</span><span><b>5,000+</b> meals a day</span><span><b>4</b> emirates</span></div>`;
  msgs.querySelectorAll(".door").forEach(d => d.onclick = () => openTopic(d.dataset.go));
  msgs.scrollTop = 0;
}
function openTopic(t, silent){
  closeView(); ctl?.abort();
  lastHit = null; topic = t; lead = {}; phoneTries = 0; turns = []; stage = "qualify"; busy = false; sendBtn.disabled = false;
  const go = () => {
    setTheme(t); $("#switch").hidden = false;
    const C = TOPICS[t];
    msgs.innerHTML = `<div class="intro"><span class="eyebrow">${C.eyebrow}</span><h3>${C.title}</h3><div class="facts">${C.facts.map(([b,s]) => `<div><b>${b}</b><span>${s}</span></div>`).join("")}</div></div>`;
    msgs.insertAdjacentHTML("beforeend", glimpseHTML());
    msgs.querySelectorAll(".tile").forEach(x => x.onclick = () => openView(+x.dataset.i));
    if (!silent) { addBubble(C.greeting.reply, "bot"); addChips(C.greeting.quick_replies); }
    renderLead(); if (!silent) msgs.scrollTop = 0;
  };
  go();
}


/* ---------- open / close ---------- */
const panel = $("#panel"), launcher = $("#launcher"), teaser = $("#teaser");
let started = false, lastFocus = null;
const store = { get: k => { try { return sessionStorage.getItem(k); } catch (e) { return null; } }, set: (k, v) => { try { sessionStorage.setItem(k, v); } catch (e) {} } };
function open(t){
  teaser.hidden = true; store.set("messibot-teaser", "1");
  if (!started) { started = true; showDoors(); }
  if (t && TOPICS[t] && t !== topic) openTopic(t);
  lastFocus = document.activeElement;
  panel.hidden = false; launcher.classList.add("open"); launcher.setAttribute("aria-expanded", "true"); launcher.setAttribute("aria-label", "Close chat");
  if (matchMedia("(max-width:560px)").matches) { document.documentElement.style.overflow = "hidden"; }
  setTimeout(() => (matchMedia("(hover:hover)").matches ? box : $("#close").offsetParent ? $("#close") : launcher).focus(), 60);
  if (window.gtag) try { window.gtag("event", "messibot_open", { topic: t || "doors" }); } catch (e) {}
}
function close(){
  closeView();
  panel.hidden = true; launcher.classList.remove("open"); launcher.setAttribute("aria-expanded", "false"); launcher.removeAttribute("aria-label");
  document.documentElement.style.overflow = "";
  if (lastFocus && lastFocus.focus) lastFocus.focus(); else launcher.focus();
}
launcher.onclick = () => panel.hidden ? open() : close();
$("#close").onclick = close;
teaser.onclick = e => { if (e.target.id === "teaser-x") { teaser.hidden = true; store.set("messibot-teaser", "1"); return; } open(); };
teaser.onkeydown = e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } };
root.addEventListener("keydown", e => { if (e.key === "Escape" && !root.querySelector(".viewer") && !panel.hidden) close(); });
root.querySelectorAll("#switch button").forEach(b => b.onclick = () => { if (b.dataset.go !== topic) openTopic(b.dataset.go); });
$("#form").addEventListener("submit", e => { e.preventDefault(); send(box.value); });
$("#restart").onclick = showDoors;
$("#qa-1").onclick = () => { if (!topic) openTopic("meals", true); send(T().qa[1]); };
$("#qa-wa").onclick = () => { if (busy) return; if (!topic) openTopic("meals", true); clearChips(); stage = "close"; showHandoff(); };
document.addEventListener("click", e => {
  const a = e.target.closest && e.target.closest("[data-messibot]");
  if (!a) return; e.preventDefault(); open(a.getAttribute("data-messibot") || undefined);
});
if (!store.get("messibot-teaser")) setTimeout(() => { if (panel.hidden) teaser.hidden = false; }, 9000);
window.Messibot = { open, close };
})();
