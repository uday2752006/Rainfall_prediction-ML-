// Flash messages close functionality
document.addEventListener('DOMContentLoaded', function() {
    // Close flash messages
    const closeButtons = document.querySelectorAll('.close-btn');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.style.animation = 'slideOut 0.3s ease-in forwards';
            setTimeout(() => {
                this.parentElement.remove();
            }, 300);
        });
    });

    // Auto-remove flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            if (message.parentElement) {
                message.style.animation = 'slideOut 0.3s ease-in forwards';
                setTimeout(() => message.remove(), 300);
            }
        }, 5000);
    });

    // Prediction form handling
    const predictionForm = document.getElementById('prediction-form');
    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePrediction);
    }
});

async function handlePrediction(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    // Show loading state
    submitBtn.innerHTML = '<div class="loading"></div> Predicting...';
    submitBtn.disabled = true;
    
    try {
        const formData = new FormData(form);
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResult(result);
        } else {
            showError(result.error || 'Prediction failed');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        // Restore button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

function displayResult(result) {
    const resultContainer = document.getElementById('result');
    const predictionText = document.getElementById('prediction-text');
    const confidenceElement = document.getElementById('confidence');
    const featuresList = document.getElementById('features-list');
    
    // Set prediction text with emoji
    predictionText.textContent = result.prediction;
    predictionText.className = 'prediction-text ' + (result.result_class || 
        (result.prediction.includes('Expected') ? 'rain-expected' : 'no-rain'));
    
    // Set confidence
    confidenceElement.textContent = `Confidence: ${result.confidence}%`;
    confidenceElement.style.color = result.confidence > 70 ? '#10b981' : 
                                   result.confidence > 50 ? '#f59e0b' : '#ef4444';
    
    // Set features
    featuresList.innerHTML = '';
    for (const [feature, value] of Object.entries(result.features)) {
        const featureItem = document.createElement('div');
        featureItem.className = 'feature-item';
        featureItem.innerHTML = `
            <span class="feature-name">${formatFeatureName(feature)}</span>
            <span class="feature-value">${value}</span>
        `;
        featuresList.appendChild(featureItem);
    }
    
    // Show result container with animation
    resultContainer.style.display = 'block';
    resultContainer.style.animation = 'fadeInUp 0.6s ease-out';
    
    // Scroll to results
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function formatFeatureName(feature) {
    return feature.split('_').map(word => 
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

function showError(message) {
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

// Add CSS for slideOut animation
const style = document.createElement('style');
style.textContent = `
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
`;
document.head.appendChild(style);