"use strict";

document.addEventListener("click", (event) => {
  const control = event.target.closest("[data-confirm]");
  if (control && !window.confirm(control.dataset.confirm)) {
    event.preventDefault();
  }
});

document.addEventListener("submit", (event) => {
  const form = event.target;
  if (
    form instanceof HTMLFormElement &&
    form.dataset.confirm &&
    !window.confirm(form.dataset.confirm)
  ) {
    event.preventDefault();
  }
});
