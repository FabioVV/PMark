const OnDocumentReady = (fn) => {
  if (!fn || typeof fn !== "function") return;
  document.addEventListener("DOMContentLoaded", fn, { once: true });
};

OnDocumentReady(() => {
  const nav = document.getElementById("navbar");
});
