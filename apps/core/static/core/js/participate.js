function openPaymentTypePopup() {
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
    'window': 'type',
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

function openPaymentLinkPopup(element) {
  let paymentType = element.getAttribute('type')
  let paymentPopupWrapper = element.closest('[popup-name="payment"]')
  let karathonId = paymentPopupWrapper.querySelector('[popup-element="payment-type-button-wrapper"]')
    .getAttribute('karathon-id')
  let karathonNumber = paymentPopupWrapper.querySelector('[popup-element="payment-type-button-wrapper"]')
    .getAttribute('karathon-number')

  paymentPopupWrapper.innerHTML = ''
  paymentPopupWrapper.classList.add('loading')

  let csrfToken = getCookie('csrftoken')
  let data = {
    'window': 'link',
    'payment_type': paymentType,
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

function closePaymentPopup() {
  paymentPopupWrapper.classList.remove('show');
  overlay.classList.remove('show')
}

let openPaymentPopupButton = document.querySelectorAll('[participate-elem="open-payment-popup-button"]')

if (openPaymentPopupButton.length > 0) {
  openPaymentPopupButton.forEach(element => element.addEventListener("click", openPaymentTypePopup))
}

let paymentPopupWrapper = document.querySelector('[popup-element="popup"][popup-name="payment"]')
if (paymentPopupWrapper) {
  paymentPopupWrapper.addEventListener('click', function (event) {
    let target = event.target

    if (target.getAttribute('popup-element') == 'payment-type-button') {
      openPaymentLinkPopup(target)
    }

    if (target.getAttribute('popup-element') == 'close') {
      closePaymentPopup()
    }
  })
}


