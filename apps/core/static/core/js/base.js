function closePopup(event) {
  let overlay = document.querySelector('[popup-element="overlay"]')
  let popup = document.querySelectorAll('[popup-element="popup"]')

  if (event.target == overlay) {
    if (overlay.querySelector('[reload="True"]')) {
      window.location.reload()
    } else {
      popup.forEach(function (element) {
        element.classList.remove('show')
      })
      overlay.classList.remove('show')
    }
  }
}

let overlay = document.querySelector('[popup-element="overlay"]')

overlay.addEventListener('click', closePopup)