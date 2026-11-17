/* Lightbox: opens a photo full-screen when it's selected.
   Without JavaScript, each photo still links straight to the
   large image file, so nothing breaks and search engines can
   follow the links. Keyboard: ← → to move, Esc to close.      */
(function () {
  const groups = document.querySelectorAll("[data-lightbox]");
  if (!groups.length || typeof HTMLDialogElement !== "function") return;

  const icon = (d) =>
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="${d}"/></svg>`;

  const dlg = document.createElement("dialog");
  dlg.className = "lightbox";
  dlg.setAttribute("aria-label", "Photo viewer");
  dlg.innerHTML = `
    <div class="lb-bar">
      <span class="lb-count" aria-live="polite"></span>
      <button class="lb-btn lb-close" type="button" aria-label="Close">${icon("M6 6l12 12M18 6L6 18")}</button>
    </div>
    <div class="lb-stage">
      <button class="lb-btn lb-prev" type="button" aria-label="Previous photo">${icon("M15 5l-7 7 7 7")}</button>
      <img alt="">
      <button class="lb-btn lb-next" type="button" aria-label="Next photo">${icon("M9 5l7 7-7 7")}</button>
    </div>
    <div class="lb-caption"></div>`;
  document.body.appendChild(dlg);

  const img = dlg.querySelector("img");
  const cap = dlg.querySelector(".lb-caption");
  const count = dlg.querySelector(".lb-count");
  let links = [];
  let index = 0;

  function show(i) {
    index = (i + links.length) % links.length;
    const a = links[index];
    const thumb = a.querySelector("img");
    const fig = a.closest("figure");
    const caption = fig && fig.querySelector("figcaption");
    img.src = a.href;
    img.alt = thumb ? thumb.alt : "";
    if (caption) {
      const span = caption.querySelector("span");
      const title = caption.firstChild ? caption.firstChild.textContent.trim() : "";
      const detail = span ? span.textContent.trim() : "";
      cap.textContent = [title, detail].filter(Boolean).join(", ");
    } else {
      cap.textContent = "";
    }
    count.textContent = `${index + 1} of ${links.length}`;
    const multi = links.length > 1;
    dlg.querySelector(".lb-prev").hidden = !multi;
    dlg.querySelector(".lb-next").hidden = !multi;
  }

  groups.forEach((group) => {
    const groupLinks = Array.from(group.querySelectorAll("a.shot-link"));
    groupLinks.forEach((a, i) => {
      a.addEventListener("click", (e) => {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return; // allow "open in new tab"
        e.preventDefault();
        links = groupLinks;
        show(i);
        dlg.showModal();
      });
    });
  });

  dlg.querySelector(".lb-close").addEventListener("click", () => dlg.close());
  dlg.querySelector(".lb-prev").addEventListener("click", () => show(index - 1));
  dlg.querySelector(".lb-next").addEventListener("click", () => show(index + 1));
  dlg.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") show(index - 1);
    if (e.key === "ArrowRight") show(index + 1);
  });
  // Click on the dark area (not the photo or buttons) closes it.
  dlg.querySelector(".lb-stage").addEventListener("click", (e) => {
    if (e.target === e.currentTarget) dlg.close();
  });
  dlg.addEventListener("close", () => { img.removeAttribute("src"); });
})();
