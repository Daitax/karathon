let task = document.querySelector('[task-elem="task_wrapper"]')
let taskDescription = document.querySelector('[task-elem="task_description"]')
let taskClose = document.querySelector('[task-elem="close"]')
let taskText = document.querySelector('[task-elem="task"]')

if (task) {
    task.addEventListener("click", function () {
        // Закрывает/открывает задание по клику на него
        taskDescription.classList.toggle("show")
        taskClose.classList.toggle("show")
        taskText.classList.toggle("task_today_background")
    })
}

window.addEventListener("load", function () {
    this.window.addEventListener("scroll", function () {
        // Задание дня зафиксровано в левом нижнем углу экрана до подвала
        let topTask = document.body.scrollHeight - footer.clientHeight - task.clientHeight
        if (task.getBoundingClientRect().bottom >= footer.getBoundingClientRect().top) {
            task.setAttribute("style", "position:absolute; height: fit-content; top:" + topTask + "px")
        }
        if (footer.offsetTop > window.pageYOffset + document.body.clientHeight) {
            task.setAttribute("style", "position:fixed; left:0; bottom:0")
        }
    })
})
