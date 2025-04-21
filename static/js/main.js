document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('input-text');
    const outputText = document.getElementById('output-text');
    const enhanceButton = document.getElementById('enhance-button');
    const clearButton = document.getElementById('clear-button');
    const thinkingAnimation = document.getElementById('thinking');
    const ratingButtons = document.querySelectorAll('.rating-btn');
    const outputContainer = document.getElementById('output-container'); // Get the container
    
    let currentInteractionId = null;

    // Focus input on page load
    inputText.focus();

    // Enhance button click handler
    enhanceButton.addEventListener('click', function() {
        enhanceText();
    });

    // Enter key to submit
    inputText.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            e.preventDefault();
            enhanceText();
        }
    });

    // Clear button click handler
    clearButton.addEventListener('click', function() {
        inputText.value = '';
        outputText.innerHTML = '';
        inputText.focus();
        
        // Add button click animation
        this.classList.add('pulse');
        setTimeout(() => this.classList.remove('pulse'), 300);
    });

    // Feedback rating handler
    ratingButtons.forEach(button => {
        button.addEventListener('click', function() {
            const rating = this.getAttribute('data-rating');
            
            // Visual feedback
            ratingButtons.forEach(btn => btn.classList.remove('selected'));
            this.classList.add('selected');
            
            // Animate icon
            this.querySelector('i').classList.add('fa-beat');
            setTimeout(() => {
                this.querySelector('i').classList.remove('fa-beat');
            }, 800);
            
            // Send feedback to server
            if (currentInteractionId) {
                sendFeedback(rating, currentInteractionId);
            }
        });
    });

    // Function to enhance text
    function enhanceText() {
        const text = inputText.value.trim();
        
        if (!text) {
            shakeElement(inputText);
            return;
        }
        
        // Show thinking animation
        outputText.style.display = 'none';
        thinkingAnimation.style.display = 'flex';
        
        // Disable button during processing
        enhanceButton.disabled = true;
        enhanceButton.classList.add('disabled');
        
        // Clear previous duration message
        const existingDuration = outputContainer.querySelector('.duration-info');
        if (existingDuration) {
            existingDuration.remove();
        }

        // Send to server
        fetch('/enhance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
            // Hide thinking animation
            thinkingAnimation.style.display = 'none';
            outputText.style.display = 'block';
            
            if (data.error) {
                outputText.innerHTML = `<span class="error">Error: ${data.error}</span>`;
            } else {
                // Store the interaction ID for feedback
                currentInteractionId = data.id;
                
                // Display with typing animation
                typeWriterEffect(outputText, data.enhanced_text);

                // Display duration after typing finishes (or immediately if preferred)
                if (data.duration !== null && data.duration !== undefined) {
                    const durationElement = document.createElement('p');
                    durationElement.classList.add('duration-info'); // Add class for styling
                    durationElement.textContent = `Enhancement took ${data.duration.toFixed(2)} seconds.`;
                    // Append after the output text div
                    outputContainer.appendChild(durationElement);
                }
            }
            
            // Re-enable button
            enhanceButton.disabled = false;
            enhanceButton.classList.remove('disabled');
        })
        .catch(error => {
            console.error('Error:', error);
            thinkingAnimation.style.display = 'none';
            outputText.style.display = 'block';
            outputText.innerHTML = '<span class="error">Server error. Please try again later.</span>';
            
            enhanceButton.disabled = false;
            enhanceButton.classList.remove('disabled');
        });
    }

    // Type writer effect for the enhanced text
    function typeWriterEffect(element, text, speed = 10) {
        let i = 0;
        element.innerHTML = '';
        
        function typeCharacter() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
                setTimeout(typeCharacter, speed);
            } else {
                // Add a success flash when completed
                element.classList.add('success-animation');
                setTimeout(() => element.classList.remove('success-animation'), 500);
            }
        }
        
        typeCharacter();
    }

    // Send feedback to server
    function sendFeedback(rating, interactionId) {
        fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                feedback: rating,
                interactionId: interactionId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Feedback recorded');
            }
        })
        .catch(error => {
            console.error('Error sending feedback:', error);
        });
    }

    // Shake animation for error feedback
    function shakeElement(element) {
        element.classList.add('shake');
        setTimeout(() => {
            element.classList.remove('shake');
        }, 500);
    }

    // Add shake animation CSS dynamically
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
            20%, 40%, 60%, 80% { transform: translateX(5px); }
        }
        
        .shake {
            animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .pulse {
            animation: pulse 0.3s ease;
        }
        
        .disabled {
            opacity: 0.7;
            cursor: not-allowed;
        }
    `;
    document.head.appendChild(style);

    // Add some basic styling for the duration info
    const durationStyle = document.createElement('style');
    durationStyle.innerHTML = `
        .duration-info {
            font-size: 0.85rem;
            color: var(--gray-color);
            text-align: right;
            margin-top: 0.5rem;
            padding-right: 0.5rem;
        }
    `;
    document.head.appendChild(durationStyle);
});
