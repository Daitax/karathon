function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, options = {}) {
  options = {
    path: '/',
    // при необходимости добавьте другие значения по умолчанию
    ...options
  };

  if (options.expires instanceof Date) {
    options.expires = options.expires.toUTCString();
  }

  let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

  for (let optionKey in options) {
    updatedCookie += "; " + optionKey;
    let optionValue = options[optionKey];
    if (optionValue !== true) {
      updatedCookie += "=" + optionValue;
    }
  }

  document.cookie = updatedCookie;
}

let cookieBlock = document.querySelector('[window-elem="cookie"]')
let cookieBlockBtn = document.querySelector('[window-elem="cookie_button"]')

function closeCookieBlock() {
    cookieBlock.classList.remove("show")
}

function openCookieBlock() {
    cookieBlock.classList.add("show")
}

cookieBlockBtn.addEventListener("click", function () {
    closeCookieBlock()
    setCookie('is_cookie_need_show', 'false')
})

if (getCookie('is_cookie_need_show') == 'false') closeCookieBlock()

if (!getCookie('is_cookie_need_show')) openCookieBlock()
