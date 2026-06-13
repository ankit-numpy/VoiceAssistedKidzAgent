/**
 * Reading session functionality
 */

let sessionData = {
    sessionId: null,
    passageId: null,
    childId: null,
    currentWordIndex: 0,
    startTime: null,
    words: [],
    isRecording: false
};

document.addEventListener('DOMContentLoaded', function() {
    // Get session data from hidden inputs
    const sessionId = document.getElementById('sessionId')?.value;
    const passageId = document.getElementById('passageId')?.value;
    const childId = document.getElementById('childId')?.value;

    if (sessionId) {
        sessionData.sessionId = sessionId;
        sessionData.passageId = passageId;
        sessionData.childId = childId;
        sessionData.startTime = Date.now();

        // Parse passage text into words
        const passageText = document.getElementById('passageText');
        if (passageText) {
            const text = passageText.textContent.trim();
            sessionData.words = text.split(/\s+/);

            // Wrap words in spans for interactive selection
            const wrappedText = sessionData.words
                .map((word, idx) => `<span class="word" data-index="${idx}">${word}</span>`)
                .join(' ');
            passageText.innerHTML = wrappedText;

            // Add click handlers to words
            document.querySelectorAll('.word').forEach(wordSpan => {
                wordSpan.addEventListener('click', function() {
                    startRecordingWord(this);
                });
            });
        }

        // Button handlers
        const startBtn = document.getElementById('startBtn');
        const stopBtn = document.getElementById('stopBtn');
        const endSessionBtn = document.getElementById('endSessionBtn');

        if (startBtn) startBtn.addEventListener('click', startSession);
        if (stopBtn) stopBtn.addEventListener('click', stopRecording);
        if (endSessionBtn) endSessionBtn.addEventListener('click', endSession);

        // Start timer
        updateTimer();
    }
});

function startSession() {
    console.log('Session started');
    if (!recognition) {
        showNotification('Speech recognition not supported in your browser', 'error');
        return;
    }

    document.getElementById('startBtn').disabled = true;
    document.getElementById('startBtn').textContent = 'Recording...';
}

function startRecordingWord(wordElement) {
    if (!recognition) return;

    const wordIndex = parseInt(wordElement.dataset.index);
    const expectedWord = wordElement.textContent;

    if (sessionData.isRecording) return;

    sessionData.isRecording = true;
    sessionData.currentWordIndex = wordIndex;

    // Visual feedback
    document.querySelectorAll('.word').forEach(w => w.classList.remove('current'));
    wordElement.classList.add('current');

    recognition.onstart = () => {
        console.log('Listening for:', expectedWord);
    };

    recognition.onresult = async (event) => {
        const transcript = Array.from(event.results)
            .map(result => result[0].transcript)
            .join('');

        const spokenWord = transcript.trim();
        console.log('Heard:', spokenWord);

        // Send to API for processing
        const feedback = await apiCall('/api/transcribe', 'POST', {
            session_id: sessionData.sessionId,
            word_index: wordIndex,
            expected_word: expectedWord,
            spoken_word: spokenWord
        });

        if (feedback) {
            displayFeedback(feedback, wordElement);
            updateProgress();
        }

        sessionData.isRecording = false;
        wordElement.classList.remove('current');
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        sessionData.isRecording = false;
        wordElement.classList.remove('current');
    };

    recognition.start();
}

function displayFeedback(feedback, wordElement) {
    const panel = document.getElementById('feedbackPanel');
    if (!panel) return;

    const status = feedback.is_correct ? '✓ Correct!' : '✓ Almost there!';
    const statusClass = feedback.is_correct ? 'correct' : 'incorrect';

    let html = `<p class="word-feedback ${statusClass}">${status} "${feedback.word_index === undefined ? sessionData.words[feedback.word_index] : ''}"</p>`;

    if (feedback.correction) {
        html += `<p class="correction">${feedback.correction}</p>`;
    }

    if (feedback.explanation) {
        html += `<p class="explanation">${feedback.explanation}</p>`;
    }

    if (feedback.encouragement) {
        html += `<p class="encouragement">${feedback.encouragement}</p>`;
    }

    panel.innerHTML = html;
    panel.style.display = 'block';

    // Color the word in the passage
    wordElement.style.color = feedback.is_correct ? 'green' : 'orange';
}

function updateProgress() {
    const total = sessionData.words.length;
    const correct = document.querySelectorAll('.word[style*="color: green"]').length;
    const percentage = (correct / total) * 100;

    const progressFill = document.getElementById('progressFill');
    if (progressFill) {
        progressFill.style.width = percentage + '%';
    }

    const progressText = document.getElementById('progressText');
    if (progressText) {
        progressText.textContent = `${correct} / ${total} words read correctly`;
    }
}

function stopRecording() {
    if (recognition && recognition.abort) {
        recognition.abort();
    }
    sessionData.isRecording = false;

    const startBtn = document.getElementById('startBtn');
    if (startBtn) {
        startBtn.disabled = false;
        startBtn.textContent = '🎤 Start Recording';
    }
}

function updateTimer() {
    if (!sessionData.startTime) return;

    const elapsed = Math.floor((Date.now() - sessionData.startTime) / 1000);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;

    const timerElement = document.getElementById('sessionTimer');
    if (timerElement) {
        timerElement.textContent = 
            `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }

    setTimeout(updateTimer, 1000);
}

async function endSession() {
    const correct = document.querySelectorAll('.word[style*="color: green"]').length;
    const total = sessionData.words.length;
    const elapsed = Math.floor((Date.now() - sessionData.startTime) / 1000);

    const result = await apiCall(`/session/end/${sessionData.sessionId}`, 'POST', {
        duration: elapsed,
        correct: correct,
        total: total
    });

    if (result && result.status === 'success') {
        window.location.href = `/session/results/${sessionData.sessionId}`;
    } else {
        showNotification('Error ending session', 'error');
    }
}

// Utility functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(endpoint, options);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        return null;
    }
}

function showNotification(message, type = 'info') {
    alert(message); // Simple implementation for now
}
