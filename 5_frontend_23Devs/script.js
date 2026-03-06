document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы формы
    const form = document.getElementById('registration-form');
    const firstNameInput = document.getElementById('first-name');
    const lastNameInput = document.getElementById('last-name');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const passwordConfirmInput = document.getElementById('password-confirm');
    const birthDayInput = document.getElementById('birth-day');
    const submitButton = document.getElementById('form-button');
    
    // Элементы для отображения ошибок
    const firstNameError = document.getElementById('first-name-error');
    const lastNameError = document.getElementById('last-name-error');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');
    const passwordConfirmError = document.getElementById('password-confirm-error');
    const birthDayError = document.getElementById('birth-day-error');
    
    // Элементы требований к паролю
    const lengthReq = document.getElementById('length-req');
    const digitReq = document.getElementById('digit-req');
    const lowercaseReq = document.getElementById('lowercase-req');
    const uppercaseReq = document.getElementById('uppercase-req');
    const specialReq = document.getElementById('special-req');
    
    // Сводка валидации
    const validationSummary = document.getElementById('validation-summary');
    const errorList = document.getElementById('error-list');
    
    // Кнопки показа/скрытия пароля
    const togglePasswordBtn = document.getElementById('toggle-password');
    const togglePasswordConfirmBtn = document.getElementById('toggle-password-confirm');
    
    // Текущее состояние валидности формы
    const formState = {
        firstName: false,
        lastName: false,
        email: false,
        password: false,
        passwordConfirm: false,
        birthDay: false
    };
    
    // Обоснование длины имени и фамилии:
    // - Минимум 2 символа: самые короткие имена (Ли, Эд, Ян и т.д.)
    // - Максимум 30 символов: достаточно для самых длинных имен и фамилий
    //   (например, "Александра-Виктория" или двойные фамилии)
    const NAME_REGEX = /^[A-Za-zА-Яа-яЁё\-']{2,30}$/;
    
    // Функция для проверки имени/фамилии
    function validateName(name, fieldName) {
        if (!name.trim()) {
            return { isValid: false, message: 'Это поле обязательно для заполнения' };
        }
        
        if (!NAME_REGEX.test(name)) {
            return { 
                isValid: false, 
                message: 'Имя может содержать только буквы, дефисы и апострофы (2-30 символов)' 
            };
        }
        
        return { isValid: true, message: '' };
    }
    
    // Функция для проверки email
    function validateEmail(email) {
        if (!email.trim()) {
            return { isValid: false, message: 'Это поле обязательно для заполнения' };
        }
        
        // Простая, но эффективная проверка email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            return { isValid: false, message: 'Введите действительный email-адрес' };
        }
        
        return { isValid: true, message: '' };
    }
    
    // Функция для проверки пароля
    function validatePassword(password) {
        if (!password.trim()) {
            return { 
                isValid: false, 
                message: 'Это поле обязательно для заполнения',
                requirements: { length: false, digit: false, lowercase: false, uppercase: false, special: false }
            };
        }
        
        // Проверяем отдельные требования
        const hasMinLength = password.length >= 8;
        const hasDigit = /\d/.test(password);
        const hasLowercase = /[a-zа-яё]/.test(password);
        const hasUppercase = /[A-ZА-ЯЁ]/.test(password);
        const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);
        
        const isValid = hasMinLength && hasDigit && hasLowercase && hasUppercase && hasSpecial;
        
        // Обновляем отображение требований
        updatePasswordRequirements(hasMinLength, hasDigit, hasLowercase, hasUppercase, hasSpecial);
        
        if (!isValid) {
            let message = 'Пароль должен содержать: ';
            const errors = [];
            
            if (!hasMinLength) errors.push('минимум 8 символов');
            if (!hasDigit) errors.push('хотя бы одну цифру');
            if (!hasLowercase) errors.push('хотя бы одну строчную букву');
            if (!hasUppercase) errors.push('хотя бы одну заглавную букву');
            if (!hasSpecial) errors.push('хотя бы один специальный символ');
            
            message += errors.join(', ');
            
            return { 
                isValid: false, 
                message: message,
                requirements: { 
                    length: hasMinLength, 
                    digit: hasDigit, 
                    lowercase: hasLowercase, 
                    uppercase: hasUppercase, 
                    special: hasSpecial 
                }
            };
        }
        
        return { 
            isValid: true, 
            message: '',
            requirements: { 
                length: hasMinLength, 
                digit: hasDigit, 
                lowercase: hasLowercase, 
                uppercase: hasUppercase, 
                special: hasSpecial 
            }
        };
    }
    
    // Функция для обновления отображения требований к паролю
    function updatePasswordRequirements(length, digit, lowercase, uppercase, special) {
        updateRequirementElement(lengthReq, length);
        updateRequirementElement(digitReq, digit);
        updateRequirementElement(lowercaseReq, lowercase);
        updateRequirementElement(uppercaseReq, uppercase);
        updateRequirementElement(specialReq, special);
    }
    
    function updateRequirementElement(element, isValid) {
        if (isValid) {
            element.classList.add('valid');
            element.classList.remove('invalid');
            element.querySelector('i').className = 'fas fa-check-circle';
        } else {
            element.classList.add('invalid');
            element.classList.remove('valid');
            element.querySelector('i').className = 'fas fa-circle';
        }
    }
    
    // Функция для проверки подтверждения пароля
    function validatePasswordConfirm(password, passwordConfirm) {
        if (!passwordConfirm.trim()) {
            return { isValid: false, message: 'Это поле обязательно для заполнения' };
        }
        
        if (password !== passwordConfirm) {
            return { isValid: false, message: 'Пароли не совпадают' };
        }
        
        return { isValid: true, message: '' };
    }
    
    // Функция для проверки даты рождения
    function validateBirthDay(dateString) {
        if (!dateString) {
            return { isValid: false, message: 'Это поле обязательно для заполнения' };
        }
        
        const birthDate = new Date(dateString);
        const today = new Date();
        
        // Проверяем, что дата не в будущем
        if (birthDate > today) {
            return { isValid: false, message: 'Дата рождения не может быть в будущем' };
        }
        
        // Рассчитываем возраст
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        
        // Если день рождения еще не наступил в этом году, вычитаем 1 год
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        
        if (age < 18) {
            return { isValid: false, message: 'Вам должно быть не менее 18 лет' };
        }
        
        return { isValid: true, message: '' };
    }
    
    // Функция для обновления состояния формы и кнопки отправки
    function updateFormState() {
        const allValid = Object.values(formState).every(value => value === true);
        
        if (allValid) {
            submitButton.disabled = false;
            form.classList.add('valid');
            form.classList.remove('invalid');
            validationSummary.style.display = 'none';
        } else {
            submitButton.disabled = true;
            form.classList.add('invalid');
            form.classList.remove('valid');
        }
    }
    
    // Функция для валидации поля и обновления UI
    function validateField(fieldName, value, validationFunction) {
        const result = validationFunction(value);
        const errorElement = getErrorElement(fieldName);
        
        // Обновляем состояние поля
        const inputElement = document.getElementById(fieldName);
        if (result.isValid) {
            inputElement.classList.add('valid');
            inputElement.classList.remove('invalid');
            errorElement.textContent = '';
            formState[fieldName] = true;
        } else {
            inputElement.classList.add('invalid');
            inputElement.classList.remove('valid');
            errorElement.textContent = result.message;
            formState[fieldName] = false;
        }
        
        // Обновляем сводку валидации
        updateValidationSummary();
        
        // Обновляем состояние формы
        updateFormState();
        
        return result.isValid;
    }
    
    // Функция для получения элемента ошибки по имени поля
    function getErrorElement(fieldName) {
        switch(fieldName) {
            case 'first-name': return firstNameError;
            case 'last-name': return lastNameError;
            case 'email': return emailEmailError;
            case 'password': return passwordError;
            case 'password-confirm': return passwordConfirmError;
            case 'birth-day': return birthDayError;
            default: return null;
        }
    }
    
    // Функция для обновления сводки валидации
    function updateValidationSummary() {
        const errors = [];
        
        // Собираем все ошибки
        if (!formState.firstName && firstNameError.textContent) {
            errors.push(`Имя: ${firstNameError.textContent}`);
        }
        
        if (!formState.lastName && lastNameError.textContent) {
            errors.push(`Фамилия: ${lastNameError.textContent}`);
        }
        
        if (!formState.email && emailError.textContent) {
            errors.push(`Email: ${emailError.textContent}`);
        }
        
        if (!formState.password && passwordError.textContent) {
            errors.push(`Пароль: ${passwordError.textContent}`);
        }
        
        if (!formState.passwordConfirm && passwordConfirmError.textContent) {
            errors.push(`Подтверждение пароля: ${passwordConfirmError.textContent}`);
        }
        
        if (!formState.birthDay && birthDayError.textContent) {
            errors.push(`Дата рождения: ${birthDayError.textContent}`);
        }
        
        // Обновляем сводку
        if (errors.length > 0) {
            errorList.innerHTML = '';
            errors.forEach(error => {
                const li = document.createElement('li');
                li.textContent = error;
                errorList.appendChild(li);
            });
            validationSummary.style.display = 'block';
        } else {
            validationSummary.style.display = 'none';
        }
    }
    
    // Обработчики событий для валидации при потере фокуса
    firstNameInput.addEventListener('blur', function() {
        validateField('first-name', this.value, (value) => validateName(value, 'first-name'));
    });
    
    lastNameInput.addEventListener('blur', function() {
        validateField('last-name', this.value, (value) => validateName(value, 'last-name'));
    });
    
    emailInput.addEventListener('blur', function() {
        validateField('email', this.value, validateEmail);
    });
    
    passwordInput.addEventListener('blur', function() {
        const result = validatePassword(this.value);
        passwordError.textContent = result.message;
        
        if (result.isValid) {
            passwordInput.classList.add('valid');
            passwordInput.classList.remove('invalid');
            formState.password = true;
        } else {
            passwordInput.classList.add('invalid');
            passwordInput.classList.remove('valid');
            formState.password = false;
        }
        
        // Также проверяем подтверждение пароля, если оно уже введено
        if (passwordConfirmInput.value) {
            const confirmResult = validatePasswordConfirm(this.value, passwordConfirmInput.value);
            passwordConfirmError.textContent = confirmResult.message;
            
            if (confirmResult.isValid) {
                passwordConfirmInput.classList.add('valid');
                passwordConfirmInput.classList.remove('invalid');
                formState.passwordConfirm = true;
            } else {
                passwordConfirmInput.classList.add('invalid');
                passwordConfirmInput.classList.remove('valid');
                formState.passwordConfirm = false;
            }
        }
        
        updateValidationSummary();
        updateFormState();
    });
    
    passwordConfirmInput.addEventListener('blur', function() {
        validateField('password-confirm', this.value, (value) => 
            validatePasswordConfirm(passwordInput.value, value));
    });
    
    birthDayInput.addEventListener('blur', function() {
        validateField('birth-day', this.value, validateBirthDay);
    });
    
    // Обработчики для валидации при вводе (для лучшего UX)
    firstNameInput.addEventListener('input', function() {
        if (this.classList.contains('invalid')) {
            const result = validateName(this.value, 'first-name');
            firstNameError.textContent = result.isValid ? '' : result.message;
            
            if (result.isValid) {
                this.classList.add('valid');
                this.classList.remove('invalid');
                formState.firstName = true;
            } else {
                this.classList.add('invalid');
                this.classList.remove('valid');
                formState.firstName = false;
            }
            
            updateValidationSummary();
            updateFormState();
        }
    });
    
    lastNameInput.addEventListener('input', function() {
        if (this.classList.contains('invalid')) {
            const result = validateName(this.value, 'last-name');
            lastNameError.textContent = result.isValid ? '' : result.message;
            
            if (result.isValid) {
                this.classList.add('valid');
                this.classList.remove('invalid');
                formState.lastName = true;
            } else {
                this.classList.add('invalid');
                this.classList.remove('valid');
                formState.lastName = false;
            }
            
            updateValidationSummary();
            updateFormState();
        }
    });
    
    emailInput.addEventListener('input', function() {
        if (this.classList.contains('invalid')) {
            const result = validateEmail(this.value);
            emailError.textContent = result.isValid ? '' : result.message;
            
            if (result.isValid) {
                this.classList.add('valid');
                this.classList.remove('invalid');
                formState.email = true;
            } else {
                this.classList.add('invalid');
                this.classList.remove('valid');
                formState.email = false;
            }
            
            updateValidationSummary();
            updateFormState();
        }
    });
    
    passwordInput.addEventListener('input', function() {
        if (this.classList.contains('invalid')) {
            const result = validatePassword(this.value);
            passwordError.textContent = result.message;
            
            if (result.isValid) {
                this.classList.add('valid');
                this.classList.remove('invalid');
                formState.password = true;
            } else {
                this.classList.add('invalid');
                this.classList.remove('valid');
                formState.password = false;
            }
            
            updateValidationSummary();
            updateFormState();
        }
    });
    
    passwordConfirmInput.addEventListener('input', function() {
        if (this.classList.contains('invalid')) {
            const result = validatePasswordConfirm(passwordInput.value, this.value);
            passwordConfirmError.textContent = result.isValid ? '' : result.message;
            
            if (result.isValid) {
                this.classList.add('valid');
                this.classList.remove('invalid');
                formState.passwordConfirm = true;
            } else {
                this.classList.add('invalid');
                this.classList.remove('valid');
                formState.passwordConfirm = false;
            }
            
            updateValidationSummary();
            updateFormState();
        }
    });
    
    // Обработчики для кнопок показа/скрытия пароля
    togglePasswordBtn.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.querySelector('i').className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
    });
    
    togglePasswordConfirmBtn.addEventListener('click', function() {
        const type = passwordConfirmInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordConfirmInput.setAttribute('type', type);
        this.querySelector('i').className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
    });
    
    // Обработчик отправки формы
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Финализируем валидацию всех полей
        const isFirstNameValid = validateField('first-name', firstNameInput.value, 
            (value) => validateName(value, 'first-name'));
        const isLastNameValid = validateField('last-name', lastNameInput.value, 
            (value) => validateName(value, 'last-name'));
        const isEmailValid = validateField('email', emailInput.value, validateEmail);
        const isPasswordValid = validateField('password', passwordInput.value, 
            (value) => validatePassword(value).isValid);
        const isPasswordConfirmValid = validateField('password-confirm', passwordConfirmInput.value, 
            (value) => validatePasswordConfirm(passwordInput.value, value).isValid);
        const isBirthDayValid = validateField('birth-day', birthDayInput.value, validateBirthDay);
        
        // Если все поля валидны, отправляем форму
        if (isFirstNameValid && isLastNameValid && isEmailValid && 
            isPasswordValid && isPasswordConfirmValid && isBirthDayValid) {
            
            // В реальном приложении здесь был бы AJAX-запрос к серверу
            alert('Форма успешно отправлена! Данные прошли валидацию.');
            
            // Сброс формы
            form.reset();
            Object.keys(formState).forEach(key => formState[key] = false);
            updateFormState();
            validationSummary.style.display = 'none';
            
            // Сброс требований к паролю
            updatePasswordRequirements(false, false, false, false, false);
            
            // Сброс классов полей
            const allInputs = form.querySelectorAll('input');
            allInputs.forEach(input => {
                input.classList.remove('valid', 'invalid');
            });
        } else {
            // Прокручиваем к первой ошибке
            const firstInvalidField = form.querySelector('.invalid');
            if (firstInvalidField) {
                firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstInvalidField.focus();
            }
        }
    });
    
    // Устанавливаем максимальную дату как сегодняшнюю
    const today = new Date().toISOString().split('T')[0];
    birthDayInput.setAttribute('max', today);
    
    // Устанавливаем начальную дату (18 лет назад)
    const initialDate = new Date();
    initialDate.setFullYear(initialDate.getFullYear() - 25);
    birthDayInput.value = initialDate.toISOString().split('T')[0];
    
    // Инициализируем валидацию для предзаполненных полей
    validateField('birth-day', birthDayInput.value, validateBirthDay);
});
