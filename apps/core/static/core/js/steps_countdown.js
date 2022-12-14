// let stepsBlock = document.querySelector('[window-elem="steps_block"]')
// let StepsTotal = document.querySelector('[window-elem="steps_total"]')
// let stopCnt = 300
// // let startCnt = 0
// let cntDwn

// // function newVal(startCnt, stopCnt) {
// //     if (startCnt < stopCnt) {
// //         return startCnt++
// //     } else {
// //         return stopCnt
// //     }
// // }

// const time = 1000;
// const step = 1;

// function outNum(stopCnt, elem) {
//     let e = document.querySelector('[window-elem="steps_total"]')
//     n = 0;
//     let t = Math.round(time / (stopCnt / step));
//     let interval = setInterval(() => {
//         n = n + step;
//         if (n == stopCnt) {
//             clearInterval(interval);
//         }
//         e.innerHTML = n;
//     }, t);
// }

// // outNum(1000);
// let isStarted = true
// let totalSteps = StepsTotal.getAttribute("total-steps")
// console.log(totalSteps)

// window.addEventListener("scroll", function () {
//     // console.log(stepsBlock.getBoundingClientRect().top)
//     // console.log(document.body.clientHeight)
//     if ((stepsBlock.getBoundingClientRect().top <= document.body.clientHeight / 2) && isStarted) {
//         console.log("ok")
//         isStarted = false
//         outNum(1000);
//     }
// })

