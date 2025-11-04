const OnDocumentReady = (fn) => {
  if (!fn || typeof fn !== "function") return;
  document.addEventListener("DOMContentLoaded", fn, { once: true });
};

OnDocumentReady(() => {});

function toggleNav() {
  const nav_main = document.getElementById("nav-ul-main");
  const nav_close_container = document.getElementById("nav-close");

  if (
    nav_main &&
    nav_close_container &&
    nav_main.classList.contains("nav-r-opened")
  ) {
    nav_close_container.classList.remove("open");
    nav_main.classList.remove("nav-r-opened");
  } else {
    nav_close_container.classList.add("open");
    nav_main.classList.add("nav-r-opened");
  }
}
