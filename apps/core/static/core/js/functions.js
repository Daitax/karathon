let stickyNavbar = document.querySelector('[window-elem="sticky_navbar"]')
let firstScreen = document.querySelector('[window-elem="first-screen"]')
let footer = document.querySelector('[window-elem="footer"]')
let stickyAccMenu = document.querySelector('[window-elem="sticky_navbar"] > [window-elem="account_menu"]')
let mobStickyAccMenu = document.querySelectorAll('.header_navbar_menu_mobile_buttons > [window-elem="account_menu"]')[1]
let mobMenues = document.querySelectorAll('[window-elem="mobile_menu"]')
var footerTop = footer.offsetTop

window.addEventListener("load", function () {
  window.addEventListener("scroll", function () {
    // Убирает/показывает главное меню при скролле ниже/выше первого экрана
    let firstScreenBottom = firstScreen.clientHeight

    if ((window.pageYOffset >= firstScreenBottom) && (window.pageYOffset <= footer.offsetTop - stickyNavbar.clientHeight)) {
      stickyNavbar.setAttribute("style", "top: 0")
    }
    else {
      stickyNavbar.setAttribute("style", "top: -6.08rem")
      if (stickyAccMenu) {
        stickyAccMenu.classList.remove("show")
      }
      if (mobStickyAccMenu) {
        mobStickyAccMenu.classList.remove("show")
      }
      if (mobMenues) {
        mobMenues.forEach(
          function (element) {
            element.classList.remove("show")
            let mobileKarathonsList = element.querySelector('[menu-elem="mobile_karathons_list"]')
            if (mobileKarathonsList) {
              mobileKarathonsList.classList.remove('open')
            }
          }
        )
      }
    }
  })
})

let avatarButtons = document.querySelectorAll('[navbar-elem="user_avatar"]')

avatarButtons.forEach(element => element.addEventListener("click", function () {
  // Показывает/убирает меню аккаунта на главной странице при клике по аватарке
  let accountMenu = element.nextElementSibling

  accountMenu.classList.toggle("show")
}))

let indexpageBackgroundArr = document.querySelectorAll('[window-elem="content"], .footsteps')
let accMenues = document.querySelectorAll('[window-elem="account_menu"]')

indexpageBackgroundArr.forEach(element => element.addEventListener("click", function () {
  // Убирает меню аккаунта на главной странице при клике вне его
  accMenues.forEach(element => element.classList.remove("show"))
}))

let deadline = 86400 // количество секунд в сутках
let localtime = document.querySelectorAll('[menu-elem="participant_localtime"]')
let timerId;

function getTime(value) {
  // Из переданнаго количества секунд возвращает время в нужном формате
  let hours = Math.trunc(value / 3600)
  let minutes = Math.trunc((value - 3600 * Math.trunc(value / 3600)) / 60)
  let seconds = (value - 3600 * Math.trunc(value / 3600)) % 60

  if (hours < 10) {
    hours = "0" + hours
  }
  if (minutes < 10) {
    minutes = "0" + minutes
  }
  if (seconds < 10) {
    seconds = "0" + seconds
  }
  return hours + ":" + minutes + ":" + seconds
}

if (localtime[0]) {
  let localHours = Number(localtime[0].getAttribute("localtime").split(" ")[0])
  let localMinutes = Number(localtime[0].getAttribute("localtime").split(" ")[1])
  let localSeconds = Number(localtime[0].getAttribute("localtime").split(" ")[2])
  var odds = deadline - (localHours * 60 * 60 + localMinutes * 60 + localSeconds)
  var firstScreenCountdown = document.querySelector('[window-elem="first-screen-countdown"]')
  var lateText = "опоздали:("

  function printTime(value) {
    // Показывает оставшееся до сдачи отчета время или сообщение
    if (value >= 0) {
      localtime.forEach(element => element.setAttribute("countdown", getTime(value)));
      if (firstScreenCountdown) {
        firstScreenCountdown.innerHTML = getTime(value)
      }
      value--;
    } else {
      localtime.forEach(element => element.setAttribute("countdown", lateText));
      if (firstScreenCountdown) {
        firstScreenCountdown.innerHTML = lateText
      }
    }
  }

  function startCountdown() {
    // Каждую секунду запускает функцию определения времени
    timerId = setInterval(() => {
      if (odds >= 0) {
        localtime.forEach(element => element.setAttribute("countdown", getTime(odds)));
        if (firstScreenCountdown) {
          firstScreenCountdown.innerHTML = getTime(odds)
        }
        odds--;
      } else {
        localtime.forEach(element => element.setAttribute("countdown", lateText));
        if (firstScreenCountdown) {
          firstScreenCountdown.innerHTML = lateText
        }
      }
    }, 1000);
  }
  printTime(odds)
  startCountdown()
}

