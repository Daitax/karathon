function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

let stickyNavbar = document.querySelector('[window-elem="sticky_navbar"]')
let firstScreen = document.querySelector('[window-elem="first-screen"]')
let firstScreenBottom = firstScreen.getBoundingClientRect().bottom
let footer = document.querySelector('[window-elem="footer"]')
let footerTop = footer.offsetTop
let stickyAccMenu = document.querySelector('[window-elem="sticky_navbar"] > [window-elem="account_menu"]')

window.addEventListener("scroll", function () {
  // Показывает/убирает главное меню при прокрутке ниже первого экрана
  let screenTop = window.pageYOffset

  if ((firstScreenBottom <= screenTop) && (screenTop <= footerTop)) {
    stickyNavbar.setAttribute("style", "top: 0")
  } else {
    stickyNavbar.setAttribute("style", "top: -150px")
    if (stickyAccMenu) {
      stickyAccMenu.classList.remove("show")
    }
  }
})

let avatarButtons = document.querySelectorAll('[navbar-elem="user_avatar"]')

avatarButtons.forEach(element => element.addEventListener("click", function () {
  // Показывает/убирает меню аккаунта при клике по аватарке
  let accountMenu = element.nextElementSibling

  accountMenu.classList.toggle("show")
}))

let content = document.querySelector('[window-elem="content"]')
let accMenues = document.querySelectorAll('[window-elem="account_menu"]')

content.addEventListener("click", function () {
  // Убирает меню аккаунта при клике вне его
  accMenues.forEach(element => element.classList.remove("show"))
})

let inputAvatar = document.querySelector('[window-elem="input_avatar"]')
let avatarPreview = document.querySelector('[window-elem="avatar_preview"]')

if (inputAvatar) {
  inputAvatar.addEventListener("change", function () {
    // Показывает превью аватарки перед загрузкой на сервер
    if (this.files[0]) {
      let fileReader = new FileReader();

      fileReader.addEventListener("load", function () {
        avatarPreview.setAttribute("src", fileReader.result)
        avatarPreview.setAttribute("style", "display:block")
      }, false);

      fileReader.readAsDataURL(this.files[0]);
    }
  });
}

let accountMenu = document.querySelector('[window-elem="account_avatar"] ~ [window-elem="account_menu"]')

if (accountMenu) {
  let accountMenuTop = accountMenu.getBoundingClientRect().top

  window.addEventListener("scroll", function () {
    // Двигает меню пользователя по странице в личном кабинете
    if ((accountMenuTop - window.pageYOffset) < 90) {
      accountMenu.setAttribute("style", "position: fixed; top: 97px; right: calc(50% - 670px); bottom: auto;")
    } else {
      accountMenu.setAttribute("style", "position: absolute; top: auto; right: -10px; bottom: -140px;")
    }
  })
}

let deadline = 86400 // количество секунд в сутках
let localtime = document.querySelectorAll('[menu-elem="participant_localtime"]')
let timerId;
let localHours = Number(localtime[0].getAttribute("localtime").split(" ")[0])
let localMinutes = Number(localtime[0].getAttribute("localtime").split(" ")[1])
let localSeconds = Number(localtime[0].getAttribute("localtime").split(" ")[2])
let odds = deadline - (localHours * 60 * 60 + localMinutes * 60 + localSeconds)
let firstScreenCountdown = document.querySelector('[window-elem="first-screen-countdown"]')
let lateText = "опоздали:("

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

function printTime(value) {
  // Показывает оставшееся до сдачи время или сообщение
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
