// Authentication page specific JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeAuthPage();
});

function initializeAuthPage() {
    // Password strength indicator
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    
    if (passwordInput) {
        passwordInput.addEventListener('input', updatePasswordStrength);
    }
    
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', validatePasswordMatch);
    }
    
    // Form validation
    const authForm = document.querySelector('.auth-form');
    if (authForm) {
        authForm.addEventListener('submit', handleAuthFormSubmit);
    }
    
    // Input animations
    initializeInputAnimations();
    
    // Auto-focus first input
    const firstInput = authForm?.querySelector('input[type="text"], input[type="email"]');
    if (firstInput) {
        setTimeout(() => firstInput.focus(), 500);
    }
}

function updatePasswordStrength() {
    const password = this.value;
    const strengthBar = document.querySelector('.strength-bar');
    
    if (!strengthBar) return;
    
    let strength = 0;
    let className = '';
    
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++;
    if (password.match(/\d/)) strength++;
    if (password.match(/[^a-zA-Z\d]/)) strength++;
    
    switch (strength) {
        case 0:
        case 1:
            className = 'strength-weak';
            break;
        case 2:
        case 3:
            className = 'strength-medium';
            break;
        case 4:
            className = 'strength-strong';
            break;
    }
    
    strengthBar.className = 'strength-bar ' + className;
}

function validatePasswordMatch() {
    const password = document.getElementById('password')?.value;
    const confirmPassword = this.value;
    const confirmGroup = this.closest('.form-group');
    
    if (!confirmGroup || !password) return;
    
    // Remove existing error message
    const existingError = confirmGroup.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    // Remove error class
    confirmGroup.classList.remove('error');
    
    // Add validation if passwords don't match and confirm password has value
    if (confirmPassword && password !== confirmPassword) {
        confirmGroup.classList.add('error');
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.innerHTML = '<i class="fas fa-exclamation-circle"></i> Passwords do not match';
        confirmGroup.appendChild(errorMessage);
    }
}

function handleAuthFormSubmit(e) {
    const form = e.target;
    const submitBtn = form.querySelector('.auth-btn');
    const password = document.getElementById('password')?.value;
    const confirmPassword = document.getElementById('confirm_password')?.value;
    
    // Basic client-side validation
    if (!validateForm(form)) {
        e.preventDefault();
        return;
    }
    
    // Check password match for signup form
    if (confirmPassword && password !== confirmPassword) {
        e.preventDefault();
        showFormError('Passwords do not match');
        return;
    }
    
    // Show loading state
    if (submitBtn) {
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        submitBtn.classList.add('loading');
        
        // Revert after 5 seconds if still processing (fallback)
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.classList.remove('loading');
        }, 5000);
    }
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required]');
    
    inputs.forEach(input => {
        const group = input.closest('.form-group');
        
        // Remove existing errors
        const existingError = group.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        group.classList.remove('error');
        
        // Validate required fields
        if (!input.value.trim()) {
            isValid = false;
            group.classList.add('error');
            const errorMessage = document.createElement('div');
            errorMessage.className = 'error-message';
            errorMessage.innerHTML = '<i class="fas fa-exclamation-circle"></i> This field is required';
            group.appendChild(errorMessage);
        }
        
        // Validate email format
        if (input.type === 'email' && input.value.trim()) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value)) {
                isValid = false;
                group.classList.add('error');
                const errorMessage = document.createElement('div');
                errorMessage.className = 'error-message';
                errorMessage.innerHTML = '<i class="fas fa-exclamation-circle"></i> Please enter a valid email address';
                group.appendChild(errorMessage);
            }
        }
    });
    
    return isValid;
}

function showFormError(message) {
    // Create error flash message
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    const errorMessage = document.createElement('div');
    errorMessage.className = 'flash-message error';
    errorMessage.innerHTML = `
        ${message}
        <span class="close-btn">&times;</span>
    `;
    
    flashContainer.appendChild(errorMessage);
    
    // Add close functionality
    errorMessage.querySelector('.close-btn').addEventListener('click', function() {
        errorMessage.style.animation = 'slideOut 0.3s ease-in forwards';
        setTimeout(() => errorMessage.remove(), 300);
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorMessage.parentElement) {
            errorMessage.style.animation = 'slideOut 0.3s ease-in forwards';
            setTimeout(() => errorMessage.remove(), 300);
        }
    }, 5000);
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

function initializeInputAnimations() {
    const inputs = document.querySelectorAll('.form-group input');
    
    inputs.forEach(input => {
        // Add focus animation
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateY(-2px)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateY(0)';
        });
        
        // Add input validation styling
        input.addEventListener('input', function() {
            if (this.value.trim()) {
                this.classList.add('has-value');
            } else {
                this.classList.remove('has-value');
            }
        });
    });
}

// Add CSS for additional animations
const authStyles = document.createElement('style');
authStyles.textContent = `
    .form-group {
        transition: transform 0.3s ease;
    }
    
    input.has-value {
        border-color: #10b981 !important;
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    /* Enhanced floating animation for auth page */
    .auth-card {
        animation: floatAuth 6s ease-in-out infinite;
    }
    
    @keyframes floatAuth {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
`;
document.head.appendChild(authStyles);