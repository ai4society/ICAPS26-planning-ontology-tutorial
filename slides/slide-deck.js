const SLIDES = [
  "slide-01-title.html",
  "slide-02-outline.html",
  "slide-03-background-divider.html",
  "slide-04-automated-planning.html",
  "slide-05-pddl-structured.html",
  "slide-06-why-ontology.html",
  "slide-07-ontology-basics.html",
  "slide-08-po-divider.html",
  "slide-09-po-scope.html",
  "slide-10-po-schema-zoom.html",
  "slide-11-competency-questions.html",
  "slide-12-example-kg.html",
  "slide-13-po-workflow.html",
  "slide-14-usecase-planner.html",
  "slide-15-usecase-explanation.html",
  "slide-16-tool-divider.html",
  "slide-17-tool-overview.html",
  "slide-18-tool-demo.html",
  "slide-19-mapo-divider.html",
  "slide-20-mapf-motivation.html",
  "slide-21-mapo-schema.html",
  "slide-22-mapo-schema-zoom.html",
  "slide-23-lifecycle.html",
  "slide-24-pipeline.html",
  "slide-25-omega-grid.html",
  "slide-26-omega-qa.html",
  "slide-27-omega-graph.html",
  "slide-28-evaluation.html",
  "slide-29-conclusion.html",
  "slide-30-future-work.html",
  "slide-31-thankyou.html",
];

const FOOTER_LEFT = "AI4S · AIISC @ University of South Carolina";
const FOOTER_CENTER = "Planning Ontology · ICAPS 2026 Tutorial";

function fitPreview() {
  if (document.body.classList.contains("render-mode")) {
    document.documentElement.style.setProperty("--preview-scale", "1");
    return;
  }
  const width = window.innerWidth - 72;
  const height = window.innerHeight - 72;
  const scale = Math.min(1, width / 1920, height / 1080);
  document.documentElement.style.setProperty("--preview-scale", scale.toFixed(4));
}

function buildDeckNav() {
  const canvas = document.querySelector(".slide-canvas");
  if (!canvas) return;
  const filename = window.location.pathname.split("/").pop();
  const slideIndex = SLIDES.indexOf(filename);
  if (slideIndex === -1) return;

  const nav = document.createElement("nav");
  nav.className = "deck-nav";
  nav.setAttribute("aria-label", "Slide navigation");

  const home = document.createElement("a");
  home.className = "nav-btn nav-home";
  home.href = "./index.html";
  home.textContent = "Deck";
  nav.appendChild(home);

  const prev = document.createElement("a");
  prev.className = "nav-btn";
  prev.href = slideIndex > 0 ? `./${SLIDES[slideIndex - 1]}` : "./index.html";
  prev.textContent = "←";
  prev.setAttribute("aria-label", "Previous slide");
  nav.appendChild(prev);

  const next = document.createElement("a");
  next.className = "nav-btn";
  next.href = slideIndex < SLIDES.length - 1 ? `./${SLIDES[slideIndex + 1]}` : "./index.html";
  next.textContent = "→";
  next.setAttribute("aria-label", "Next slide");
  nav.appendChild(next);

  canvas.appendChild(nav);

  window.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft" && slideIndex > 0) {
      window.location.href = `./${SLIDES[slideIndex - 1]}`;
    }
    if (event.key === "ArrowRight" && slideIndex < SLIDES.length - 1) {
      window.location.href = `./${SLIDES[slideIndex + 1]}`;
    }
  });
}

function buildSlideFooter() {
  const canvas = document.querySelector(".slide-canvas");
  if (!canvas) return;
  const filename = window.location.pathname.split("/").pop();
  const slideIndex = SLIDES.indexOf(filename);
  if (slideIndex === -1) return;
  if (canvas.classList.contains("title-slide")) return; // title has its own band

  const existing = document.querySelector(".slide-footer");
  if (existing) existing.style.display = "none";

  const footer = document.createElement("div");
  footer.className = "runtime-slide-footer";
  const renderMode = document.body.classList.contains("render-mode");
  Object.assign(footer.style, {
    position: renderMode ? "fixed" : "absolute",
    left: "96px", right: "96px", bottom: "40px", zIndex: "6", pointerEvents: "none",
  });

  const rule = document.createElement("div");
  Object.assign(rule.style, { width: "100%", height: "5px", background: "#73000a" });

  const mk = (text, css) => {
    const d = document.createElement("div");
    d.textContent = text;
    Object.assign(d.style, Object.assign({
      position: "absolute", top: "15px", color: "#444444",
      fontFamily: "\"Open Sans\", Arial, sans-serif", fontSize: "15px", lineHeight: "1",
    }, css));
    return d;
  };
  footer.appendChild(rule);
  footer.appendChild(mk(FOOTER_LEFT, { left: "0" }));
  footer.appendChild(mk(FOOTER_CENTER, { left: "50%", transform: "translateX(-50%)" }));
  footer.appendChild(mk(`${String(slideIndex + 1).padStart(2, "0")} / ${String(SLIDES.length).padStart(2, "0")}`,
    { right: "0", fontFamily: "\"Source Code Pro\", monospace" }));
  canvas.appendChild(footer);
}

function ensureStage() {
  const shell = document.querySelector(".preview-shell");
  const canvas = document.querySelector(".slide-canvas");
  if (!shell || !canvas || canvas.parentElement?.classList.contains("slide-stage")) return;
  const stage = document.createElement("div");
  stage.className = "slide-stage";
  shell.insertBefore(stage, canvas);
  stage.appendChild(canvas);
}

function enableRenderMode() {
  const params = new URLSearchParams(window.location.search);
  if (params.get("render") === "1") document.body.classList.add("render-mode");
}

window.addEventListener("DOMContentLoaded", () => {
  enableRenderMode();
  document.body.classList.add("slide-page");
  ensureStage();
  buildDeckNav();
  buildSlideFooter();
  fitPreview();
  window.addEventListener("resize", fitPreview);
});
