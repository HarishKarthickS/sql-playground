document.querySelectorAll(".folio__name").forEach((button) => {
  button.addEventListener("click", () => {
    const cols = button.nextElementSibling;
    const open = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!open));
    if (cols) cols.hidden = open;
  });
});
