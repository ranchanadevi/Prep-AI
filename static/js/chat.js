// Prep AI — Chatbot Client Script

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');
    const clearChatBtn = document.getElementById('clearChatBtn');

    // Scroll chat area to bottom
    const scrollToBottom = () => {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    };

    scrollToBottom();

    // Create typing indicator element
    const createTypingIndicator = () => {
        const div = document.createElement('div');
        div.className = 'chat-bubble bot typing-indicator-bubble';
        div.innerHTML = `
            <div class="spinner-container">
                <span>Prep AI is thinking</span>
                <div class="dot-flashing"></div>
            </div>
        `;
        return div;
    };

    if (chatForm && chatInput && chatMessages) {
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = chatInput.value.trim();
            if (!message) return;

            // 1. Add user message to UI
            const userBubble = document.createElement('div');
            userBubble.className = 'chat-bubble user';
            userBubble.textContent = message;
            chatMessages.appendChild(userBubble);
            chatInput.value = '';
            scrollToBottom();

            // 2. Add typing indicator
            const typingIndicator = createTypingIndicator();
            chatMessages.appendChild(typingIndicator);
            scrollToBottom();

            try {
                // 3. Post to backend
                const response = await fetch('/chatbot/send', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                
                // Remove typing indicator
                typingIndicator.remove();

                // 4. Render response
                const botBubble = document.createElement('div');
                botBubble.className = 'chat-bubble bot';
                
                if (data.status === 'success') {
                    // Render markdown using simple conversion or text
                    // If we have markdown, we can format it nicely or just set innerHTML
                    // Let's use marked.js if loaded, otherwise fallback to plain text with newlines
                    if (window.marked) {
                        botBubble.innerHTML = marked.parse(data.response);
                    } else {
                        botBubble.innerHTML = data.response.replace(/\n/g, '<br>');
                    }
                } else {
                    botBubble.textContent = data.message || "An error occurred. Please try again.";
                }
                
                chatMessages.appendChild(botBubble);
                scrollToBottom();

            } catch (err) {
                console.error(err);
                typingIndicator.remove();
                
                const errBubble = document.createElement('div');
                errBubble.className = 'chat-bubble bot text-danger';
                errBubble.textContent = "Unable to connect to the server. Please check your network.";
                chatMessages.appendChild(errBubble);
                scrollToBottom();
            }
        });
    }

    // Clear chat button handler
    if (clearChatBtn) {
        clearChatBtn.addEventListener('click', async () => {
            if (confirm("Are you sure you want to clear this chat session's conversation context?")) {
                try {
                    const response = await fetch('/chatbot/clear', { method: 'POST' });
                    const data = await response.json();
                    if (data.status === 'success') {
                        if (chatMessages) {
                            chatMessages.innerHTML = `
                                <div class="chat-bubble bot">
                                    Hello! I am <strong>Prep AI</strong>, your placement preparation assistant. 
                                    I can help you study for DSA, OOP, OS, Networks, SQL, Java/Python/C/C++, and review resume and HR questions. 
                                    How can I help you today?
                                </div>
                            `;
                        }
                    }
                } catch (err) {
                    console.error("Error clearing chat session:", err);
                }
            }
        });
    }
});
