function showPreview(elem, picture) {
    // Добавляет стили на блоки превью для аватарки при передачи в функцию пути
    elem.setAttribute("style", "\
    display:block;\
    background-image:url(" + picture + ");\
    background-repeat: no-repeat;\
    background-position: center center;\
    background-size: cover;")
}

function openPersonalForm() {
  let overlay = document.querySelector('[popup-element="overlay"]')
  let personalFormWrapper = overlay.querySelector('[form-name="personal"]')

  overlay.classList.add('show')
  personalFormWrapper.classList.add('show')

  let csrfToken = getCookie('csrftoken')

  fetch('/account/', {
    method: "OPEN_FORM",
    headers: {
      'X-CSRFToken': csrfToken
    }
  })
    .then((response) => response.json())
    .then(function (data) {
      personalFormWrapper.innerHTML = data.participant_form
    })
}

function closePersonalForm() {
  personalFormWrapper.classList.remove('show');
  overlay.classList.remove('show')
}

let openPersonalFormButton = document.querySelectorAll('[window-elem="open_personal_form"]')

if (openPersonalFormButton.length > 0) {
  openPersonalFormButton.forEach(openButton => {
    openButton.addEventListener('click', openPersonalForm)
  })
}

function sendPersonalForm(formWrapper) {
  let form = formWrapper.querySelector('form')
  let data = new FormData(form)
  data.append('personal', '')

  let csrfToken = getCookie('csrftoken')

  fetch('/account/', {
    method: "POST",
    body: data,
    headers: {
      'X-CSRFToken': csrfToken
    }
  })
    .then((response) => response.json())
    .then(function (data) {
      console.log(data)
      if (data.status == 'ok'){
        window.location.reload()
      } else if (data.status == 'error') {
        formWrapper.innerHTML = data.participant_form
      }
    })
}

let personalFormWrapper = document.querySelector('[popup-element="popup"][form-name="personal"]')
if (personalFormWrapper) {

  personalFormWrapper.addEventListener('click', function (event) {
    let target = event.target

    if (target.getAttribute('popup-element') == 'close') {
      closePersonalForm()
    }
  })

  personalFormWrapper.addEventListener('change', function(event) {
    let target = event.target

    let avatarPreview = personalFormWrapper.querySelector('[window-elem="avatar_preview"]')

    if (target.getAttribute('window-elem') == 'input_avatar'){
      if(target.files[0]) {
        let fileReader = new FileReader();
        let customInputAvatar = personalFormWrapper.querySelector('[window-elem="custom_input_avatar"]')

        fileReader.addEventListener("load", function () {
          if (customInputAvatar) {
            customInputAvatar.setAttribute("style", "border:none")
          }
          let avatar = fileReader.result

          showPreview(avatarPreview, avatar)
        }, false)
        fileReader.readAsDataURL(target.files[0]);
      }
    }
  })

  personalFormWrapper.addEventListener('submit', function(event) {
    event.preventDefault()


    sendPersonalForm(personalFormWrapper)
  })
}