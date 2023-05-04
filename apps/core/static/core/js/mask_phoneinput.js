function mobileMaskInput() {
    var phoneInputs = document.querySelectorAll('input[data-tel-input]');

    var getInputNumbersValue = function (input) {
        // Return stripped input value — just numbers
        return input.value.replace(/\D/g, '');
    }

    var onPhonePaste = function (e) {
        var input = e.target,
            inputNumbersValue = getInputNumbersValue(input);
        var pasted = e.clipboardData || window.clipboardData;
        if (pasted) {
            var pastedText = pasted.getData('Text');
            if (/\D/g.test(pastedText)) {
                // Attempt to paste non-numeric symbol — remove all non-numeric symbols,
                // formatting will be in onPhoneInput handler
                input.value = inputNumbersValue;
                return;
            }
        }
    }

    var onPhoneInput = function (e) {
        var input = e.target,
            inputNumbersValue = getInputNumbersValue(input),
            selectionStart = input.selectionStart,
            formattedInputValue = "";

        if (!inputNumbersValue) {
            return input.value = "";
        }

        if (input.value.length != selectionStart) {
            // Editing in the middle of input, not last symbol
            if (e.data && /\D/g.test(e.data)) {
                // Attempt to input non-numeric symbol
                input.value = inputNumbersValue;
            }
            return;
        }

        if (["7", "8", "9"].indexOf(inputNumbersValue[0]) > -1) { // для РФ, Казахстана
            if (inputNumbersValue[0] == "9") inputNumbersValue = "7" + inputNumbersValue;
            var firstSymbols = (inputNumbersValue[0] == "8") ? "8" : "+7";
            formattedInputValue = input.value = firstSymbols + " ";
            if (inputNumbersValue.length > 1) {
                formattedInputValue += '(' + inputNumbersValue.substring(1, 4);
            }
            if (inputNumbersValue.length >= 5) {
                formattedInputValue += ') ' + inputNumbersValue.substring(4, 7);
            }
            if (inputNumbersValue.length >= 8) {
                formattedInputValue += '-' + inputNumbersValue.substring(7, 9);
            }
            if (inputNumbersValue.length >= 10) {
                formattedInputValue += '-' + inputNumbersValue.substring(9, 11);
            }
        }
        else if ("1".indexOf(inputNumbersValue[0]) > -1) { // для США, Канады
            var firstSymbols = "+" + inputNumbersValue[0];
            formattedInputValue = input.value = firstSymbols + " ";
            if (inputNumbersValue.length > 1) {
                formattedInputValue += '(' + inputNumbersValue.substring(1, 4);
            }
            if (inputNumbersValue.length >= 5) {
                formattedInputValue += ') ' + inputNumbersValue.substring(4, 7);
            }
            if (inputNumbersValue.length >= 8) {
                formattedInputValue += '-' + inputNumbersValue.substring(7, 11);
            }
        }
        else if ("3".indexOf(inputNumbersValue[0]) > -1) {
            var firstSymbols = "+" + inputNumbersValue[0];
            formattedInputValue = input.value = firstSymbols + " ";
            if (inputNumbersValue[1] == "7") {
                formattedInputValue = input.value = firstSymbols + inputNumbersValue[1] + " ";
                if (inputNumbersValue[2] == "4") { // для Армении
                    formattedInputValue = input.value = firstSymbols + inputNumbersValue[1] + inputNumbersValue[2] + " ";
                    if (inputNumbersValue.length > 3) {
                        formattedInputValue += ' ' + inputNumbersValue.substring(3, 6);
                    }
                    if (inputNumbersValue.length > 6) {
                        formattedInputValue += ' ' + inputNumbersValue.substring(6, 12);
                    }
                }
                else if (inputNumbersValue[2] == "5") { // для Беларуси
                    formattedInputValue = input.value = firstSymbols + inputNumbersValue[1] + inputNumbersValue[2] + " ";
                    if (inputNumbersValue.length > 3) {
                        formattedInputValue += ' ' + inputNumbersValue.substring(3, 5);
                    }
                    if (inputNumbersValue.length > 5) {
                        formattedInputValue += ' ' + inputNumbersValue.substring(5, 8);
                    }
                    if (inputNumbersValue.length > 8) {
                        formattedInputValue += '-' + inputNumbersValue.substring(8, 10);
                    }
                    if (inputNumbersValue.length > 10) {
                        formattedInputValue += '-' + inputNumbersValue.substring(10, 12);
                    }
                }
                else {
                    formattedInputValue = '+' + inputNumbersValue.substring(0, 16);
                }
            }
            else if (inputNumbersValue[1] == "8") {
                formattedInputValue = input.value = firstSymbols + inputNumbersValue[1] + " ";
                if (inputNumbersValue[2] == "0") { // для Украины
                    formattedInputValue = input.value = firstSymbols + inputNumbersValue[1] + inputNumbersValue[2] + " ";
                    if (inputNumbersValue.length > 3) {
                        formattedInputValue += ' ' + inputNumbersValue.substring(3, 5);
                    }
                    if (inputNumbersValue.length > 5) {
                        formattedInputValue += ' ' + inputNumbersValue.substring(5, 8);
                    }
                    if (inputNumbersValue.length > 8) {
                        formattedInputValue += ' ' + inputNumbersValue.substring(8, 12);
                    }
                }
                else {
                    formattedInputValue = '+' + inputNumbersValue.substring(0, 16);
                }
            }
            else {
                formattedInputValue = '+' + inputNumbersValue.substring(0, 16);
            }
        } else {
            formattedInputValue = '+' + inputNumbersValue.substring(0, 16);
        }
        input.value = formattedInputValue;
    }
    var onPhoneKeyDown = function (e) {
        // Clear input after remove last symbol
        var inputValue = e.target.value.replace(/\D/g, '');
        if (e.keyCode == 8 && inputValue.length == 1) {
            e.target.value = "";
        }
    }
    for (var phoneInput of phoneInputs) {
        phoneInput.addEventListener('keydown', onPhoneKeyDown);
        phoneInput.addEventListener('input', onPhoneInput, false);
        phoneInput.addEventListener('paste', onPhonePaste, false);
    }
}

let authFormWrapper = document.querySelector('[popup-element="popup"][form-name="authentication"]')

if (authFormWrapper) {
    authFormWrapper.addEventListener('click', function (event) {
        let target = event.target

        if (target.getAttribute('auth-form-elem') == 'phone') {
            mobileMaskInput()
        }
    })
}

let addFormWrapper = document.querySelector('[popup-element="popup"][form-name="desire"]')

if (addFormWrapper) {
    addFormWrapper.addEventListener('click', function (event) {
        let target = event.target

        if (target.getAttribute('desire-form-elem') == 'phone') {
            mobileMaskInput()
        }
    })
}