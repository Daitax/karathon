let showNextKarathonRatingItemsButton = document.querySelector('[window-elem="next_items_ratings"]')
let karathonRatingWrapper = document.querySelector('[window-elem="rating_wrapper"]')

if (showNextKarathonRatingItemsButton){
  data = {}

  showNextKarathonRatingItemsButton.addEventListener("click", function () {
    // дополняет список рейтинга карафона при клике на кнопку

    showNextKarathonRatingItemsButton.classList.add("click_opacity")

    data["amount_list"] = document.querySelectorAll('[window-elem="rating_item"]').length / 2
    // делим на 2 так как отображаюся и мобильные, и десктопные чемпионы

    let csrfToken = getCookie('csrftoken')
    let current_path = location.pathname

    fetch(current_path, {
      method: "GET_RATING_LIST",
      body: JSON.stringify(data),
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
      }
    })
      .then((response) => response.json())
      .then(function (data) {

        if (data.status == "ok") {
          karathonRatingWrapper.innerHTML = data.rating_list_block

          if (!data.next_rating_items_exist) {
            showNextKarathonRatingItemsButton.setAttribute("style", "display:none")
          }
        }

        showNextKarathonRatingItemsButton.classList.remove("click_opacity")
      })

  })
}