let mobileMenuButtons = document.querySelectorAll('[window-elem="mobile_menu_button"]')

mobileMenuButtons.forEach(element => element.addEventListener("click", function () {
  // Показывает/убирает главное меню по клику на кнопку "Меню"
  let mobileMenu = element.nextElementSibling
  mobileMenu.classList.toggle("show")
}))

let mobileMenuKarathonsListButton = document.querySelectorAll('[menu-elem="mobile_karathons"]')

if (mobileMenuKarathonsListButton) {
  mobileMenuKarathonsListButton.forEach(element => {
    element.addEventListener('click', function(ev) {
      let mobileMenuWrapper = element.closest('[menu-elem="menu_mobile_wrapper"]')

      let mobileMenuKarathonsList = mobileMenuWrapper.querySelector('[menu-elem="mobile_karathons_list"]')

      mobileMenuKarathonsList.classList.toggle('open')
    })
  })
}

let content = document.querySelector('[window-elem="content"]')
content.addEventListener("click", function () {
  // Убирает меню при клике вне его в мобильной версии
  mobMenues.forEach(element => element.classList.remove("show"))
})

firstScreen.addEventListener("click", function () {
  // Убирает меню при клике вне его в мобильной версии
  mobMenues.forEach(element => element.classList.remove("show"))
})

let logoutButton = document.querySelectorAll('[menu-elem="logout"]')
let popupHeader = document.querySelector('[popup-name="confirmation"] h4')
let popupButtons = document.querySelectorAll('[popup-element]')
let confirmationPopup = document.querySelector('[popup-name="confirmation"]')

function confirmationClose() {
  // Закрывает поп-ап подтверждения и убирает заголовок в нем
  overlay.classList.remove('show')
  confirmationPopup.classList.remove('show')
  popupHeader.innerHTML = ""
}

function confirmationOpen(header) {
  // Открывает поп-ап подтверждения и добавляет заголовок
  overlay.classList.add('show')
  confirmationPopup.classList.add('show')
  popupHeader.innerHTML = header
}

logoutButton.forEach(element => element.addEventListener("click", function (event) {
  // Показывает поп-ап с подтверждением выхода из аккаунта
  event.preventDefault()
  confirmationOpen(header = "Выйти?")
  popupButtons.forEach(el => el.addEventListener("click", function () {
    let choise = el.getAttribute("popup-element")

    if (choise == "confirm") {
      location.href = element.getAttribute("href")
    }
    if (choise == "deny") {
      popupHeader.innerHTML = ""
      confirmationClose()
    }
  }))
}, false))

function showStepOrHide(elem, crossing_block = document.querySelector('[window-elem="about_karathon_wrapper"]')) {
  let leftBorder = crossing_block.getBoundingClientRect().left
  let rightBorder = crossing_block.getBoundingClientRect().right
  let topBorder = crossing_block.getBoundingClientRect().top
  let bottomBorder = crossing_block.getBoundingClientRect().bottom
  let elemY = elem.getBoundingClientRect().top
  let elemX = elem.getBoundingClientRect().left
  let deltaX = elem.clientWidth
  let deltaY = elem.clientHeight

  if (elemY < 0.5 * window.innerHeight) {
    if ((elemY + deltaY >= topBorder && elemY <= bottomBorder) && (elemX >= leftBorder && elemX <= rightBorder)) {
      elem.classList.add('show_blur')
    } else {
      elem.classList.add('show')
    }
  } else {
    elem.classList.remove('show') || elem.classList.remove('show_blur')
  }
}

if (window.location.pathname == "/") {
  let stepsArr = document.querySelectorAll('[window-elem="footsteps"] img')

  if (stepsArr) {
    window.addEventListener("scroll", function () {
      // Показывает/убирает следы на главной странице
      stepsArr.forEach(element => showStepOrHide(element))
    })
  }
}

if (window.location.pathname.includes("-karathon")) {
  window.addEventListener("scroll", function () {
    // Показывает/убирает следы на странице информации о карафоне
    document.querySelectorAll('[window-elem="footsteps_karathon_page"] img').forEach(element => showStepOrHide(element))
  })
}
