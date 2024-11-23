// static/js/forms.js

export function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
            let valid = true;
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.classList.add('is-invalid');
                    if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorFeedback = document.createElement('div');
                        errorFeedback.className = 'invalid-feedback';
                        errorFeedback.innerText = 'This field is required.';
                        input.parentNode.insertBefore(errorFeedback, input.nextSibling);
                    }
                } else {
                    input.classList.remove('is-invalid');
                    if (input.nextElementSibling && input.nextElementSibling.classList.contains('invalid-feedback')) {
                        input.parentNode.removeChild(input.nextElementSibling);
                    }
                }
            });
            if (!valid) {
                e.preventDefault();
            }
        });
    });
}

// Initialize form validation on document ready
$(document).ready(function() {
    initializeFormValidation();
});
