const API_URL = "http://127.0.0.1:8000";

const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");


function addMessage(message, sender) {

    const messageDiv = document.createElement("div");

    messageDiv.className = `message ${sender}-message`;

    if (sender === "bot") {
        const avatar = document.createElement("div");
        avatar.className = "message-avatar";
        avatar.textContent = "AI";
        messageDiv.appendChild(avatar);
    }

    const content = document.createElement("div");
    content.className = "message-content";

    const paragraph = document.createElement("p");

    paragraph.style.whiteSpace = "pre-line";
    paragraph.textContent = message;

    content.appendChild(paragraph);
    messageDiv.appendChild(content);

    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;
    return messageDiv;
}


function sendSuggestion(message) {

    userInput.value = message;

    sendMessage();

}


async function sendMessage() {

    const message = userInput.value.trim();

    if (!message || sendButton.disabled) {
        return;
    }

    addMessage(message, "user");

    userInput.value = "";

    sendButton.disabled = true;

    const loadingMessage = addMessage(
        "I'm investigating your request. Please wait...",
        "bot"
    );

    try {

        const response = await fetch(`${API_URL}/chat`, {

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
            throw new Error(data.detail || "Something went wrong.");
        }

        // Remove the temporary loading message.
        loadingMessage.remove();

        addMessage(data.reply, "bot");

    } catch (error) {

        loadingMessage.remove();

        addMessage(
            "Sorry, I couldn't process your request. Please check whether the backend is running.",
            "bot"
        );

        console.error(error);

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