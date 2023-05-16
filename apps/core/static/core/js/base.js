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

let firstScreenPromo = document.querySelector('[window-elem="first-screen-promo"]')

if (firstScreenPromo) {
  firstScreenPromo.addEventListener("click", function () {
    let promoVideo = document.querySelector('[popup-name="promo-video"]')

    overlay.classList.add('show')
    promoVideo.classList.add("show")

    if (promoVideo) {
      promoVideo.addEventListener('click', function (event) {
        let target = event.target

        if (target.getAttribute('popup-element') == 'close') {
          overlay.classList.remove('show')
          promoVideo.classList.remove("show")
        }
      })
    }

  })
}

let overlay = document.querySelector('[popup-element="overlay"]')

overlay.addEventListener('click', closePopup)