function openAuthenticationForm() {
  let overlay = document.querySelector('[popup-element="overlay"]')
  let authenticationFormWrapper = overlay.querySelector('[form-name="authentication"]')

  overlay.classList.add('show')
  authenticationFormWrapper.classList.add('show')


  let csrfToken = getCookie('csrftoken')
  let data = new FormData()
  data.append('window', 'open')

  fetch('/account/authentication/', {
    method: "POST",
    body: data,
    headers: {
      'X-CSRFToken': csrfToken
    }
  })
    .then((response) => response.json())
    .then(function (data) {
      if (data.status == 'ok') {
        if (data.action == 'window') {
          authenticationFormWrapper.innerHTML = data.window
        }
      }
    })
}

function submitAuthenticationForm(button) {
  let authenticationFormWrapper = button.closest('[popup-element="popup"][form-name="authentication"]')
  let authenticationForm = button.closest('[auth-form-elem="form"]')

  let csrfToken = getCookie('csrftoken')
  let data = new FormData(authenticationForm)

  fetch('/account/authentication/', {
    method: "POST",
    body: data,
    headers: {
      'X-CSRFToken': csrfToken
    }
  })
    .then((response) => response.json())
    .then(function (data) {
      if (data.status == 'ok') {
        if (data.action == 'window') {
          authenticationFormWrapper.innerHTML = data.window
        }
        if (data.action == 'reload') {
          window.location.reload()
        }
      }
    })
}

let openFormAuthenticationButton = document.querySelector('[button-action="open-auth-form"]')
if (openFormAuthenticationButton) {
  openFormAuthenticationButton.addEventListener('click', openAuthenticationForm)
}


let authenticationFormWrapper = document.querySelector('[popup-element="popup"][form-name="authentication"]')
if (authenticationFormWrapper) {
  authenticationFormWrapper.addEventListener('submit', function (event) {
    event.preventDefault()
    submitAuthenticationForm(event.target)
  })

  authenticationFormWrapper.addEventListener('click', function (event) {
    let target = event.target
    if (target.getAttribute('auth-form-elem') == 'button') {
      submitAuthenticationForm(target)
    }
    if (target.getAttribute('auth-form-elem') == 'later') {
    //  TODO Написать функцию закрытия overlay
    }
  })

  authenticationFormWrapper.addEventListener('input', function (event) {
    let target = event.target
    if (target.getAttribute('auth-form-elem') == 'code') {
      if (target.value.length == 4) {
        submitAuthenticationForm(target)
      }

    }
  })
}