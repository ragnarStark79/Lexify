document.addEventListener('DOMContentLoaded', function() {
    // --- Enhancer Page Specific Elements & Logic ---
    const inputText = document.getElementById('input-text');
    const outputText = document.getElementById('output-text');
    const enhanceButton = document.getElementById('enhance-button');
    const clearButton = document.getElementById('clear-button');
    const thinkingAnimation = document.getElementById('thinking');
    const ratingButtons = document.querySelectorAll('.rating-btn');
    const outputContainer = document.getElementById('output-container'); // Get the container
    const feedbackSection = document.getElementById('feedback-section'); // Get feedback section

    let currentInteractionId = null;

    // --- Scroll Animation Logic (Runs on all pages) ---
    const animatedElements = document.querySelectorAll('.animate-on-scroll');

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const delay = entry.target.getAttribute('data-delay') || 0;
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, parseInt(delay));
                    observer.unobserve(entry.target); // Optional: stop observing once animated
                }
            });
        }, {
            threshold: 0.1 // Trigger when 10% of the element is visible
        });

        animatedElements.forEach(el => {
            observer.observe(el);
        });
    } else {
        // Fallback for browsers that don't support IntersectionObserver
        // Make all elements visible immediately
        animatedElements.forEach(el => {
            el.classList.add('visible');
        });
    }
    // --- End Scroll Animation Logic ---


    // Only run enhancer-specific code if the input text element exists
    if (inputText) {
        // Focus input on page load (enhancer page only)
        inputText.focus();

        // Enhance button click handler
        enhanceButton.addEventListener('click', function() {
            enhanceText();
        });

        // Enter key to submit
        inputText.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { // Allow Cmd+Enter on Mac
                e.preventDefault();
                enhanceText();
            }
        });

        // Clear button click handler
        clearButton.addEventListener('click', function() {
            inputText.value = '';
            if (outputText) outputText.innerHTML = '';
            if (outputText) outputText.classList.remove('visible'); // Hide output text
            if (feedbackSection) feedbackSection.classList.remove('visible'); // Hide feedback
            if (outputContainer) outputContainer.classList.remove('success', 'error'); // Reset background state
            inputText.focus();
            // Clear duration if exists
            if (outputContainer) {
                const existingDuration = outputContainer.querySelector('.duration-info');
                if (existingDuration) {
                    existingDuration.remove();
                }
            }
            // Reset rating buttons
            if (ratingButtons) ratingButtons.forEach(btn => btn.classList.remove('selected'));

            // Add button click animation
            this.classList.add('pulse');
            setTimeout(() => this.classList.remove('pulse'), 300);
        });

        // Feedback rating handler
        if (ratingButtons) {
            ratingButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const rating = this.getAttribute('data-rating');

                    // Visual feedback
                    ratingButtons.forEach(btn => btn.classList.remove('selected'));
                    this.classList.add('selected');

                    // Animate icon
                    const icon = this.querySelector('i');
                    if (icon) {
                        icon.classList.add('fa-beat');
                        setTimeout(() => {
                            icon.classList.remove('fa-beat');
                        }, 800);
                    }

                    // Send feedback to server
                    if (currentInteractionId) {
                        sendFeedback(rating, currentInteractionId);
                    }
                });
            });
        }

        // Function to enhance text
        function enhanceText() {
            const text = inputText.value.trim();

            if (!text) {
                shakeElement(inputText);
                return;
            }

            // --- UI Reset and Loading State ---
            outputText.classList.remove('visible'); // Hide previous text for animation
            feedbackSection.classList.remove('visible'); // Hide feedback
            outputContainer.classList.remove('success', 'error'); // Reset background state
            thinkingAnimation.style.display = 'flex'; // Show thinking animation
            outputText.innerHTML = ''; // Clear previous content immediately

            // Disable buttons during processing
            enhanceButton.disabled = true;
            enhanceButton.classList.add('disabled');
            clearButton.disabled = true; // Disable clear button too
            clearButton.classList.add('disabled');

            // Clear previous duration message
            const existingDuration = outputContainer.querySelector('.duration-info');
            if (existingDuration) {
                existingDuration.remove();
            }
            // Reset rating buttons
            ratingButtons.forEach(btn => btn.classList.remove('selected'));

            // Send to server
            fetch('/enhance', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            })
            .then(response => {
                if (!response.ok) {
                    // Try to parse error message from JSON response
                    return response.json().then(err => {
                        throw new Error(err.error || `HTTP error! status: ${response.status}`);
                    }).catch(() => {
                        // Fallback if response is not JSON or doesn't have 'error'
                        throw new Error(`HTTP error! status: ${response.status}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                thinkingAnimation.style.display = 'none'; // Hide thinking animation
                console.log('Received data from /enhance:', data); // <-- Log received data

                if (data.error) {
                    outputText.innerHTML = `<span class="error">Error: ${data.error}</span>`;
                    outputContainer.classList.add('error'); // Error background state
                    outputText.classList.add('visible'); // Show error message
                } else {
                    // Store the interaction ID for feedback (assuming API returns it as 'id')
                    currentInteractionId = data.id; // Make sure your backend sends this!
                    console.log('Set currentInteractionId:', currentInteractionId); // <-- Log the ID being set

                    // Display with typing animation (or just set text and add class)
                    // Using direct set and class for smoother animation defined in CSS
                    outputText.textContent = data.enhanced_text;
                    outputText.classList.add('visible'); // Trigger fade/slide-in animation

                    // Display duration
                    if (data.duration !== null && data.duration !== undefined) {
                        const durationElement = document.createElement('p');
                        durationElement.classList.add('duration-info');
                        durationElement.textContent = `(Took ${data.duration.toFixed(2)}s)`; // Shortened text
                        // Append inside the output container, after the text div
                        outputContainer.appendChild(durationElement);
                    }

                    // Show feedback section after successful enhancement
                    feedbackSection.classList.add('visible');
                }
            })
            .catch(error => {
                thinkingAnimation.style.display = 'none'; // Hide thinking animation on error too
                outputText.innerHTML = `<span class="error">Error: ${error.message}</span>`;
                outputContainer.classList.add('error'); // Error background state
                outputText.classList.add('visible'); // Show error message
                console.error('Fetch error:', error);
            })
            .finally(() => {
                // Re-enable buttons
                enhanceButton.disabled = false;
                enhanceButton.classList.remove('disabled');
                clearButton.disabled = false;
                clearButton.classList.remove('disabled');
            });
        }

        // Send feedback to server
        function sendFeedback(rating, interactionId) {
            console.log(`Attempting to send feedback: rating=${rating}, interactionId=${interactionId}`); // <-- Log values

            // Prevent sending feedback if interactionId is missing
            if (!interactionId) {
                console.error('Cannot send feedback: interactionId is missing.');
                // Optionally, provide user feedback here (e.g., disable buttons temporarily or show a message)
                return;
            }

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
                    console.log('Feedback recorded for interaction:', interactionId);
                    // Optional: Show a small confirmation message
                } else {
                     console.error('Failed to record feedback:', data.error);
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

    } // End of if (inputText) block

    // --- General UI Enhancements (Run on all pages) ---

    // Add shake animation CSS dynamically (if not already added by enhancer logic)
    if (!document.getElementById('dynamic-animations-style')) {
        const style = document.createElement('style');
        style.id = 'dynamic-animations-style'; // Give it an ID to prevent duplicates
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

            /* Success animation for output text - optional */
            .output-text.success-animation {
                 /* Example: subtle glow */
                /* box-shadow: 0 0 15px rgba(40, 167, 69, 0.5); */
            }
        `;
        document.head.appendChild(style);
    }

    // Add duration info styling dynamically (if not already added)
    if (!document.getElementById('duration-info-style')) {
        const durationStyle = document.createElement('style');
        durationStyle.id = 'duration-info-style';
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
    }

});
