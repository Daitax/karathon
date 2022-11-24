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

let accountMenu = document.querySelector('[window-elem="account_avatar"] ~ [window-elem="account_menu"]')

if (accountMenu) {
  let accountMenuTop = accountMenu.getBoundingClientRect().top

  window.addEventListener("scroll", function () {
    // let accountMenuTop = accountMenu.getBoundingClientRect().top
    // console.log(accountMenuTop)
    // Двигает меню пользователя по странице в личном кабинете
    if ((accountMenuTop - window.pageYOffset) < 90) {
      // if (accountMenuTop <= 90) {
      accountMenu.setAttribute("style", "position: fixed; top: 97px; right: calc(50% - 670px); bottom: auto;")
    } else {
      accountMenu.setAttribute("style", "position: absolute; top: auto; right: -10px; bottom: -140px;")
    }
  })
}
