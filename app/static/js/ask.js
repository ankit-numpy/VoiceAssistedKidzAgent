/**
 * Ask Anything - Voice Q&A functionality
 */

let askState = {
    isListening: false,
    questionHistory: [],
    sessionId: null,
    currentAge: null
};

// Initialize speech recognition
let recognition = null;
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
}

document.addEventListener('DOMContentLoaded', function() {
    // Get session ID
    askState.sessionId = document.getElementById('sessionId')?.value;

    // Voice Input Button
    const voiceInputBtn = document.getElementById('voiceInputBtn');
    if (voiceInputBtn) {
        voiceInputBtn.addEventListener('click', startVoiceInput);
    }

    // Submit Button
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        submitBtn.addEventListener('click', submitQuestion);
    }

    // Clear Button
    const clearBtn = document.getElementById('clearBtn');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearQuestion);
    }

    // Ask Another Button
    const askAnotherBtn = document.getElementById('askAnotherBtn');
    if (askAnotherBtn) {
        askAnotherBtn.addEventListener('click', resetForm);
    }

    // Back Home Button
    const backHomeBtn = document.getElementById('backHomeBtn');
    if (backHomeBtn) {
        backHomeBtn.addEventListener('click', () => window.location.href = '/');
    }

    // Age Select Change
    const ageSelect = document.getElementById('ageSelect');
    if (ageSelect) {
        ageSelect.addEventListener('change', (e) => {
            if (e.target.value) {
                askState.currentAge = parseInt(e.target.value);
            }
        });
    }

    loadHistory();
});

/**
 * Start voice input for question
 */
function startVoiceInput() {
    if (!recognition) {
        showError('Voice recognition not supported in your browser. Please use Chrome, Edge, or Safari.');
        return;
    }

    askState.isListening = true;
    const btn = document.getElementById('voiceInputBtn');
    btn.classList.add('listening');
    btn.disabled = true;

    const voiceText = document.getElementById('voiceInputText');
    voiceText.textContent = 'Listening... speak now!';

    let interimTranscript = '';

    recognition.onstart = () => {
        console.log('Voice recognition started');
    };

    recognition.onresult = (event) => {
        interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;

            if (event.results[i].isFinal) {
                const textInput = document.getElementById('questionInput');
                if (textInput) {
                    textInput.value = (textInput.value + ' ' + transcript).trim();
                }
            } else {
                interimTranscript += transcript;
            }
        }

        // Show interim results
        voiceText.textContent = interimTranscript || 'Listening...';
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        showError(`Error: ${event.error}. Please try again.`);
        stopVoiceInput();
    };

    recognition.onend = () => {
        stopVoiceInput();
    };

    recognition.start();
}

/**
 * Stop voice input
 */
function stopVoiceInput() {
    askState.isListening = false;
    const btn = document.getElementById('voiceInputBtn');
    btn.classList.remove('listening');
    btn.disabled = false;

    const voiceText = document.getElementById('voiceInputText');
    voiceText.textContent = 'Click or Say Your Question';

    if (recognition) {
        recognition.abort();
    }
}

/**
 * Submit the question
 */
async function submitQuestion() {
    const questionInput = document.getElementById('questionInput');
    const question = questionInput?.value?.trim();

    if (!question) {
        showError('Please ask a question!');
        return;
    }

    // Show loading state
    showLoading();

    try {
        const response = await fetch('/api/ask-question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                age: askState.currentAge,
                session_id: askState.sessionId
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to get answer');
        }

        const data = await response.json();

        // Update current age
        askState.currentAge = data.detected_age;

        // Display results
        displayAnswer(data);

        // Add to history
        askState.questionHistory.unshift({
            question: data.question,
            answer: data.answer,
            age: data.detected_age,
            timestamp: new Date().toLocaleTimeString()
        });

        saveHistory();
        updateHistory();

    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
    } finally {
        hideLoading();
    }
}

/**
 * Display the answer
 */
