let stepsBlock = document.querySelector('[window-elem="steps_block"]')
let stepsBlockTop = stepsBlock.getBoundingClientRect().top
let stepsTotal = document.querySelector('[window-elem="steps_total"]')
let totalStepsAmount = stepsTotal.getAttribute("total-steps")
let stepsPastKarathon = document.querySelector('[window-elem="steps_past_karathon"]')
let stepsPastKarathonAmount = stepsPastKarathon.getAttribute("steps-past-karathon")
let stepsTotalToday = document.querySelector('[window-elem="steps_total_today"]')
let stepsTotalTodayAmount = stepsTotalToday.getAttribute("steps-total-today")
let isStarted = false

function format(str) {
    // Делает отступ в числе (число привести к строке) после каждых 3 цифр
    const s = str.length
    const chars = str.split('')
    const strWithSpaces = chars.reduceRight((acc, char, i) => {
        const spaceOrNothing = ((((s - i) % 3) === 0) ? ' ' : '')
        return (spaceOrNothing + char + acc)
    }, '')

    return ((strWithSpaces[0] === ' ') ? strWithSpaces.slice(1) : strWithSpaces)
}

function counter(value, element, timeout = 10, step = Math.floor(value * 0.005) + 111, delta = 0.5) {
    // Счетчик от 0 до заданного числа
    let i = 0;
    (function () {
        if (i <= value) {
            setTimeout(arguments.callee, timeout)
            element.innerHTML = format(String(i))
            i = i + step
            timeout = timeout + delta
        } else {
            element.innerHTML = format(String(value))
        }
    })();
}

window.addEventListener("load", function () {
    this.window.addEventListener("scroll", function () {
        if (window.pageYOffset >= stepsBlockTop - 0.5 * window.screen.height) {
            // Запускает счетчики шагов при прокрутке не доходя половины экрана до блока шагов
            if (!isStarted) {
                counter(totalStepsAmount, stepsTotal);
                counter(stepsPastKarathonAmount, stepsPastKarathon);
                counter(stepsTotalTodayAmount, stepsTotalToday);
                isStarted = true
            }
        }
    })
})



