function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
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
    sessionStorage.setItem('is_cookie_need_show', false);
})

if (sessionStorage.getItem('is_cookie_need_show') == 'false') closeCookieBlock()

if (!sessionStorage.getItem('is_cookie_need_show')) openCookieBlock()
