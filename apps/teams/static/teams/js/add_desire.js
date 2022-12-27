function openAddDesireForm() {
  let overlay = document.querySelector('[popup-element="overlay"]')
  let addDesireFormWrapper = overlay.querySelector('[form-name="desire"]')

  overlay.classList.add('show')
  addDesireFormWrapper.classList.add('show')

  let csrfToken = getCookie('csrftoken')
  let data = new FormData()
  data.append('window', 'open')
  fetch('/account/team/add-desire/', {
    method: "POST",
    body: data,
    headers: {
      'X-CSRFToken': csrfToken
    }
  })
    .then((response) => response.json())
    .then(function (data) {
      // console.log(data)
      if (data.status == 'ok') {
        if (data.action == 'window') {
          addDesireFormWrapper.innerHTML = data.window
        }
      }
    })
}

let userToDelete = document.querySelectorAll('[window-elem="delete"]')
let confirmationPopup = document.querySelector('[popup-name="confirmation"]')

function confirmationClose() {
  // Закрывает поп-ап подтверждения удаления друга из команды
  overlay.classList.remove('show')
  confirmationPopup.classList.remove('show')
}

let closeConfirmationButton = document.querySelector('[popup-element="close"]')

if (closeConfirmationButton) {
  closeConfirmationButton.addEventListener("click", function () {
    confirmationClose()
  })
}

userToDelete.forEach(element => element.addEventListener("click", function () {
  // Удаляет друга из команды при клике на крестик с поп-апом
  let userId = element.getAttribute('user-to-delete')
  let csrfToken = getCookie('csrftoken')
  let data = {
    'user_id': userId,
    'is_delete': true
  }

  overlay.classList.add('show')
  confirmationPopup.classList.add('show')

  let popupButtons = document.querySelectorAll('[popup-element]')

  popupButtons.forEach(el => el.addEventListener("click", function () {
    // Подтверждение удаления друга из команды
    let confirm = el.getAttribute("popup-element")

    if (confirm == "confirm") {
      confirmationClose()

      if (data.is_delete) {
        fetch('/account/team/', {
          method: "POST",
          body: JSON.stringify(data),
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
          }
        })
          .then((response) => response.json())
          .then(function (data) {
            if (data.status == 'ok') {
              window.location.reload()
            }
          })
      }
    }
    if (confirm == "deny") {
      confirmationClose()
      data.is_delete = false
    }
  })
  )
}))

function closeAddDesireForm() {
  overlay.classList.remove('show')
  addDesireFormWrapper.classList.remove('show')
  window.location.reload()
}

function submitAddDesireForm(button) {
  let addDesireFormWrapper = button.closest('[popup-element="popup"][form-name="desire"]')
  let addDesireForm = button.closest('[desire-form-elem="form"]')

  let csrfToken = getCookie('csrftoken')
  let data = new FormData(addDesireForm)

  fetch('/account/team/add-desire/', {
    method: "POST",
    body: data,
    headers: {
      'X-CSRFToken': csrfToken
    }
  })
    .then((response) => response.json())
    .then(function (data) {
      // console.log(data)
      if (data.status == 'ok') {
        if (data.action == 'window') {
          addDesireFormWrapper.innerHTML = data.window
        }
      }
    })
}

let openFormAddDesireButton = document.querySelector('[button-action="open-add-desire-form"]')
if (openFormAddDesireButton) {
  openFormAddDesireButton.addEventListener('click', openAddDesireForm)
}
let addDesireFormWrapper = document.querySelector('[popup-element="popup"][form-name="desire"]')
if (addDesireFormWrapper) {
  addDesireFormWrapper.addEventListener('click', function (event) {
    let target = event.target

    if (target.getAttribute('desire-form-elem') == 'button') {
      submitAddDesireForm(target)
    }

    if (target.getAttribute('popup-element') == 'close') {
      closeAddDesireForm()
    }

    if (target.getAttribute('desire-form-elem') == 'phone') {
      let phoneField = document.querySelector('[desire-form-elem="phone"]')
      let maskOptions = {
        mask: '+{7}(000) 000-00-00'
      };
      IMask(phoneField, maskOptions);
    }
  })
  addDesireFormWrapper.addEventListener('submit', function (event) {
    event.preventDefault()
    submitAddDesireForm(event.target)
  })
}
