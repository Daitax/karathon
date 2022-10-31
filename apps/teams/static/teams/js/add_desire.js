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

function submitAddDesireForm(button){
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
  })
  addDesireFormWrapper.addEventListener('submit', function (event) {
    event.preventDefault()
    submitAddDesireForm(event.target)
  })
}