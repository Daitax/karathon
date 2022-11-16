function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}


let stickyNavbar = document.querySelector('[window-elem="sticky_navbar"]')
let firstScreen = document.querySelector('[window-elem="first-screen"]')
let firstScreenBottom = firstScreen.getBoundingClientRect().bottom
let leftOffset = firstScreen.getBoundingClientRect().left / 2 + "px"
let stickyNavbarStyle = "position: fixed; left: " + leftOffset + "; padding: 10px 0 10px " + leftOffset + "; z-index: 2;"
let footer = document.querySelector('[window-elem="footer"]')
let footerTop = footer.offsetTop

let stickyAccMenu = document.querySelector('[window-elem="sticky_navbar"] > [window-elem="account_menu"]')
// console.log(stickyAccMenu)

window.addEventListener("scroll", function () {
  let screenTop = window.pageYOffset

  if ((firstScreenBottom <= screenTop) && (screenTop <= footerTop)) {
    stickyNavbar.setAttribute("style", stickyNavbarStyle + "top: 0")
    stickyAccMenu.setAttribute("style", "display: block; transition: 1s")
  } else {
    stickyNavbar.setAttribute("style", stickyNavbarStyle + "top: -50px")
    stickyAccMenu.setAttribute("style", "display: none")
  }
})

// let header = document.querySelector('[window-elem="header"]')
// let navbar = document.querySelector('[window-elem="navbar"]')
// let leftOffset = navbar.getBoundingClientRect().left / 2 + "px"
// let footer = document.querySelector('[window-elem="footer"]')

// window.addEventListener("scroll", function () {
//   let screenTop = window.pageYOffset
//   let footerTop = footer.offsetTop
//   let headerHeight = header.offsetHeight
//   if (screenTop <= footerTop) {
//     navbar.setAttribute("style", "position: fixed; left: " + leftOffset + "; padding: 10px 0 10px " + leftOffset + "; background: #F648A5; margin-top: 10px; z-index: 1;")
//     header.setAttribute("style", "min-height: " + headerHeight + "px")
//   }
// })