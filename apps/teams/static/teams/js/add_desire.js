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
      console.log(data)
      if (data.status == 'ok') {
        if (data.action == 'window') {
          addDesireFormWrapper.innerHTML = data.window
        }
      }
    })
}

let userToDelete = document.querySelectorAll('[window-elem="delete"]')

userToDelete.forEach(element => element.addEventListener("click", function () {
  // Удаляет пользователя из команды при клике на крестик
  let userId = element.getAttribute("user-to-delete")
  let csrfToken = getCookie('csrftoken')
  let data = {
    'user_id': userId
  }

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
}))

// let player = document.querySelector(".team_wishlist_items_item")
// player.addEventListener("mouseover", function () {
//   document.querySelector('[window-elem="delete"]').setAttribute("style", "visibility: visible; margin-left: 0;")
// })

function closeAddDesireForm() {
  overlay.classList.remove('show')
  addDesireFormWrapper.classList.remove('show')
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
      console.log(data)
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


