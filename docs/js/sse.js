const eventSource = new EventSource("/livereload");

eventSource.onmessage = function (event) {
  if (event.data === "reload") {
    console.log("🔄 LiveReload: Changes detected, reloading page...");
    window.location.reload();
  }
};

eventSource.onerror = function (event) {
  console.log("LiveReload: Connection error", event);
};