function displayAnswer(data) {
    // Hide input, show answer
    document.querySelector('.input-section').style.display = 'none';
    const answerSection = document.getElementById('answerSection');
    answerSection.style.display = 'block';

    // Display question
    document.getElementById('displayQuestion').textContent = data.question;

    // Display answer
    document.getElementById('answerText').textContent = data.answer;

    // Display age info
    const ageBox = document.getElementById('ageBox');
    ageBox.style.display = 'block';
    document.getElementById('ageValue').textContent = `${data.detected_age} years old`;
    document.getElementById('ageConfidence').textContent = 
        `Detected: ${Math.round(data.age_confidence * 100)}% confident`;

    // Update answer age badge
    document.getElementById('ageEmoji').textContent = getAgeEmoji(data.detected_age);
    document.getElementById('ageText').textContent = data.age_description;

    // Scroll to answer
    answerSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Get emoji for age
 */
function getAgeEmoji(age) {
    if (age <= 6) return '👶';
    if (age <= 8) return '👧';
    if (age <= 10) return '👦';
    return '🧒';
}

/**
 * Clear the question input
 */
function clearQuestion() {
    document.getElementById('questionInput').value = '';
    document.getElementById('questionInput').focus();
}

/**
 * Reset form to ask another question
 */
function resetForm() {
    document.querySelector('.input-section').style.display = 'block';
    document.getElementById('answerSection').style.display = 'none';
    document.getElementById('ageBox').style.display = 'none';
    clearQuestion();
    document.getElementById('ageSelect').value = '';
    document.getElementById('questionInput').focus();
}

/**
 * Show loading state
 */
function showLoading() {
    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('answerSection').style.display = 'none';
}

/**
 * Hide loading state
 */
function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
}

/**
 * Show error message
 */
function showError(message) {
    const errorBox = document.getElementById('errorBox');
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorBox.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Close error message
 */
function closeError() {
    document.getElementById('errorBox').style.display = 'none';
}

/**
 * Record feedback on answer
 */
function recordFeedback(isHelpful) {
    const message = isHelpful ? 'Thanks! I\'m learning!' : 'Thanks for the feedback!';
    showError(message);
    setTimeout(closeError, 2000);
}

/**
 * Update history display
 */
function updateHistory() {
    const historyList = document.getElementById('historyList');
    
    if (askState.questionHistory.length === 0) {
        historyList.innerHTML = '<p class="empty-history">No questions asked yet.</p>';
        return;
    }

    historyList.innerHTML = askState.questionHistory
        .map((item, idx) => `
            <div class="history-item" onclick="loadHistoryItem(${idx})">
                <div class="history-q">❓ ${item.question}</div>
                <div class="history-meta">
                    <span>Age ${item.age}</span>
                    <span>${item.timestamp}</span>
                </div>
            </div>
        `).join('');
}

/**
 * Load a history item
 */
function loadHistoryItem(index) {
    const item = askState.questionHistory[index];
    if (item) {
        document.querySelector('.input-section').style.display = 'none';
        displayAnswer({
            question: item.question,
            answer: item.answer,
            detected_age: item.age,
            age_confidence: 1.0,
            age_description: getAgeDescription(item.age)
        });
    }
}

/**
 * Get age description
 */
function getAgeDescription(age) {
    if (age <= 6) return 'Early Reader (K-1st Grade)';
    if (age <= 8) return 'Elementary Reader (2nd-3rd Grade)';
    if (age <= 10) return 'Middle Elementary (4th-5th Grade)';
    return 'Upper Elementary (6th+ Grade)';
}

/**
 * Local storage - save history
 */
function saveHistory() {
    try {
        localStorage.setItem('askAnyHistory', JSON.stringify(askState.questionHistory));
    } catch (e) {
        console.warn('Could not save history to localStorage');
    }
}

/**
 * Load history from local storage
 */
function loadHistory() {
    try {
        const saved = localStorage.getItem('askAnyHistory');
        if (saved) {
            askState.questionHistory = JSON.parse(saved);
            updateHistory();
        }
    } catch (e) {
        console.warn('Could not load history from localStorage');
    }
}
