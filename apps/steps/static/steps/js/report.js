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
    .then(function () {
      let stepsInput = document.querySelector('[name="steps"]')
      stepsInput.focus()
      stepsInput.click()
    })
    .then(
      function () {
        let reportCustomInput = document.querySelector('[report-form-elem="custom_input"]')

        reportCustomInput.addEventListener("click", function () {
          reportCustomInput.classList.add("click_opacity")
        })
      }
    )
}

function closeReportForm() {
  reportFormWrapper.classList.remove('show');
  overlay.classList.remove('show')
}

function submitReportForm(button) {
  let reportFormWrapper = button.closest('[popup-element="popup"][form-name="report"]')
  let reportForm = button.closest('[report-form-elem="form"]')

  let csrfToken = getCookie('csrftoken')
  let data = new FormData(reportForm)

  let steps = data.get("steps").split(' ').join('')

  data.set("steps", steps)

  document.querySelector('[report-form-elem="button"] > span').classList.add("click_opacity")

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

    // if (target.getAttribute('report-form-elem') == 'button') {
    //   submitReportForm(target)
    // }
    if (target.getAttribute('report-form-elem') == 'custom_input') {
      let input = document.querySelector("#photo_report")
      let inputCustom = document.querySelector('[report-form-elem="custom_input"]')

      input.addEventListener('change', function () {
        if (this.files && this.files.length >= 1) {
          inputCustom.innerHTML = "Фото выбрано"
          inputCustom.setAttribute("style", "text-decoration: none;")
        } else {
          inputCustom.innerHTML = "Прикрепи фото"
        }
      })
    }
    if (target.getAttribute('popup-element') == 'close') {
      if (reportFormWrapper.querySelector('[reload="True"]')) {
        window.location.reload()
      } else {
        closeReportForm()
      }
    }
    if (target.getAttribute('name') == 'steps') {
      let stepsField = document.querySelector('[name="steps"]')
      let maskStepsOptions = {
        mask: Number,
        thousandsSeparator: ' ',
      };

      IMask(stepsField, maskStepsOptions);
    }
  })
  reportFormWrapper.addEventListener('submit', function (event) {
    event.preventDefault()
    submitReportForm(event.target)
  })
}

