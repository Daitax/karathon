let firstScreenPromo = document.querySelectorAll('[window-elem="first-screen-promo"]')
let promoVideo = document.querySelector('[popup-name="promo-video"]')

function openPromoVideoPopup() {
    // открывает поп-ап с промо-видео

    overlay.classList.add('show')
    promoVideo.classList.add("show")
}

function closePromoVideoPopup() {
    // закрывает поп-ап с промо-видео

    overlay.classList.remove('show')
    promoVideo.classList.remove("show")
}

if (firstScreenPromo) {
    firstScreenPromo.forEach(element => element.addEventListener("click", function () {
        // let promoVideo = document.querySelector('[popup-name="promo-video"]')

        openPromoVideoPopup()

        if (promoVideo) {
            promoVideo.addEventListener('click', function (event) {
                let target = event.target

                if (target.getAttribute('popup-element') == 'close') {
                    closePromoVideoPopup()
                }
            })
        }
    }))
}