function bindFolio() {
  document.querySelectorAll(".folio__name").forEach((button) => {
    button.addEventListener("click", () => {
      const cols = button.nextElementSibling;
      const open = button.getAttribute("aria-expanded") === "true";
      button.setAttribute("aria-expanded", String(!open));
      if (cols) cols.hidden = open;
    });
  });
}

bindFolio();
document.body.addEventListener("htmx:afterSwap", bindFolio);

const form = document.getElementById("run-form");
const sql = document.getElementById("sql");
if (form && sql) {
  sql.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
      event.preventDefault();
      form.requestSubmit();
    }
  });
}
