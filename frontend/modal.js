const modal = document.getElementById("myModal");
const close = modal.querySelector(".close");
const product_name = modal.querySelector("#confirm_product_name");
const yes = modal.querySelector("#confirmDelete");
const no = modal.querySelector("#denyDelete");
const myLogElement = document.getElementById("myLog");

function hideModal() {
  modal.style.display = "none";
}

export function WriteLog(txt) {
  const logEntry = document.createElement("p");
  logEntry.innerText = txt;
  myLogElement.appendChild(logEntry);
}

export function ShowModal(text, yes_function) {
  window.onclick = (event) => {
    if (event.target == modal) {
      hideModal();
    }
  };
  close.onclick = () => hideModal();
  no.onclick = () => hideModal();
  if (yes_function) {
    yes.onclick = () => {
      hideModal();
      yes_function();
    };
  }

  product_name.innerText = text;
  WriteLog(`ShowModal: ${text}`);
  modal.style.display = "block";
}

export function ShowSnack(text, color = "var(--nc-lk-2") {
  WriteLog(`ShowSnack: ${text}`);
  Toastify({
    text: text,
    duration: 5000,
    close: true,
    gravity: "bottom", // `top` or `bottom`
    position: "right", // `left`, `center` or `right`
    backgroundColor: color,
    stopOnFocus: true, // Prevents dismissing of toast on hover
  }).showToast();
}
