function closePopup(event) {
  let overlay = document.querySelector('[popup-element="overlay"]')
  let popup = document.querySelectorAll('[popup-element="popup"]')

  if (event.target == overlay) {
    if (overlay.querySelector('[reload="True"]')) {
      window.location.reload()
    } else {
      if (promoVideo) {
        toggleActionVideo('pause', promoVideo)
      }

      popup.forEach(function (element) {
        element.classList.remove('show')
      })
      overlay.classList.remove('show')
      removeButtonsOpacity(".blue_button")
      removeButtonsOpacity(".pink_button")
    }
  }
}

function addButtonsOpacity(btn) {
  // добавляет затемнение названия кнопки после нажатия
  let button = document.querySelectorAll(btn)

  if (button) {
    button.forEach(element => element.addEventListener("click", function () {
      element.firstElementChild.classList.add("click_opacity")
    }))
  }
}

function removeButtonsOpacity(btn) {
  // убирает затемнение названия кнопки
  let button = document.querySelectorAll(btn)

  if (button) {
    button.forEach(element => element.firstElementChild.classList.remove("click_opacity"))
  }
}

addButtonsOpacity(".blue_button")
addButtonsOpacity(".pink_button")

let overlay = document.querySelector('[popup-element="overlay"]')

overlay.addEventListener('click', closePopup)