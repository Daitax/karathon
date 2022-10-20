function openReportForm() {
  let overlay = document.querySelector('[popup-element="overlay"]')
  let reportFormWrapper = overlay.querySelector('[form-name="report"]')

  overlay.classList.add('show')
  reportFormWrapper.classList.add('show')

  let csrfToken = getCookie('csrftoken')
  let data = new FormData()
  data.append('window', 'open')

  fetch('/steps/addreport/', {
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
          reportFormWrapper.innerHTML = data.window
        }
      }
    })
}

function submitReportForm(button) {
  let reportFormWrapper = button.closest('[popup-element="popup"][form-name="report"]')
  let reportForm = button.closest('[report-form-elem="form"]')

  let csrfToken = getCookie('csrftoken')
  let data = new FormData(reportForm)

  fetch('/steps/addreport/', {
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
          reportFormWrapper.innerHTML = data.window
        }
      }
    })
}

let openFormReportButtons = document.querySelectorAll('[button-action="open-report-form"]')
if (openFormReportButtons.length > 0) {
  openFormReportButtons.forEach(function (button) {
    button.addEventListener('click', openReportForm)
  })
}
let reportFormWrapper = document.querySelector('[popup-element="popup"][form-name="report"]')
if (reportFormWrapper) {
  reportFormWrapper.addEventListener('click', function (event) {
    let target = event.target

    if (target.getAttribute('report-form-elem') == 'button') {
      submitReportForm(target)
    }
  })
  reportFormWrapper.addEventListener('submit', function (event) {
    event.preventDefault()
    submitReportForm(event.target)
  })
}

