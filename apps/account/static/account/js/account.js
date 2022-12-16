let inputAvatar = document.querySelector('[window-elem="input_avatar"]')
let avatarPreview = document.querySelector('[window-elem="avatar_preview"]')
let avatarPreviewBig = document.querySelector('[window-elem="avatar_preview_big"]')

function showPreview(val) {
    // Добавляет стили на блоки превью для аватарки при передачи в функцию пути
    avatarPreview.setAttribute("style", "\
        display:block;\
        background-image:url(" + val + ");\
        background-repeat: no-repeat;\
        background-position: center center;\
        background-size: cover;")
    avatarPreviewBig.setAttribute("style", "\
        display:block;\
        background-image:url(" + val + ");\
        background-repeat: no-repeat;\
        background-position: center center;\
        background-size: cover;")
}

if (inputAvatar) {
    inputAvatar.addEventListener("change", function () {
        // Показывает превью аватарки перед загрузкой на сервер
        if (this.files[0]) {
            let fileReader = new FileReader();
            let customInputAvatar = document.querySelector('[window-elem="custom_input_avatar"]')

            fileReader.addEventListener("load", function () {
                if (customInputAvatar) {
                    customInputAvatar.setAttribute("style", "border:none")
                }
                showPreview(fileReader.result)
            }, false);
            fileReader.readAsDataURL(this.files[0]);
        }
    });
}