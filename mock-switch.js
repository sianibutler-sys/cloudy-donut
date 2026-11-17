// MOCKUP ONLY: variant switcher. Remove before main.
(function () {
  const q = new URLSearchParams(location.search);
  const hv = q.get("hero") || "n", nv = q.get("nav") || "icons", fv = q.get("firsts") || "a";
  document.documentElement.classList.add("hv-" + hv, "nv-" + nv, "fv-on-" + fv);
  const bar = document.createElement("div"); bar.className = "mock-bar"; bar.setAttribute("role", "region"); bar.setAttribute("aria-label", "Mockup variants");
  const link = (k, v, label) => { const p = new URLSearchParams(location.search); p.set(k, v); const cur = k === "hero" ? hv : k === "nav" ? nv : fv; const on = cur === v; return `<a href="?${p}"${on ? ' aria-current="true"' : ""}>${label}</a>`; };
  bar.innerHTML = `<span>Hero</span>${link("hero","l","L centered")}${link("hero","m","M left")}${link("hero","n","N glow")}<span>Menu</span>${link("nav","icons","Icons")}${link("nav","word","Word")}<span>Firsts</span>${link("firsts","x","Now")}${link("firsts","a","A one 1st")}${link("firsts","b","B seals")}${link("firsts","c","C sentence")}`;
  document.body.appendChild(bar);
})();
