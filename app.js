/* Cloudy Donut Co. concept, Siani Creates */
(() => {
  const TZ = "America/New_York";
  const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const $ = (s, el = document) => el.querySelector(s);
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
    setTimeout(endIntro, 4300);
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

  /* ---------- Concept panel ---------- */
  const pill = $(".concept-pill"), panel = $("#concept");
  const setPanel = (open) => { panel.hidden = !open; pill.setAttribute("aria-expanded", String(open)); };
  pill.addEventListener("click", () => setPanel(panel.hidden));
  $(".concept-close").addEventListener("click", () => setPanel(false));

  /* ---------- Time helpers (New York) ---------- */
  const nyNow = () => {
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

    // Lineup
    $("#lineup-grid").innerHTML = data.lineup.flavors.map((id) => byId[id]).filter(Boolean).map((f) => `
      <li><button class="lineup-card" type="button" data-id="${f.id}">
        <img src="${wix(f.img, 360)}" alt="" loading="lazy" decoding="async">
        <h3>${esc(f.name)}</h3>
        <span class="tag">${f.contains ? esc(f.contains) : ""}</span>
      </button></li>`).join("");
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
      <li><button class="flavor-card" type="button" data-id="${f.id}">
        ${thisWeek.has(f.id) ? '<span class="now">This week</span>' : ""}
        <img src="${wix(f.img, 300)}" alt="" loading="lazy" decoding="async">
        <span><span class="fc-name">${esc(f.name)}</span><br><span class="fc-meta">${f.contains ? esc(f.contains) : f.tags.includes("pups") ? "For dogs" : "Vegan"}</span></span>
      </button></li>`).join("");
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
    apply();

    // Flavor dialog
    const dlg = $("#flavor-dialog");
    document.addEventListener("click", (e) => {
      const card = e.target.closest("[data-id]"); if (!card) return;
      const f = byId[card.dataset.id]; if (!f) return;
      $("#fd-img").src = wix(f.img, 700); $("#fd-img").alt = f.name;
      $("#fd-name").textContent = f.name;
      $("#fd-desc").textContent = f.desc;
      $("#fd-contains").textContent = f.contains || "";
      $("#fd-badge").hidden = !thisWeek.has(f.id);
      if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
    });
    dlg.addEventListener("click", (e) => { if (e.target === dlg) dlg.close(); });

    // Locations
    const renderLocs = () => {
      $("#loc-grid").innerHTML = data.locations.map((l) => {
        const s = status(l);
        const map = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent("Cloudy Donut " + l.address)}`;
        return `<li class="loc-card reveal in">
          <h3>${esc(l.name)}</h3>
          <p class="loc-city">${esc(l.city)}</p>
          <p class="loc-status"><span class="dot ${s.open ? "on" : ""}"></span>${esc(s.text)}</p>
          <address>${esc(l.address)}</address>
          <p class="fine" style="margin:0">${esc(l.hours_label)}</p>
          <p class="loc-note">${esc(l.note || "")}</p>
          <div class="loc-actions">
            <a href="${map}" target="_blank" rel="noopener">Directions</a>
            <a href="tel:+1${l.phone.replace(/\D/g, "")}">Call</a>
            ${Object.keys(l.hours).length ? `<a href="${data.links.order || "#"}" data-order>Order ahead</a>` : `<a href="#popups">See pop-ups</a>`}
          </div>
        </li>`;
      }).join("");
      const openLoc = data.locations.map((l) => [l, status(l)]).find(([, s]) => s.open);
      const hero = $("#hero-status");
      const lc = (t) => t.charAt(0).toLowerCase() + t.slice(1);
      if (openLoc) hero.innerHTML = `<span class="dot on"></span>${esc(openLoc[0].name)} is ${esc(lc(openLoc[1].text))}`;
      else {
        const next = data.locations.map((l) => [l, status(l)]).find(([l]) => Object.keys(l.hours).length);
        hero.innerHTML = next ? `<span class="dot"></span>${esc(next[0].name)} ${esc(lc(next[1].text))}` : "";
      }
    };
    renderLocs();
    setInterval(renderLocs, 60000);

    // Order links: placeholder until the real ordering link is confirmed
    document.addEventListener("click", (e) => {
      const a = e.target.closest("[data-order]");
      if (a && !data.links.order) { e.preventDefault(); alertSoft(a, "Ordering link goes here once confirmed."); }
    });

    // Tour
    // Marquee
    const names = data.flavors.filter((f) => !f.tags.includes("pups")).map((f) => `<span>${esc(f.name)}</span>`).join("");
    $("#marquee").innerHTML = names + names;

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
      const hp = $("#hero-popup"); if (hp) hp.textContent = `Next pop-up: ${next.city.split(",")[0]}`;
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
  }).catch(() => {
    $("#lineup-grid").innerHTML = '<li class="fine">The lineup will be back shortly.</li>';
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
        msg.textContent = bad.type === "email" ? "Please enter a valid email." : bad.type === "date" && bad.validity.rangeUnderflow ? "Please choose a date at least 14 days out." : "Please fill in the required fields.";
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
    const els = $$(".head-row, .lineup-grid li, .founder, .firsts li, .press-list li, .loc-card, .exp-grid > *, .ship-card > *, .faq details, .display-xl");
    if (reduceMotion || !("IntersectionObserver" in window)) return;
    els.forEach((el) => el.classList.add("reveal"));
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
    }), { rootMargin: "0px 0px -8% 0px" });
    els.forEach((el) => io.observe(el));
  }
  hydrateImages();
})();
