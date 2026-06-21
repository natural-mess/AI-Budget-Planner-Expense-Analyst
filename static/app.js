document.addEventListener("DOMContentLoaded", () => {
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const messagesContainer = document.getElementById("messages-container");
    const chatContainer = document.getElementById("chat-container");
    const loadingIndicator = document.getElementById("loading-indicator");

    // Modal handling
    const settingsBtn = document.getElementById('settings-btn');
    const apiModal = document.getElementById('api-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const saveApiKeyBtn = document.getElementById('save-api-key-btn');
    const apiKeyInput = document.getElementById('api-key-input');
    const modelSelect = document.getElementById('model-select');

    apiKeyInput.value = localStorage.getItem('gemini_api_key') || '';
    modelSelect.value = localStorage.getItem('gemini_model') || 'gemini-flash-lite-latest';

    settingsBtn.addEventListener('click', () => {
        apiModal.classList.remove('hidden');
    });

    closeModalBtn.addEventListener('click', () => {
        apiModal.classList.add('hidden');
        apiKeyInput.value = localStorage.getItem('gemini_api_key') || '';
        modelSelect.value = localStorage.getItem('gemini_model') || 'gemini-flash-lite-latest';
    });

    saveApiKeyBtn.addEventListener('click', () => {
        const key = apiKeyInput.value.trim();
        if (key) {
            localStorage.setItem('gemini_api_key', key);
        } else {
            localStorage.removeItem('gemini_api_key');
        }
        localStorage.setItem('gemini_model', modelSelect.value);
        apiModal.classList.add('hidden');
    });

    // Generate a random session ID for this tab
    const sessionId = "sess_" + Math.random().toString(36).substring(2, 9);

    function formatText(text) {
        return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>');
    }

    function addMessage(text, isUser = false) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${isUser ? 'user' : 'ai'}`;
        
        const avatar = document.createElement("div");
        avatar.className = "avatar";
        avatar.textContent = isUser ? "U" : "AI";
        
        const content = document.createElement("div");
        content.className = "content";
        content.innerHTML = formatText(text);
        
        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);
        messagesContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        addMessage(text, true);
        userInput.value = "";
        loadingIndicator.classList.remove("hidden");

        try {
            const payload = { 
                message: text, 
                session_id: sessionId 
            };
            const apiKey = localStorage.getItem('gemini_api_key');
            if (apiKey) {
                payload.api_key = apiKey;
            }
            const savedModel = localStorage.getItem('gemini_model');
            if (savedModel) {
                payload.model = savedModel;
            }

            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!response.body) throw new Error("ReadableStream not supported");
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let aiText = "";
            let buffer = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                buffer += decoder.decode(value, { stream: true });
                
                let boundary = buffer.indexOf('\n\n');
                while (boundary !== -1) {
                    const eventStr = buffer.slice(0, boundary);
                    buffer = buffer.slice(boundary + 2);
                    
                    const lines = eventStr.split('\n');
                    for (const line of lines) {
                        if (line.startsWith("data: ")) {
                            try {
                                const eventData = JSON.parse(line.substring(6));
                                
                                if (eventData.content && eventData.content.parts) {
                                    for (const part of eventData.content.parts) {
                                        if (part.text) {
                                            aiText += part.text + " ";
                                        }
                                        if (part.function_response && part.function_response.response && part.function_response.response.budget) {
                                            aiText += `\n\n**[Requires Approval]**\n${part.function_response.response.budget}\n`;
                                        }
                                    }
                                }
                            } catch (e) {
                                console.warn("Could not parse event data", e);
                            }
                        }
                    }
                    boundary = buffer.indexOf('\n\n');
                }
            }
            
            if (aiText) {
                addMessage(aiText);
            } else {
                addMessage("Finished processing. Please check console for event streams.");
            }

        } catch (error) {
            console.error(error);
            addMessage(`Error: ${error.message}`);
        } finally {
            loadingIndicator.classList.add("hidden");
        }
    }

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
});
