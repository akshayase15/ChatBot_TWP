document.addEventListener("DOMContentLoaded", () => {
    const chatMessages = document.getElementById("chat-messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");
    const clearButton = document.getElementById("clear-button");

    sendButton.addEventListener("click", () => {
        const message = userInput.value.trim();
        if (message !== "") {
            // Display user message
            displayMessage(message, "user");

            // Send message to backend
            sendMessageToBackend(message);

            // Clear input field
            userInput.value = "";
        }
    });

    clearButton.addEventListener("click", () => {
        // Send a GET request to the /clear endpoint
        fetch("http://127.0.0.1:8000/clear")
            .then(response => response.json())
            .then(data => {
                console.log(data.message);  // Log the response message
                chatMessages.innerHTML = "";  // Clear the chat container
            })
            .catch(error => console.error("Error:", error));
    });

    function displayMessage(message, sender) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${sender}`;

        const formattedMessage = parseMessage(message);

        // Set the innerHTML of the message div with formatted content
        messageDiv.innerHTML = formattedMessage;

        chatMessages.appendChild(messageDiv);

        // Scroll to the bottom to show the latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function parseMessage(message) {
        // Handle new lines: Replace new lines with <br> tags
        const messageWithLineBreaks = message.replace(/\n/g, "<br>");

        // Handle bold text: Wrap bold text with <b> tags
        const messageWithBoldText = messageWithLineBreaks.replace(/\*([^\*]+)\*/g, "<b>$1</b>");

        return messageWithBoldText;
    }

    function sendMessageToBackend(message) {
        // Show the loading animation
        const loadingAnimation = document.querySelector(".middle");
        loadingAnimation.style.display = "block";
    
        fetch(`http://127.0.0.1:8000/chatbot/${encodeURIComponent(message)}`, {
            method: "POST",
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const botResponse = data.message;
    
            // Hide the loading animation
            loadingAnimation.style.display = "none";
    
            // Display bot response or apology if response is missing
            if (botResponse) {
                displayMessage(botResponse, "bot");
            } else {
                displayMessage("I'm sorry, but I couldn't retrieve a response at the moment.", "bot");
            }
        })
        .catch(error => {
            // Hide the loading animation on error
            loadingAnimation.style.display = "none";
            console.error("Error:", error);
        });
    }
    

});
