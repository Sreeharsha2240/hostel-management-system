"use strict";

document.addEventListener("click", (event) => {
  const control = event.target.closest("[data-confirm]");
  if (
    !control ||
    control instanceof HTMLFormElement ||
    (control.form &&
      ((control instanceof HTMLButtonElement && control.type === "submit") ||
        (control instanceof HTMLInputElement &&
          ["submit", "image"].includes(control.type))))
  ) {
    return;
  }
  if (!window.confirm(control.dataset.confirm)) {
    event.preventDefault();
  }
});

document.addEventListener("submit", (event) => {
  const form = event.target;
  if (!(form instanceof HTMLFormElement)) {
    return;
  }
  const message = event.submitter?.dataset.confirm || form.dataset.confirm;
  if (message && !window.confirm(message)) {
    event.preventDefault();
  }
});
