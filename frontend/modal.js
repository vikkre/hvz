const modal = document.getElementById('myModal')
const close = modal.querySelector('.close')
const product_name = modal.querySelector('#confirm_product_name')
const yes = modal.querySelector('#confirmDelete')
const no = modal.querySelector('#denyDelete')

function hideModal() {
  modal.style.display = 'none'
}

export function ShowModal(text, yes_function) {
  window.onclick = event => {
    if (event.target == modal) {
      hideModal()
    }
  }
  close.onclick = () => hideModal()
  no.onclick = () => hideModal()
  if (yes_function) {
    yes.onclick = () => {
      hideModal()
      yes_function()
    }
  }

  product_name.innerText = text
  modal.style.display = 'block'
}


export function ShowSnack(text, color = 'var(--color') {
  Toastify({
    text: text,
    duration: 5000,
    close: true,
    gravity: 'bottom', // `top` or `bottom`
    position: 'right', // `left`, `center` or `right`
    backgroundColor: color,
    stopOnFocus: true, // Prevents dismissing of toast on hover
  }).showToast()
}
