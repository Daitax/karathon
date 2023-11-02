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
      // console.log(data)
      if (data.status == 'ok') {
        if (data.action == 'window') {
          authenticationFormWrapper.innerHTML = data.window
          let email = document.querySelector('[auth-form-elem="email"]')
          email.focus()
        }
      }
    })
}

function closeAuthenticationForm() {
  authenticationFormWrapper.classList.remove('show');
  overlay.classList.remove('show')
}

function submitAuthenticationForm(button) {
  let authenticationFormWrapper = button.closest('[popup-element="popup"][form-name="authentication"]')
  let authenticationForm = button.closest('[auth-form-elem="form"]')

  let csrfToken = getCookie('csrftoken')
  let data = new FormData(authenticationForm)

  if (document.querySelector('[auth-form-elem="button"] > span')) {
    document.querySelector('[auth-form-elem="button"] > span').classList.add("click_opacity")
  }

  fetch('/account/authentication/', {
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
          authenticationFormWrapper.innerHTML = data.window
          let smsCode = document.querySelector('[auth-form-elem="code"]')
          if (smsCode) {
            smsCode.focus()
          }
        }
        if (data.action == 'reload') {
          window.location.reload()
        }
      }
    })
}

let openFormAuthenticationButtons = document.querySelectorAll('[button-action="open-auth-form"]')
  openFormAuthenticationButtons.forEach(element => element.addEventListener('click', openAuthenticationForm)
)

let authenticationFormWrapper = document.querySelector('[popup-element="popup"][form-name="authentication"]')
if (authenticationFormWrapper) {
  authenticationFormWrapper.addEventListener('submit', function (event) {
    event.preventDefault()
    submitAuthenticationForm(event.target)
  })

  authenticationFormWrapper.addEventListener('click', function (event) {
    let target = event.target

    if (target.getAttribute('auth-form-elem') == 'later') {
      closeAuthenticationForm()
      window.location.reload()
    }
    if (target.getAttribute('popup-element') == 'close') {
      closeAuthenticationForm()
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