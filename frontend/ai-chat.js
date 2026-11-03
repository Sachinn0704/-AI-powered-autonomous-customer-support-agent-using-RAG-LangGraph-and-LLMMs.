const API_URL = "http://127.0.0.1:8000";

const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const sourceArea = document.getElementById("sourceArea");


function addMessage(message, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.className = `message ${sender}-message`;

    const content = document.createElement("div");

    content.className = "message-content";
    content.textContent = message;

    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageDiv;
}


async function sendMessage() {

    const message = userInput.value.trim();

    if (!message || sendButton.disabled) {
        return;
    }

    addMessage(message, "user");

    userInput.value = "";
    sendButton.disabled = true;

    sourceArea.textContent = "";

    const loadingMessage = addMessage(
        "Thinking and searching the knowledge base...",
        "bot"
    );

    try {

        const response = await fetch(`${API_URL}/ai-chat`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                customer_id: 1,
                message: message
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }

        loadingMessage.remove();

        addMessage(data.reply, "bot");

        if (data.sources && data.sources.length > 0) {

            sourceArea.textContent =
                "Sources: " + data.sources.join(", ");

        }

    } catch (error) {

        loadingMessage.remove();

        addMessage(
            "Sorry, I couldn't process your question. Please check the AI backend and Ollama service.",
            "bot"
        );

        console.error("AI Chat Error:", error);

    } finally {

        sendButton.disabled = false;
        userInput.focus();

    }
}


userInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});
