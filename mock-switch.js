// MOCKUP ONLY: variant switcher. Remove before main.
(function () {
  const q = new URLSearchParams(location.search);
  const hv = q.get("hero") || "l", nv = q.get("nav") || "icons";
  document.documentElement.classList.add("hv-" + hv, "nv-" + nv);
  const bar = document.createElement("div"); bar.className = "mock-bar"; bar.setAttribute("role", "region"); bar.setAttribute("aria-label", "Mockup variants");
  const link = (k, v, label) => { const p = new URLSearchParams(location.search); p.set(k, v); const on = (k === "hero" ? hv : nv) === v; return `<a href="?${p}"${on ? ' aria-current="true"' : ""}>${label}</a>`; };
  bar.innerHTML = `<span>Hero</span>${link("hero","l","L centered")}${link("hero","m","M left")}${link("hero","n","N glow")}<span>Menu</span>${link("nav","icons","Icons")}${link("nav","word","Word")}`;
  document.body.appendChild(bar);
})();
