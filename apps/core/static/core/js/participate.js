function openPaymentEmailPopup() {
  let overlay = document.querySelector('[popup-element="overlay"]')
  let paymentPopupWrapper = overlay.querySelector('[popup-name="payment"]')

  paymentPopupWrapper.innerHTML = ''
  overlay.classList.add('show')
  paymentPopupWrapper.classList.add('show', 'loading')

  let karathonWrapper = this.closest('[participate-elem="karathon-wrapper"]')
  let karathonId = karathonWrapper.getAttribute('karathon-id')
  let karathonNumber = karathonWrapper.querySelector('[participate-elem="karathon-number"]')
    .getAttribute('karathon-number')

  let csrfToken = getCookie('csrftoken')
  let data = {
    'window': 'email',
    'karathon_id': karathonId,
    'karathon_number': karathonNumber
  }

  fetch('/participate/', {
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
        paymentPopupWrapper.classList.remove('loading')
        paymentPopupWrapper.innerHTML = data.window
      }
    })
}

function openPaymentTypePopup(element) {
  let popupWrapper = element.closest('[popup-name="payment"]')
  let email = popupWrapper.querySelector('[popup-element="payment-email"]').value
  if (validateEmail(email)) {
    let karathonId = popupWrapper.querySelector('[karathon-id]')
      .getAttribute('karathon-id')
    let karathonNumber = popupWrapper.querySelector('[karathon-number]')
      .getAttribute('karathon-number')

    popupWrapper.innerHTML = ''
    popupWrapper.classList.add('loading')

    let csrfToken = getCookie('csrftoken')
    let data = {
      'window': 'type',
      'email': email,
      'karathon_id': karathonId,
      'karathon_number': karathonNumber
    }

    fetch('/participate/', {
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
          paymentPopupWrapper.classList.remove('loading')
          paymentPopupWrapper.innerHTML = data.window
        }
      })
  } else {
  //  TODO Надо сделать обработку ошибки некорректного email
  }
}

function openPaymentLinkPopup(element) {

  let paymentType = element.getAttribute('type')
  let popupWrapper = element.closest('[popup-name="payment"]')
  let karathonId = popupWrapper.querySelector('[popup-element="payment-type-button-wrapper"]')
    .getAttribute('karathon-id')
  let karathonNumber = popupWrapper.querySelector('[popup-element="payment-type-button-wrapper"]')
    .getAttribute('karathon-number')
  let email = popupWrapper.querySelector('[popup-element="payment-type-button-wrapper"]')
    .getAttribute('email')

  paymentPopupWrapper.innerHTML = ''
  paymentPopupWrapper.classList.add('loading')

  let csrfToken = getCookie('csrftoken')
  let data = {
    'window': 'link',
    'payment_type': paymentType,
    'karathon_id': karathonId,
    'karathon_number': karathonNumber,
    'email': email,
  }

  fetch('/participate/', {
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
        paymentPopupWrapper.classList.remove('loading')
        paymentPopupWrapper.innerHTML = data.window
      }
    })
}

function closePaymentPopup() {
  paymentPopupWrapper.classList.remove('show');
  overlay.classList.remove('show')
}

function validateEmail(email) {
  const mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
  return !!email.match(mailformat)
}

// let openEmailPopupButton = document.querySelectorAll('[participate-elem="open-email-popup-button"]')
//
// if (openEmailPopupButton.length > 0) {
//   openEmailPopupButton.forEach(element => element.addEventListener("click", openPaymentEmailPopup))
// }
//
// let paymentPopupWrapper = document.querySelector('[popup-element="popup"][popup-name="payment"]')
// if (paymentPopupWrapper) {
//   paymentPopupWrapper.addEventListener('click', function (event) {
//     event.preventDefault()
//     let target = event.target
//
//     if (target.closest('[popup-element]').getAttribute('popup-element') === 'payment-email-button') {
//       openPaymentTypePopup(target)
//     }
//
//     if (target.closest('[popup-element]').getAttribute('popup-element') === 'payment-type-button') {
//       openPaymentLinkPopup(target)
//     }
//
//     if (target.closest('[popup-element]').getAttribute('popup-element') === 'close') {
//       closePaymentPopup()
//     }
//   })
// }

function openPaymentPopup(element) {
  let overlay = document.querySelector('[popup-element="overlay"]')
  let paymentPopupWrapper = overlay.querySelector('[popup-name="payment"]')

  paymentPopupWrapper.innerHTML = ''
  overlay.classList.add('show')
  paymentPopupWrapper.classList.add('show', 'loading')

  let karathonWrapper = this.closest('[participate-elem="karathon-wrapper"]')
  let karathonId = karathonWrapper.getAttribute('karathon-id')
  let karathonNumber = karathonWrapper.querySelector('[participate-elem="karathon-number"]')
    .getAttribute('karathon-number')

  let csrfToken = getCookie('csrftoken')
  let data = {
    'window': 'link',
    'karathon_id': karathonId,
    'karathon_number': karathonNumber
  }

  fetch('/participate/', {
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
        paymentPopupWrapper.classList.remove('loading')
        paymentPopupWrapper.innerHTML = data.window
      }
    })
}

let openPaymentPopupButton = document.querySelectorAll('[participate-elem="open-payment-popup-button"]')

if (openPaymentPopupButton.length > 0) {
  openPaymentPopupButton.forEach(element => element.addEventListener("click", openPaymentPopup))
}

let paymentPopupWrapper = document.querySelector('[popup-element="popup"][popup-name="payment"]')
if (paymentPopupWrapper) {
  paymentPopupWrapper.addEventListener('click', function (event) {
    event.preventDefault()
    let target = event.target

    if (target.closest('[popup-element]').getAttribute('popup-element') === 'close') {
      closePaymentPopup()
    }
  })
}
