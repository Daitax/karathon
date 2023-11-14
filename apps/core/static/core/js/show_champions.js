let showChampsButton = document.querySelector('[window-elem="next_champs"]')
let champsWrapper = document.querySelector('[window-elem="champions_wrapper"]')

data = {}

if (showChampsButton) {
  showChampsButton.addEventListener("click", function () {
    // дополняет список рекордсменов при клике на кнопку

    showChampsButton.classList.toggle("click_opacity")

    data["amount_champs"] = document.querySelectorAll('[window-elem="champions_item"]').length / 2 // делим на 2 так как отображаюся и мобильные, и десктопные чемпионы
    console.log(data)
    let csrfToken = getCookie('csrftoken')

    fetch('/champions', {
      method: "GET_CHAMPS_LIST",
      body: JSON.stringify(data),
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
      }
    })
      .then((response) => response.json())
      .then(function (data) {
        if (data.status == "ok") {
          champsWrapper.innerHTML = data.champs_block

          if (!data.next_champs_exist) {
            showChampsButton.setAttribute("style", "display:none")
          }
        }
      })
  })
}