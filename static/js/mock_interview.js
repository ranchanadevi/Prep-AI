// Prep AI — Mock Interview Controller Script

document.addEventListener('DOMContentLoaded', () => {
    const interviewForm = document.getElementById('interviewForm');
    const answerInput = document.getElementById('answerInput');
    const questionText = document.getElementById('questionText');
    const currentQNum = document.getElementById('currentQNum');
    const totalQNum = document.getElementById('totalQNum');
    const feedbackSection = document.getElementById('feedbackSection');
    const submitBtn = document.getElementById('submitBtn');
    
    // Evaluation scores elements
    const commScoreVal = document.getElementById('commScoreVal');
    const techScoreVal = document.getElementById('techScoreVal');
    const confScoreVal = document.getElementById('confScoreVal');
    const suggestionsText = document.getElementById('suggestionsText');
    
    let isEvaluated = false;

    if (interviewForm && answerInput && submitBtn) {
        interviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (isEvaluated) {
                // User has seen feedback and wants to move to the next question
                window.location.reload(); // Reload page to fetch the next question from the session
                return;
            }

            const answer = answerInput.value.trim();
            if (!answer) {
                alert("Please type an answer before submitting.");
                return;
            }

            // Show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Evaluating answer...
            `;
            answerInput.disabled = true;

            try {
                // Post answer to server for evaluation
                const response = await fetch('/mock-interview/evaluate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ answer: answer })
                });

                const data = await response.json();
                
                if (data.status === 'success') {
                    // Populate score feedback cards
                    if (commScoreVal) commScoreVal.textContent = `${data.feedback.communication_score}/10`;
                    if (techScoreVal) techScoreVal.textContent = `${data.feedback.technical_score}/10`;
                    if (confScoreVal) confScoreVal.textContent = `${data.feedback.confidence_score}/10`;
                    if (suggestionsText) suggestionsText.textContent = data.feedback.suggestions;

                    // Unhide feedback section
                    if (feedbackSection) {
                        feedbackSection.classList.remove('d-none');
                        feedbackSection.scrollIntoView({ behavior: 'smooth' });
                    }

                    // Change button behavior
                    isEvaluated = true;
                    submitBtn.disabled = false;
                    
                    const isLast = data.is_last;
                    if (isLast) {
                        submitBtn.textContent = "Finish & View Performance Summary";
                        submitBtn.className = "btn btn-success w-100 py-3 mt-3";
                        // Override action to redirect to summary
                        interviewForm.onsubmit = (event) => {
                            event.preventDefault();
                            window.location.href = "/mock-interview/summary";
                        };
                    } else {
                        submitBtn.textContent = "Proceed to Next Question";
                        submitBtn.className = "btn btn-primary w-100 py-3 mt-3";
                    }
                } else {
                    alert(data.message || "Could not evaluate answer. Please try again.");
                    submitBtn.disabled = false;
                    submitBtn.textContent = "Submit Answer";
                    answerInput.disabled = false;
                }
            } catch (err) {
                console.error(err);
                alert("An error occurred during evaluation. Please try again.");
                submitBtn.disabled = false;
                submitBtn.textContent = "Submit Answer";
                answerInput.disabled = false;
            }
        });
    }
});
