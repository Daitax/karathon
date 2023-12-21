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
}

function isEmpty(obj) {
  // Проверяет пустой ли массив
  for (let key in obj) {
    return false;
  }
  return true;
}

function countNewMessages() {
  // Считает количество непрочитанных сообщений
  let amountMessages = document.querySelectorAll('[window-elem="new_message"]').length
  if (amountMessages == 0) {
    return ""
  }
  return amountMessages
}

function amountMessagesShowed() {
  // Считает количество показанных сообщений
  return document.querySelectorAll('[window-elem="message_item"]').length
}

function hideMarkAllMessagesButton() {
  // Убирает кнопку прочитать все сообщения, если новых сообщений нет
  let amountNewMessages = document.querySelectorAll('[window-elem="new_message"]').length
  if (amountNewMessages == 0) {
    markedAsReadAllButton.classList.remove("show")
  }
}

let newMessages = document.querySelectorAll('[window-elem="new_message"]')
let markedAsReadButton = document.querySelector('[window-elem="marked_as_read"]')
let markedAsReadAllButton = document.querySelector('[window-elem="marked_as_read_all"]')
let data = {}
let markedButtons = []
let previousMessages = document.querySelector('[window-elem="previous_messages"]')
let messageItems = document.querySelector('[window-elem="messages_items_wrapper"]')

window.addEventListener("load", function () {
  if (markedAsReadAllButton) {
    hideMarkAllMessagesButton()
  }
})

function collectData(i) {
  // Собирает id сообщений в массив по клику на них
  i.classList.toggle("touched")
  let newMessageId = i.getAttribute("mes-id")
  if (i.classList.length == 2) {
    data["newMessageId" + newMessageId] = Number(newMessageId)
  } else {
    delete data["newMessageId" + newMessageId]
    if (data["amount"]) {
      delete data["amount"]
    }
  }
  if (!isEmpty(data)) {
    markedAsReadButton.classList.add("show")
  } else {
    markedAsReadButton.classList.remove("show")
  }
}

if (markedAsReadAllButton) {
  markedButtons.push(markedAsReadAllButton)
  markedAsReadAllButton.addEventListener("click", function () {
    // Собирает id всех непрочитанных сообщений в массив по клику на кнопку
    data = {}

    newMessages.forEach(element =>
      element.classList.toggle("touched")
    )
    newMessages.forEach(element =>
      data["newMessageId" + element.getAttribute("mes-id")] = Number(element.getAttribute("mes-id"))
    )
  })
}

if (markedAsReadButton) {
  markedButtons.push(markedAsReadButton)
}

markedButtons.forEach(element => element.addEventListener("click", function () {
  // Передаёт id выбранных сообщений во вьюху для обновления атрибута is_viewed
  data["amount"] = amountMessagesShowed()
  document.querySelector('[window-elem="marked_as_read_all"] > span').classList.add("click_opacity")

  let csrfToken = getCookie('csrftoken')

  fetch('/account/messages/', {
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
        messageItems.innerHTML = data.messages_block
      }
    })
    .then(markedAsReadButton.classList.remove("show"))
    .then(function () {
      document.querySelector('[unread-mes]').setAttribute("unread-mes", countNewMessages())
    })
    .then(function () {
      hideMarkAllMessagesButton()
    })
    .then(
      function () {
        if (markedAsReadAllButton) {
          document.querySelector('[window-elem="marked_as_read_all"] > span').classList.remove("click_opacity")
        }
      }
    )
}))

if (previousMessages) {
  previousMessages.addEventListener("click", function () {
    // Выводит прочитанные сообщения при нажатии на кнопку
    previousMessages.classList.toggle("click_opacity")

    data = {}
    let csrfToken = getCookie('csrftoken')

    data["amount"] = amountMessagesShowed()

    fetch('/account/messages/', {
      method: "GET_PREV_MESSAGES",
      body: JSON.stringify(data),
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
      }
    })
      .then((response) => response.json())
      .then(function (data) {
        if (data.status == 'ok') {
          messageItems.innerHTML = messageItems.innerHTML + data.messages_block
        }
        if (!data.next_messages_exist) {
          previousMessages.setAttribute("style", "display:none")
        }
      })
      .then(
        function () {
          if (previousMessages) {
            previousMessages.classList.toggle("click_opacity")
          }
        }
      )
  })
}
