let firstScreenPromo = document.querySelectorAll('[window-elem="first-screen-promo"]')
let promoVideo = document.querySelector('[popup-name="promo-video"]')

function openPromoVideoPopup() {
    toggleActionVideo('play', promoVideo)

    // открывает поп-ап с промо-видео
    overlay.classList.add('show')
    promoVideo.classList.add("show")
}

function closePromoVideoPopup() {
    toggleActionVideo('pause', promoVideo)

    // закрывает поп-ап с промо-видео
    overlay.classList.remove('show')
    promoVideo.classList.remove("show")
}

function toggleActionVideo(action, container) {
    let video = container.getElementsByTagName('iframe')
    if (action == 'play'){
        video[0].contentWindow.postMessage('{"event":"command","func":"playVideo","args":""}', '*');
    } else if (action == 'pause') {
        video[0].contentWindow.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');
    }
}

if (firstScreenPromo) {
    firstScreenPromo.forEach(element => element.addEventListener("click", function () {
        openPromoVideoPopup()
    }))
}

if (promoVideo) {
    overlay.addEventListener('click', function (event) {
        let target = event.target

        if (target.getAttribute('popup-element') == 'close') {
            closePromoVideoPopup()
        }

        if (target.getAttribute('popup-element') == 'overlay') {
            closePromoVideoPopup()
        }
    })
}