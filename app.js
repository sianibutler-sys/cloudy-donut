/* Cloudy Donut Co. concept, Siani Creates */
(() => {
  const TZ = "America/New_York";
  const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  // Pages share this script. A missing element returns a no-op stand-in, so each page
  // only renders the sections it actually contains.
  const NONE = new Proxy(function () {}, {
    get: (_, k) => (k === "textContent" || k === "innerHTML" || k === "value" ? "" : k === Symbol.toPrimitive ? () => "" : NONE),
    set: () => true,
    apply: () => NONE,
  });
  const $ = (s, el = document) => el.querySelector(s) || NONE;
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Wix-hosted images, resized on their CDN
  const wix = (id, w = 600) =>
    `https://static.wixstatic.com/media/${id}/v1/fit/w_${w},h_${w},q_90,enc_auto/${id}`;
  const hydrateImages = (root = document) =>
    $$("img.wix[data-wix]", root).forEach((img) => {
      if (!img.src) img.src = wix(img.dataset.wix, img.dataset.w || 600);
      img.loading = img.closest(".intro, .site-header, .hero") ? "eager" : "lazy";
      img.decoding = "async";
    });

  /* ---------- Intro ---------- */
  const intro = $("#intro");
  const endIntro = () => {
    intro.classList.add("done");
    try { sessionStorage.setItem("cd-intro", "1"); } catch (e) {}
  };
  let seen = false;
  try { seen = sessionStorage.getItem("cd-intro") === "1"; } catch (e) {}
  if (seen || reduceMotion) intro.classList.add("done");
  else {
    setTimeout(endIntro, 5000);
    $(".intro-skip").addEventListener("click", endIntro);
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") endIntro(); }, { once: true });
  }

  /* ---------- Header ---------- */
  const header = $(".site-header");
  const onScroll = () => header.classList.toggle("solid", window.scrollY > 40);
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* ---------- Nav ---------- */
  const toggle = $(".nav-toggle"), nav = $("#nav");
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    document.body.style.overflow = open ? "hidden" : "";
    toggle.setAttribute("aria-expanded", String(open));
  });
  $$("#nav a").forEach((a) => a.addEventListener("click", () => {
    nav.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); document.body.style.overflow = "";
  }));

  /* ---------- Demo badge: clock switch + behind the scenes ---------- */
  const MODES = [
    { id: "live", label: "Right now", short: "Now", note: "Showing the real time in New York." },
    { id: "sat", label: "Saturday 10am", short: "Sat 10am", note: "Saturday, 10am in New York: Brooklyn Heights is open, NoLita opens at 11.", day: 6, mins: 600 },
    { id: "tue", label: "Tuesday", short: "Tue", note: "Tuesday in New York: both shops show when they open next.", day: 2, mins: 720 },
  ];
  let modeIx = 0;
  try { modeIx = Math.max(0, MODES.findIndex((m) => m.id === sessionStorage.getItem("cd-mode"))); } catch (e) {}
  const modeBtn = $("#mode-btn"), bts = $("#bts"), btsBtn = $("#bts-btn");
  const paintMode = () => {
    const m = MODES[modeIx];
    modeBtn.innerHTML = `<span class="b-lg">${m.label} view · switch</span><span class="b-sm">${m.short} ⇄</span>`;
    modeBtn.setAttribute("aria-label", `${m.label} view. Switch the clock`);
  };
  paintMode();
  modeBtn.addEventListener("click", () => {
    modeIx = (modeIx + 1) % MODES.length;
    try { sessionStorage.setItem("cd-mode", MODES[modeIx].id); } catch (e) {}
    paintMode();
    if (window.__cdRefresh) window.__cdRefresh();
    const t = $("#mode-toast"); t.textContent = MODES[modeIx].note; t.classList.add("on");
    $("#mode-live").textContent = MODES[modeIx].note;
    clearTimeout(paintMode.t); paintMode.t = setTimeout(() => t.classList.remove("on"), 3200);
  });
  const snap = () => {
    const h1 = $("main h1");
    const c = $('[data-snap="h1"]'); if (c && h1) c.textContent = `"${h1.innerHTML.replace(/<br\s*\/?>/gi, " ").replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim()}"`;
    const t = $('[data-snap="tel"]'); if (t) t.textContent = `Every one (${$$('a[href^="tel:"]').length} on this page)`;
  };
  const btsOpen = (o) => {
    bts.hidden = !o; btsBtn.setAttribute("aria-expanded", String(o));
    requestAnimationFrame(() => bts.classList.toggle("on", o));
    if (o) { snap(); $(".bts-x").focus(); } else btsBtn.focus();
  };
  btsBtn.addEventListener("click", () => btsOpen(bts.hidden));
  $(".bts-x").addEventListener("click", () => btsOpen(false));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !bts.hidden) btsOpen(false); });
  const tabs = $$(".bts-tabs [role=tab]");
  const pick = (tab) => {
    tabs.forEach((x) => { const on = x === tab; x.setAttribute("aria-selected", String(on)); x.tabIndex = on ? 0 : -1; $("#" + x.getAttribute("aria-controls")).hidden = !on; });
    $(".bts-body").scrollTop = 0;
  };
  tabs.forEach((tab, i) => {
    tab.addEventListener("click", () => pick(tab));
    tab.addEventListener("keydown", (e) => {
      const d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!d) return; e.preventDefault(); const n = tabs[(i + d + tabs.length) % tabs.length]; pick(n); n.focus();
    });
  });

  /* ---------- Time helpers (New York) ---------- */
  const nyNow = () => {
    const sim = MODES[modeIx];
    if (sim.day !== undefined) return { day: sim.day, mins: sim.mins };
    const parts = new Intl.DateTimeFormat("en-US", {
      timeZone: TZ, weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false,
    }).formatToParts(new Date());
    const get = (t) => parts.find((p) => p.type === t).value;
    const day = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].indexOf(get("weekday"));
    const mins = (parseInt(get("hour"), 10) % 24) * 60 + parseInt(get("minute"), 10);
    return { day, mins };
  };
  const toMins = (hhmm) => { const [h, m] = hhmm.split(":").map(Number); return h * 60 + m; };
  const fmt = (hhmm) => {
    let [h, m] = hhmm.split(":").map(Number);
    const ap = h >= 12 ? "pm" : "am"; h = h % 12 || 12;
    return m ? `${h}:${String(m).padStart(2, "0")}${ap}` : `${h}${ap}`;
  };
  const status = (loc) => {
    const keys = Object.keys(loc.hours || {});
    if (!keys.length) return { open: false, text: loc.hours_label };
    const { day, mins } = nyNow();
    const today = loc.hours[String(day)];
    if (today && mins >= toMins(today[0]) && mins < toMins(today[1]))
      return { open: true, text: `Open now until ${fmt(today[1])}` };
    for (let i = 0; i < 8; i++) {
      const d = (day + i) % 7, h = loc.hours[String(d)];
      if (!h) continue;
      if (i === 0 && mins >= toMins(h[0])) continue;
      const when = i === 0 ? "today" : i === 1 ? "tomorrow" : DAYS[d];
      return { open: false, text: `Opens ${when} at ${fmt(h[0])}` };
    }
    return { open: false, text: loc.hours_label };
  };


  /* ---------- Instagram row (Pop-ups) ---------- */
  // With an Instagram token, /api/instagram returns the live feed and the row draws its own tiles.
  // Without one (this concept), it shows Instagram's official embeds of the latest posts.
  const setupIG = async (data) => {
    const row = document.getElementById("ig-row");
    if (!row) return;
    let posts = null;
    try {
      const r = await fetch("/api/instagram");
      if (r.status === 200) posts = (await r.json()).posts;
    } catch (e) {}
    if (!posts || !posts.length) posts = data.instagram_posts || [];
    const day = (iso) => new Date(iso.length > 10 ? iso : iso + "T12:00:00").toLocaleDateString("en-US", { month: "short", day: "numeric" });
    const cloud = wix("d6231e_9077a0dc3d96405ca1bae4d9ad1a346c~mv2.png", 200);
    row.innerHTML = posts.map((p) => {
      const kind = p.kind === "reel" ? "Reel" : p.kind === "carousel" ? "Carousel" : "Post";
      const quote = p.quote || (p.caption || "").split(/(?<=[.!?])\s/)[0];
      return `<li class="igc${p.img || p.cover ? " has-img" : ""}"><a href="${esc(p.url)}" target="_blank" rel="noopener">
        ${p.img || p.cover ? `<img class="igc-img" src="${esc(p.img || p.cover)}" alt="" loading="lazy">` : `<img class="igc-mark" src="${cloud}" alt="" loading="lazy">`}
        <span class="igc-top"><span class="igc-kind">${p.kind === "reel" ? '<i class="igc-play"></i>' : ""}${kind}</span><time datetime="${esc(p.date)}">${esc(day(p.date))}</time></span>
        <span class="igc-q">${esc(quote)}</span>
        <span class="igc-foot">${p.note ? `<span class="igc-note">${esc(p.note)}</span>` : ""}<span class="igc-h">${esc(p.handles || "@cloudydonuts")}</span><span class="igc-go">${p.kind === "reel" ? "Watch the reel" : "See the post"} <b class="igc-playbtn" aria-hidden="true"></b></span></span>
      </a></li>`;
    }).join("");
    // Tap a card to watch the post right here, in Instagram's own player
    const dlg = document.getElementById("ig-dlg"), body = document.getElementById("ig-dlg-body");
    const embedJS = () => new Promise((res) => {
      if (window.instgrm) return res();
      const sc = document.createElement("script"); sc.src = "https://www.instagram.com/embed.js"; sc.async = true;
      sc.onload = res; sc.onerror = res; document.body.appendChild(sc);
    });
    row.addEventListener("click", async (e) => {
      const a = e.target.closest("a"); if (!a || !dlg || e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault();
      body.innerHTML = `<blockquote class="instagram-media" data-instgrm-permalink="${esc(a.href)}?utm_source=ig_embed" data-instgrm-version="14"><a href="${esc(a.href)}" target="_blank" rel="noopener">Loading the post…</a></blockquote>`;
      $("#ig-dlg-open").href = a.href;
      dlg.showModal();
      await embedJS(); if (window.instgrm) window.instgrm.Embeds.process();
    });
    $(".ig-dlg-x").addEventListener("click", () => dlg.close());
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("close", () => { body.innerHTML = ""; });
    row.addEventListener("pointerenter", embedJS, { once: true });
    const step = () => (row.querySelector("li") || { offsetWidth: 300 }).offsetWidth + 18;
    $("#ig-prev").addEventListener("click", () => row.scrollBy({ left: -step(), behavior: reduceMotion ? "auto" : "smooth" }));
    $("#ig-next").addEventListener("click", () => row.scrollBy({ left: step(), behavior: reduceMotion ? "auto" : "smooth" }));
  };

  /* ---------- Deep links (flavors.html#picker): land on the section after content renders ---------- */
  const landOnHash = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    const t = id && document.getElementById(id);
    if (!t) return;
    t.querySelectorAll(".reveal").forEach((el) => el.classList.add("in"));
    if (t.classList.contains("reveal")) t.classList.add("in");
    let userMoved = false;
    ["wheel", "touchstart", "keydown"].forEach((ev) => window.addEventListener(ev, () => { userMoved = true; }, { once: true, passive: true }));
    const go = () => { if (!userMoved) t.scrollIntoView({ block: "start", behavior: "auto" }); };
    go();
    requestAnimationFrame(go);
    window.addEventListener("load", go, { once: true });
    setTimeout(go, 500);
    const h = t.querySelector("h2, h1"); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
  };

  /* ---------- Email terms ---------- */
  const termsDlg = document.getElementById("terms-dlg");
  document.addEventListener("click", (e) => {
    if (e.target.closest("[data-terms]") && termsDlg) { e.preventDefault(); termsDlg.showModal(); }
    else if (e.target === termsDlg) termsDlg.close();
  });

  /* ---------- Content ---------- */
  const load = async () => {
    try {
      const r = await fetch("/api/content", { headers: { accept: "application/json" } });
      if (r.ok && (r.headers.get("content-type") || "").includes("json")) return await r.json();
    } catch (e) {}
    try {
      const [f, s] = await Promise.all([
        fetch("data/flavors.json").then((r) => r.json()),
        fetch("data/site.json").then((r) => r.json()),
      ]);
      return { ...f, ...s };
    } catch (e) {
      if (window.CD_DATA) return window.CD_DATA;
      throw e;
    }
  };

  const esc = (s = "") => s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  load().then((data) => {
    const byId = Object.fromEntries(data.flavors.map((f) => [f.id, f]));
    const thisWeek = new Set(data.lineup.flavors);

    // Lineup as a donut box (home). Tap a donut to lift it and read about it.
    const week = data.lineup.flavors.map((id) => byId[id]).filter(Boolean);
    $("#donut-box").innerHTML = week.map((f, i) => `
      <button class="slot" type="button" role="tab" data-box="${f.id}" aria-selected="false" aria-controls="box-detail" style="--r:${[-18, 34, -50, 12, 64, -8, 40, -30][i % 8]}deg;--x:${[-4, 5, -2, 3, 4, -3, 2, -5][i % 8]}px;--y:${[3, -2, 4, -3, 2, -4, 3, -1][i % 8]}px">
        <span class="well" aria-hidden="true"></span>
        <img src="${wix(f.img, 360)}" alt="" loading="lazy" decoding="async">
        <span class="visually-hidden">${esc(f.name)}</span>
      </button>`).join("");
    const showBox = (f) => {
      $$(".slot").forEach((s) => s.setAttribute("aria-selected", String(s.dataset.box === f.id)));
      $("#box-detail").innerHTML = `
        <p class="bd-num">${String(week.indexOf(f) + 1).padStart(2, "0")} / ${String(week.length).padStart(2, "0")}</p>
        <h3 class="bd-name">${esc(f.name)}</h3>
        <p class="bd-desc">${esc(f.desc)}</p>
        ${f.contains ? `<p class="bd-contains">${esc(f.contains)}</p>` : ""}`;
    };
    // Sealed box: tap the seal, the lid swings open, then donuts can be tapped
    const cbox = $("#cbox");
    const logo = wix("d6231e_9077a0dc3d96405ca1bae4d9ad1a346c~mv2.png", 200);
    const tiles = (n) => Array.from({ length: n }, () => `<img src="${logo}" alt="">`).join("");
    $("#cbox-print").innerHTML = tiles(70); $("#lid-pat").innerHTML = tiles(70); $("#lid-pat-in").innerHTML = tiles(70);
    const openBox = (instant) => {
      if (cbox.dataset.state !== "closed") return;
      cbox.dataset.state = instant ? "open" : "opening";
      $("#cbox-seal").setAttribute("aria-expanded", "true");
      $("#cbox-body").removeAttribute("inert");
      const done = () => { cbox.dataset.state = "open"; if (week.length) showBox(week[0]); };
      instant ? done() : setTimeout(done, 1100);
    };
    $("#cbox-seal").addEventListener("click", () => openBox(reduceMotion));
    if (reduceMotion && week.length) openBox(true);
    $("#donut-box").addEventListener("click", (e) => { const s = e.target.closest(".slot"); if (s) showBox(byId[s.dataset.box]); });
    $("#donut-box").addEventListener("keydown", (e) => {
      const slots = $$(".slot"); const i = slots.indexOf(document.activeElement);
      if (i < 0) return;
      const step = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: 4, ArrowUp: -4 }[e.key];
      if (step) { e.preventDefault(); const n = slots[(i + step + slots.length) % slots.length]; n.focus(); showBox(byId[n.dataset.box]); }
    });

    $("#lineup-also").textContent = data.lineup.also || "";
    if (data.lineup.week_of) $("#lineup-sub").textContent = `Week of ${data.lineup.week_of}. ` + $("#lineup-sub").textContent;
    $("#price-strip").innerHTML = data.prices.map((p) => `<span>${esc(p.item)} $${p.price}</span>`).join("");

    // Flavor library
    const FILTERS = [
      ["all", "All"], ["week", "This week"], ["fruity", "Fruity"], ["chocolate", "Chocolate"],
      ["cookie", "Cookie"], ["filled", "Filled"], ["spirited", "Spirited"], ["classic", "Classics"],
      ["nutfree", "Nut free"], ["pups", "For pups"],
    ];
    let active = "all", query = "";
    $("#chips").innerHTML = FILTERS.map(([k, label]) =>
      `<button class="chip" type="button" data-f="${k}" aria-pressed="${k === "all"}">${label}</button>`).join("");
    $("#flavor-grid").innerHTML = data.flavors.map((f) => `
      <li><button class="fl" type="button" data-id="${f.id}">
        <span class="fl-ghost" aria-hidden="true">${esc(f.name)}</span>
        <img src="${wix(f.img, 400)}" alt="" loading="lazy" decoding="async">
        <span class="fl-name">${esc(f.name)}</span>
        <span class="fl-meta">${thisWeek.has(f.id) ? '<span class="fl-now">This week</span>' : ""}${f.contains ? esc(f.contains) : f.tags.includes("pups") ? "For dogs" : ""}</span>
      </button></li>`).join("");

    // Flavor picker: mood + style + topping + booze, nut-free, this week or the full rotation
    const pick = { mood: null, style: "any", texture: "any", boozy: "any", nonuts: false, scope: "week", page: 0 };
    let seed = Math.random();
    const jitter = (id) => { let h = 0; for (const c of id) h = (h * 31 + c.charCodeAt(0)) % 9973; return ((h * 9301 + seed * 49297) % 233280) / 233280; };
    const runPicker = () => {
      if (!pick.mood) return;
      const pool = data.flavors.filter((f) => !f.tags.includes("pups") && !(pick.nonuts && f.tags.includes("nuts")) && (pick.scope === "all" || thisWeek.has(f.id)));
      const want = [["mood", 3], ["style", 2], ["texture", 1.5], ["boozy", 2]].filter(([k]) => pick[k] !== "any");
      const hit = (f, k) => k === "mood" ? (f.profile || []).includes(pick.mood) : k === "boozy" ? (pick.boozy === "yes") === !!f.boozy : f[k] === pick[k];
      const max = want.reduce((s, [, w]) => s + w, 0);
      const ranked = pool.map((f) => {
        const s = want.reduce((acc, [k, w]) => acc + (hit(f, k) ? w : 0), 0);
        return { f, s, perfect: s === max, tie: (pick.scope === "all" && thisWeek.has(f.id) ? .3 : 0) + jitter(f.id) * .25 };
      }).filter((r) => r.s > 0).sort((a, b) => (b.s + b.tie) - (a.s + a.tie));
      const perfect = ranked.filter((r) => r.perfect).length;
      const pages = Math.max(1, Math.ceil(ranked.length / 3));
      const show = ranked.slice((pick.page % pages) * 3, (pick.page % pages) * 3 + 3);
      $("#picker-results").innerHTML = show.length ? show.map((r) => `
        <button class="pk" type="button" data-id="${r.f.id}">
          <img src="${wix(r.f.img, 300)}" alt="" loading="lazy">
          <span class="pk-name">${esc(r.f.name)}</span>
          <span class="pk-meta">${r.perfect ? "Perfect match" : "Close match"} · ${thisWeek.has(r.f.id) ? "in the case this week" : "in the rotation"}</span>
        </button>`).join("") : "";
      const note = !ranked.length
        ? (pick.scope === "week" ? "Nothing in the case this week fits all of that. Try Any flavor." : "Nothing fits all of that. Loosen one answer.")
        : pick.scope === "week" && perfect < 3
          ? `${perfect === 0 ? "No" : perfect === 1 ? "Only one" : "Only two"} perfect ${perfect === 1 ? "match" : "matches"} in the case this week. Switch to Any flavor to see more.`
          : `${perfect} perfect ${perfect === 1 ? "match" : "matches"}${pick.scope === "all" ? " across the rotation" : " this week"}.`;
      $("#picker-note").textContent = note;
      $("#picker-more").hidden = ranked.length <= 3;
      $("#picker-out").hidden = false;
    };
    $$("[data-pick]").forEach((b) => b.addEventListener("click", () => {
      const [q, v] = b.dataset.pick.split(":"); pick[q] = v; pick.page = 0; seed = Math.random();
      $$(`[data-pick^="${q}:"]`).forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      runPicker();
    }));
    $$("[data-scope]").forEach((b) => b.addEventListener("click", () => {
      pick.scope = b.dataset.scope; pick.page = 0;
      $$("[data-scope]").forEach((x) => x.setAttribute("aria-checked", String(x === b)));
      runPicker();
    }));
    $("#picker-more").addEventListener("click", () => { pick.page++; runPicker(); });
    $("#pick-nonuts").addEventListener("change", (e) => { pick.nonuts = e.target.checked; pick.page = 0; runPicker(); });
    const apply = () => {
      let n = 0;
      $$("#flavor-grid li").forEach((li) => {
        const f = byId[li.firstElementChild.dataset.id];
        const tagOk =
          active === "all" ? true :
          active === "week" ? thisWeek.has(f.id) :
          active === "nutfree" ? !f.tags.includes("nuts") && !f.tags.includes("pups") :
          f.tags.includes(active);
        const qOk = !query || (f.name + " " + f.desc).toLowerCase().includes(query);
        const show = tagOk && qOk;
        li.hidden = !show; if (show) n++;
      });
      $("#flavor-count").textContent = `${n} flavor${n === 1 ? "" : "s"}`;
    };
    $("#chips").addEventListener("click", (e) => {
      const b = e.target.closest(".chip"); if (!b) return;
      active = b.dataset.f;
      $$(".chip").forEach((c) => c.setAttribute("aria-pressed", String(c === b)));
      apply();
    });
    $("#flavor-search").addEventListener("input", (e) => { query = e.target.value.trim().toLowerCase(); apply(); });
    const preset = new URLSearchParams(location.search).get("filter");
    if (preset && FILTERS.some(([k]) => k === preset)) {
      active = preset;
      $$(".chip").forEach((c) => c.setAttribute("aria-pressed", String(c.dataset.f === preset)));
      setTimeout(() => $("#flavors").scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" }), 250);
    }
    apply();

    // Flavor dialog
    const dlg = $("#flavor-dialog");
    // Flavor card: opens on a sheet of Cloudy deli paper
    const LOGO_ID = "d6231e_9077a0dc3d96405ca1bae4d9ad1a346c~mv2.png";
    let printed = false;
    const tear = (y0, dir) => {
      const pts = []; let x = 0;
      while (x < 100) { x = Math.min(100, x + 1.5 + Math.random() * 3); pts.push(`${x.toFixed(2)}% ${(y0 + dir * Math.random() * .45).toFixed(2)}%`); }
      return pts;
    };
    const openFlavor = (f) => {
      if (!printed) {
        const logo = wix(LOGO_ID, 200);
        $("#fd-print").innerHTML = Array.from({ length: 120 }, () => `<img src="${logo}" alt="">`).join("");
        printed = true;
      }
      $("#fd-paper").style.clipPath = `polygon(0% .3%, ${tear(.15, 1).join(",")}, 100% 99.7%, ${tear(99.85, -1).reverse().join(",")}, 0% 99.7%)`;
      $("#fd-img").src = wix(f.img, 700); $("#fd-img").alt = f.name;
      $("#fd-name").textContent = f.name;
      $("#fd-desc").textContent = f.desc;
      $("#fd-contains").textContent = f.contains || "";
      $("#fd-badge").hidden = !thisWeek.has(f.id);
      const sheet = $("#fd-sheet"); sheet.classList.remove("play"); void sheet.offsetWidth; sheet.classList.add("play");
      if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
    };
    document.addEventListener("click", (e) => {
      const card = e.target.closest("[data-id]"); if (!card) return;
      const f = byId[card.dataset.id]; if (f) openFlavor(f);
    });
    dlg.addEventListener("click", (e) => { if (e.target === dlg || e.target.classList.contains("sheet-wrap")) dlg.close(); });
    const deep = new URLSearchParams(location.search).get("f");
    if (deep && byId[deep]) setTimeout(() => openFlavor(byId[deep]), 300);

    // Site search
    setupSearch(data, thisWeek, byId, openFlavor);

    // Locations
    // Locations: cards (with a map) render once; open/closed status refreshes every minute
    $("#loc-grid").innerHTML = data.locations.map((l) => {
      const q = encodeURIComponent("Cloudy Donut Co, " + l.address);
      return `<li class="loc-card reveal in" data-loc="${l.id}">
        <div class="loc-map" data-lat="${l.lat}" data-lng="${l.lng}" role="group" aria-label="Map of Cloudy Donut ${esc(l.name)}, ${esc(l.address)}"></div>
        <p class="open-in"><span>Open in</span>
          <a href="https://www.google.com/maps/dir/?api=1&destination=${q}" target="_blank" rel="noopener">Google Maps</a>
          <a href="https://maps.apple.com/?q=${encodeURIComponent("Cloudy Donut Co")}&daddr=${encodeURIComponent(l.address)}" target="_blank" rel="noopener">Apple Maps</a>
          <a href="https://waze.com/ul?ll=${l.lat},${l.lng}&navigate=yes" target="_blank" rel="noopener">Waze</a>
        </p>
        <h3>${esc(l.name)}</h3>
        <p class="loc-city">${esc(l.city)}</p>
        <p class="loc-status"></p>
        <address>${esc(l.address)}</address>
        <p class="fine" style="margin:0">${esc(l.hours_label)}</p>
        ${l.note ? `<p class="loc-note">${esc(l.note)}</p>` : ""}
        <div class="loc-actions">
          <a href="tel:+1${l.phone.replace(/\D/g, "")}">Call</a>
          ${Object.keys(l.hours).length ? `<a href="${data.links.order || "#"}" data-order>Order ahead</a>` : `<a href="pop-ups.html">See pop-ups</a>`}
        </div>
      </li>`;
    }).join("");
    const refreshStatus = () => {
      data.locations.forEach((l) => {
        const s = status(l);
        $(`[data-loc="${l.id}"] .loc-status`).innerHTML = `<span class="dot ${s.open ? "on" : ""}"></span>${esc(s.text)}`;
      });
      const openLoc = data.locations.map((l) => [l, status(l)]).find(([, s]) => s.open);
      const hero = $("#hero-status");
      const lc = (t) => t.charAt(0).toLowerCase() + t.slice(1);
      if (openLoc) hero.innerHTML = `<span class="dot on"></span><span class="on-txt">${esc(openLoc[0].name)} is ${esc(lc(openLoc[1].text))}</span>`;
      else {
        const next = data.locations.map((l) => [l, status(l)]).find(([l]) => Object.keys(l.hours).length);
        hero.innerHTML = next ? `<span class="dot"></span><span class="on-txt">${esc(next[0].name)} ${esc(lc(next[1].text))}</span>` : "";
      }
    };
    refreshStatus();
    window.__cdRefresh = refreshStatus;
    setInterval(refreshStatus, 60000);
    setupMaps();
    setupIG(data);

    // Order links: placeholder until the real ordering link is confirmed
    document.addEventListener("click", (e) => {
      const a = e.target.closest("[data-order]");
      if (a && !data.links.order) { e.preventDefault(); alertSoft(a, "Ordering link goes here once confirmed."); }
    });

    // Tour
    // Marquee
    // This week's lineup first, then fan favorites. Kept to 18 names so the strip stays light enough for phones.
    const lineupIds = new Set((data.lineup && data.lineup.flavors) || []);
    const pool = data.flavors.filter((f) => !f.tags.includes("pups"));
    const picked = [...pool.filter((f) => lineupIds.has(f.id)), ...pool.filter((f) => !lineupIds.has(f.id))].slice(0, 18);
    const names = picked.map((f) => `<span>${esc(f.name)}</span>`).join("");
    const mq = $("#marquee");
    mq.innerHTML = names + names;
    mq.style.animationDuration = Math.round(60 * picked.length / 42) + "s";

    // Pop-ups: next dated stop becomes the flyer
    const todayISO = new Intl.DateTimeFormat("en-CA", { timeZone: TZ }).format(new Date());
    const stops = data.tour.stops.slice().sort((a, b) => (a.date || "9999") < (b.date || "9999") ? -1 : 1);
    const upcoming = stops.filter((s) => s.date && s.date >= todayISO && s.status !== "sold_out");
    const next = upcoming[0];
    const fmtDate = (iso) => new Date(iso + "T12:00:00").toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
    const ord = (d) => { const s = ["th", "st", "nd", "rd"], v = d % 100; return d + (s[(v - 20) % 10] || s[v] || s[0]); };
    const flyerDate = (iso) => { const d = new Date(iso + "T12:00:00"); return `${d.toLocaleDateString("en-US", { weekday: "long" })}, ${d.toLocaleDateString("en-US", { month: "long" })} ${ord(d.getDate())}`; };
    if (data.links.flyer_image) $("#flyer").style.setProperty("--flyer-img", `url("${wix(data.links.flyer_image, 1400)}")`);
    if (next) {
      $("#popups-h").textContent = next.city.split(",")[0];
      $("#flyer-bottom").innerHTML = `<span>${esc(next.address || next.venue || next.city)}</span><span class="r">${esc(next.time || "")}<br>${esc(flyerDate(next.date))}</span>`;
      const days = Math.round((new Date(next.date + "T12:00:00") - new Date(todayISO + "T12:00:00")) / 864e5);
      $("#flyer-count").textContent = days === 0 ? "Today" : days === 1 ? "Tomorrow" : `In ${days} days`;
      $("#hero-popup").textContent = `Next pop-up: ${next.city.split(",")[0]}`;
    } else {
      $("#flyer-bottom").innerHTML = `<span>New cities announced on Instagram</span><span class="r">@cloudydonuts</span>`;
    }
    $("#tour-list").innerHTML = stops.map((s) => {
      const isNext = next && s === next;
      const past = s.date && s.date < todayISO;
      if (past) return "";
      const when = s.date ? [fmtDate(s.date), s.time, s.address].filter(Boolean).map(esc).join(" · ") : "Date and venue announced on Instagram";
      const badge = s.status === "sold_out" ? ["sold", "Sold out"] : isNext ? ["next", "Next up"] : s.date ? ["", "Announced"] : ["", "Coming soon"];
      return `<li><span class="tour-city">${esc(s.city)}</span><span class="tour-badge ${badge[0]}">${badge[1]}</span><span class="tour-when">${when}</span></li>`;
    }).join("");

    hydrateImages();
    observeReveals();
    landOnHash();
  }).catch(() => {
    $("#box-detail").innerHTML = '<p class="fine">The lineup will be back shortly.</p>';
  });

  /* ---------- Soft inline notice ---------- */
  function alertSoft(anchor, msg) {
    let tip = anchor.parentElement.querySelector(".soft-tip");
    if (!tip) { tip = document.createElement("span"); tip.className = "soft-tip fine"; tip.style.flexBasis = "100%"; anchor.parentElement.appendChild(tip); }
    tip.textContent = msg;
  }

  /* ---------- Forms ---------- */
  const eventDate = $("#event-date");
  if (eventDate) {
    const d = new Date(); d.setDate(d.getDate() + 14);
    eventDate.min = d.toISOString().slice(0, 10);
  }
  const DONE = {
    newsletter: "You're on the list. The lineup lands every week.",
    tour_alert: "Got it. You'll hear when Cloudy is headed your way.",
    ship_waitlist: "You're on the waitlist. You'll hear first.",
    catering: "Request sent. We'll reply with menu options.",
  };
  $$("form[data-form]").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const msg = $(".form-msg", form);
      msg.classList.remove("err");
      const bad = $$("[required]", form).find((el) => !el.checkValidity());
      if (bad) {
        msg.textContent = bad.type === "checkbox" ? "Please agree to the email terms to sign up." : bad.type === "email" ? "Please enter a valid email." : bad.type === "date" && bad.validity.rangeUnderflow ? "Please choose a date at least 14 days out." : "Please fill in the required fields.";
        msg.classList.add("err"); bad.focus(); return;
      }
      const btn = $("button[type=submit]", form); btn.disabled = true;
      const fields = Object.fromEntries(new FormData(form).entries());
      let saved = false;
      try {
        const r = await fetch("/api/submit", {
          method: "POST", headers: { "content-type": "application/json" },
          body: JSON.stringify({ form: form.dataset.form, fields }),
        });
        saved = r.ok;
      } catch (err) {}
      msg.textContent = DONE[form.dataset.form] + (saved ? "" : " (Concept preview: nothing was saved.)");
      form.reset(); btn.disabled = false;
    });
  });

  /* ---------- Reveal on scroll ---------- */
  function observeReveals() {
    const els = $$(".head-row, .slot, .fl, .founder, .firsts li, .press-list li, .loc-card, .exp-grid > *, .ship-card > *, .faq details, .display-xl");
    if (reduceMotion || !("IntersectionObserver" in window)) return;
    els.forEach((el) => el.classList.add("reveal"));
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
    }), { rootMargin: "0px 0px -8% 0px" });
    els.forEach((el) => io.observe(el));
  }

  /* ---------- Maps: Leaflet + CARTO tiles, with a donut for a pin ---------- */
  let leafletReady;
  const loadLeaflet = () => leafletReady || (leafletReady = new Promise((res, rej) => {
    const css = document.createElement("link"); css.rel = "stylesheet"; css.href = "assets/leaflet/leaflet.css"; document.head.appendChild(css);
    const js = document.createElement("script"); js.src = "assets/leaflet/leaflet.js"; js.onload = () => res(window.L); js.onerror = rej; document.head.appendChild(js);
  }));
  // CARTO Voyager tiles need a key (Cloudflare variable CARTO_API_KEY, served by /api/config).
  // Without one (local preview), fall back to standard OpenStreetMap tiles.
  let configReady;
  const getConfig = () => configReady || (configReady = fetch("/api/config").then((r) => (r.ok ? r.json() : {})).catch(() => ({})));
  const tileLayerFor = (L) => getConfig().then((cfg) => cfg.cartoKey
    ? L.tileLayer(`https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png?key=${encodeURIComponent(cfg.cartoKey)}`, {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
      })
    : L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }));
  function setupMaps() {
    const boxes = $$(".loc-map[data-lat]");
    if (!boxes.length) return;
    const init = (el) => loadLeaflet().then((L) => {
      if (el._map) return;
      const ll = [+el.dataset.lat, +el.dataset.lng];
      const map = L.map(el, { center: ll, zoom: 16, scrollWheelZoom: false, dragging: !L.Browser.mobile, tap: false, zoomControl: true, attributionControl: true });
      tileLayerFor(L).then((layer) => layer.addTo(map));
      const icon = L.divIcon({ className: "donut-pin", iconSize: [56, 62], iconAnchor: [28, 56], html: '<span class="dp-shadow"></span><span class="dp-donut"></span>' });
      L.marker(ll, { icon, keyboard: false }).addTo(map);
      map.attributionControl.setPrefix('<a href="https://leafletjs.com">Leaflet</a>');
      el._map = map;
    }).catch(() => { el.classList.add("map-failed"); });
    if (!("IntersectionObserver" in window)) return boxes.forEach(init);
    const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { init(e.target); io.unobserve(e.target); } }), { rootMargin: "200px" });
    boxes.forEach((b) => io.observe(b));
  }

  /* ---------- Site search ---------- */
  const PAGES = [
    { t: "This week's lineup", d: "The flavors in the case this weekend", u: "index.html#lineup", k: "lineup weekend this week menu" },
    { t: "All flavors", d: "The full rotation, with allergens", u: "flavors.html", k: "flavors menu donuts list allergens" },
    { t: "Pop-up tour", d: "Next stop, dates and city signups", u: "pop-ups.html", k: "pop up popup tour events city" },
    { t: "Our story", d: "Firsts, intention and Worlds of Black luxury", u: "our-story.html", k: "story about founders history black owned derrick zewiditu brown collective 7streams" },
    { t: "Experiences", d: "Cloudy Donut Minis for events and catering", u: "experiences.html", k: "catering events party wedding minis order large" },
    { t: "Cake shipping waitlist", d: "Pound cakes, shipped, coming next year", u: "experiences.html#ship", k: "ship shipping delivery mail cake pound waitlist" },
    { t: "Locations & hours", d: "Brooklyn Heights, NoLita and Baltimore", u: "locations.html", k: "locations hours address directions open shop store" },
  ];
  const FAQS = [
    ["Are your donuts gluten free?", "gluten celiac wheat"],
    ["Which donuts have nuts?", "nuts allergy peanut almond pistachio"],
    ["What replaces eggs and dairy?", "vegan eggs dairy applesauce coconut oil shortening fried"],
    ["How long do they keep?", "storage shelf life fresh keep"],
    ["What if I forget to pick up a preorder?", "preorder pickup doordash grubhub forgot"],
    ["Do you ship?", "ship shipping mail"],
    ["Do you make custom donuts?", "custom special order holiday"],
    ["Something for the dog?", "dog pup pet"],
    ["Gift cards?", "gift card"],
    ["How can I apply for a job?", "job hiring work apply career"],
  ];
  const TAG_WORDS = { nuts: "nuts nut", fruity: "fruit fruity", chocolate: "chocolate", cookie: "cookie", filled: "filled", spirited: "boozy alcohol spirited rum wine", classic: "classic plain sugar", pups: "dog pup pet" };

  function setupSearch(data, thisWeek, byId, openFlavor) {
    const sd = $("#search-dialog"), input = $("#site-search"), box = $("#search-results"), hint = $("#search-hint");
    const items = [];
    data.flavors.forEach((f) => items.push({
      type: "Flavor", t: f.name, d: f.contains ? f.contains : thisWeek.has(f.id) ? "On this week's lineup" : "Vegan",
      img: wix(f.img, 120), key: [f.name, f.desc, ...f.tags.map((g) => TAG_WORDS[g] || g), f.tags.includes("nuts") ? "" : "nut free nutfree", thisWeek.has(f.id) ? "this week" : ""].join(" "),
      go: () => { if (document.body.classList.contains("page-flavors") || document.body.classList.contains("page-index")) { sd.close(); openFlavor(f); } else location.href = `flavors.html?f=${f.id}`; },
    }));
    data.locations.forEach((l) => items.push({ type: "Shop", t: l.name, d: `${l.address} · ${l.hours_label}`, key: [l.name, l.city, l.address, "shop location hours"].join(" "), go: () => (location.href = "locations.html") }));
    data.tour.stops.forEach((s) => items.push({ type: "Pop-up", t: s.city, d: s.date ? [s.date, s.time, s.address].filter(Boolean).join(" · ") : "Date announced on Instagram", key: [s.city, s.address, "pop up popup tour"].join(" "), go: () => (location.href = "pop-ups.html") }));
    PAGES.forEach((p) => items.push({ type: "Page", t: p.t, d: p.d, key: [p.t, p.d, p.k].join(" "), go: () => { sd.close(); location.href = p.u; } }));
    FAQS.forEach(([q, k]) => items.push({ type: "Question", t: q, d: "Good to know", key: q + " " + k, go: () => (location.href = "locations.html#faq") }));

    // Quick menu shown before anyone types: the things people come to the site for
    const go = (u) => () => { sd.close(); location.href = u; };
    const todayISO = new Intl.DateTimeFormat("en-CA", { timeZone: TZ }).format(new Date());
    const nextStop = data.tour.stops.filter((s) => s.date && s.date >= todayISO).sort((a, b) => (a.date < b.date ? -1 : 1))[0];
    const openShop = data.locations.map((l) => [l, status(l)]).find(([, s]) => s.open);
    const firstShop = data.locations.find((l) => Object.keys(l.hours).length);
    const weekNames = data.lineup.flavors.map((id) => byId[id] && byId[id].name).filter(Boolean);
    const QUICK = [
      ["Right now", [
        { icon: "◎", t: "This week's lineup", d: weekNames.slice(0, 3).join(", ") + (weekNames.length > 3 ? ` + ${weekNames.length - 3} more` : ""), go: go("index.html#lineup") },
        { icon: "◷", t: "Hours & locations", d: openShop ? `${openShop[0].name} is open now` : firstShop ? `${firstShop.name}: ${status(firstShop).text}` : "Brooklyn Heights, NoLita, Baltimore", go: go("locations.html") },
        nextStop && { icon: "✦", t: `Next pop-up: ${nextStop.city.split(",")[0]}`, d: [new Date(nextStop.date + "T12:00:00").toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" }), nextStop.time].filter(Boolean).join(" · "), go: go("pop-ups.html") },
        { icon: "↗", t: "Order ahead for pickup", d: "Skip the weekend line", go: go("locations.html") },
      ].filter(Boolean)],
      ["Popular", [
        { icon: "", t: "Nut-free flavors", d: "Every flavor without nuts", go: go("flavors.html?filter=nutfree") },
        { icon: "", t: "Boozy flavors", d: "Rum, rosé, champagne and more", go: go("flavors.html?filter=spirited") },
        { icon: "", t: "Something for the dog", d: "Lil Bow Wow and Snoop Doggy Donut", go: go("flavors.html?filter=pups") },
        { icon: "", t: "Catering & events", d: "Cloudy Donut Minis for your event", go: go("experiences.html") },
        { icon: "", t: "Ship a pound cake", d: "Join the waitlist", go: go("experiences.html#ship") },
      ]],
      ["Questions", [
        { icon: "?", t: "Are the donuts gluten free?", d: "Good to know", go: go("locations.html#faq") },
        { icon: "?", t: "How long do they keep?", d: "Good to know", go: go("locations.html#faq") },
      ]],
    ];
    const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9& ]/g, " ");
    items.forEach((i) => { i.n = norm(i.t); i.k = norm(i.key); });
    const score = (i, q) => {
      const words = q.split(/\s+/).filter(Boolean);
      let s = 0;
      for (const w of words) {
        if (i.n.startsWith(w)) s += 6; else if (i.n.includes(" " + w)) s += 4; else if (i.n.includes(w)) s += 3;
        else if (i.k.includes(w)) s += 1; else return 0;
      }
      return s + (i.type === "Flavor" ? .5 : 0);
    };
    let results = [], active = -1;
    const render = () => {
      const q = norm(input.value).trim();
      hint.hidden = !!q;
      if (!q) {
        results = QUICK.flatMap(([, list]) => list);
        active = 0;
        let ix = 0;
        box.innerHTML = QUICK.map(([group, list]) => `<p class="sr-group">${group}</p>` + list.map((r) => {
          const i = ix++;
          return `<button type="button" class="sr sr-quick" role="option" id="sr-${i}" aria-selected="${i === 0}" data-ix="${i}">
            <span class="sr-icon" aria-hidden="true">${r.icon}</span>
            <span class="sr-text"><span class="sr-t">${esc(r.t)}</span><span class="sr-d">${esc(r.d)}</span></span>
            <span class="sr-type" aria-hidden="true">→</span>
          </button>`;
        }).join("")).join("");
        input.setAttribute("aria-activedescendant", "sr-0");
        requestAnimationFrame(cue);
        return;
      }
      results = items.map((i) => [i, score(i, q)]).filter(([, s]) => s > 0).sort((a, b) => b[1] - a[1]).slice(0, 12).map(([i]) => i);
      active = results.length ? 0 : -1;
      box.innerHTML = results.length ? results.map((r, ix) => `
        <button type="button" class="sr" role="option" id="sr-${ix}" aria-selected="${ix === active}" data-ix="${ix}">
          ${r.img ? `<img src="${r.img}" alt="">` : `<span class="sr-icon" aria-hidden="true">${r.type[0]}</span>`}
          <span class="sr-text"><span class="sr-t">${esc(r.t)}</span><span class="sr-d">${esc(r.d)}</span></span>
          <span class="sr-type">${r.type}</span>
        </button>`).join("") : `<p class="sr-empty">Nothing for "${esc(input.value)}". Try a flavor, a city or a question.</p>`;
      input.setAttribute("aria-activedescendant", active >= 0 ? "sr-0" : "");
      box.scrollTop = 0; requestAnimationFrame(cue);
    };
    const more = $("#sr-more");
    const cue = () => { more.hidden = box.scrollHeight - box.scrollTop - box.clientHeight < 12; };
    box.addEventListener("scroll", cue, { passive: true });
    more.addEventListener("click", () => box.scrollBy({ top: box.clientHeight * .7, behavior: reduceMotion ? "auto" : "smooth" }));
    const setActive = (n) => {
      if (!results.length) return;
      active = (n + results.length) % results.length;
      $$(".sr", box).forEach((b, ix) => b.setAttribute("aria-selected", String(ix === active)));
      const el = $(`#sr-${active}`); el.scrollIntoView({ block: "nearest" });
      input.setAttribute("aria-activedescendant", `sr-${active}`);
    };
    const open = () => { if (sd.showModal) sd.showModal(); input.value = ""; render(); setTimeout(() => input.focus(), 30); };
    $$(".search-open").forEach((b) => b.addEventListener("click", () => { nav.classList.remove("open"); document.body.style.overflow = ""; open(); }));
    $(".search-close").addEventListener("click", () => sd.close());
    sd.addEventListener("click", (e) => { if (e.target === sd) sd.close(); });
    input.addEventListener("input", render);
    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); setActive(active + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); setActive(active - 1); }
      else if (e.key === "Enter" && results[active]) { e.preventDefault(); results[active].go(); }
    });
    box.addEventListener("click", (e) => { const b = e.target.closest(".sr"); if (b) results[+b.dataset.ix].go(); });
    document.addEventListener("keydown", (e) => {
      const typing = /input|textarea|select/i.test(document.activeElement.tagName);
      if ((e.key === "/" && !typing) || (e.key.toLowerCase() === "k" && (e.metaKey || e.ctrlKey))) { e.preventDefault(); open(); }
    });
  }
  // Links that open a new tab say so to screen readers
  const markNewTabs = (root = document) => $$('a[target="_blank"]', root).forEach((a) => {
    if (a.querySelector(".nt")) return;
    a.insertAdjacentHTML("beforeend", '<span class="visually-hidden nt"> (opens in a new tab)</span>');
  });
  markNewTabs();
  new MutationObserver(() => markNewTabs()).observe(document.body, { childList: true, subtree: true });
  hydrateImages();
})();
