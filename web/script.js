document.addEventListener("DOMContentLoaded", () => {
    const chatbox = document.getElementById("chatbox");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const voiceBtn = document.getElementById("voice-btn");

    const appendMessage = (message, sender) => {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("mb-3", "flex", sender === "user" ? "justify-end" : "justify-start");
        msgDiv.innerHTML = `
            <span class="inline-block px-4 py-2 rounded-xl max-w-[80%] ${sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-800"}">${message}</span>
        `;
        chatbox.appendChild(msgDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    };

    const appendMessageTypingWithVoice = (message, sender) => {
        const typingMessage = document.createElement("div");
        typingMessage.classList.add("mb-3", "flex", sender === "user" ? "justify-end" : "justify-start");
        typingMessage.innerHTML = `
        <span class="inline-block px-4 py-2 rounded-xl max-w-[80%] ${sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-800"} typing"></span>
    `;
        chatbox.appendChild(typingMessage);
        chatbox.scrollTop = chatbox.scrollHeight;

        const typingSpan = typingMessage.querySelector(".typing");
        let currentIndex = 0;

        // Stop any ongoing speech
        if (speechSynthesis.speaking) {
            speechSynthesis.cancel();
        }

        // Initialize SpeechSynthesis
        const utterance = new SpeechSynthesisUtterance(message);
        utterance.lang = "en-US"; // Set language (customize as needed)

        // Event listener to ensure typing finishes before speaking
        utterance.addEventListener("start", () => {
            console.log("Speech started");
        });

        utterance.addEventListener("end", () => {
            console.log("Speech ended");
        });

        speechSynthesis.speak(utterance);

        // Typing effect: Display one letter at a time
        const typingInterval = setInterval(() => {
            if (currentIndex < message.length) {
                typingSpan.textContent += message[currentIndex];
                currentIndex++;
                chatbox.scrollTop = chatbox.scrollHeight; // Keep scrolling to the latest message
            } else {
                clearInterval(typingInterval);
            }
        }, 50); // Adjust typing speed
    };




    // Button click animations
    [sendBtn, voiceBtn].forEach((btn) => {
        btn.addEventListener("click", () => {
            btn.classList.add("btn-click");
            setTimeout(() => btn.classList.remove("btn-click"), 200);
        });
    });

    sendBtn.addEventListener("click", async () => {
        const input = userInput.value.trim();
        if (input) {
            appendMessage(input, "user");
            userInput.value = ""; // Clear input immediately

            // Fetch bot response and handle typing and voice output
            const botResponse = await eel.get_response(input)();
            appendMessageTypingWithVoice(botResponse, "bot");
        }
    });

    voiceBtn.addEventListener("click", async () => {
        voiceBtn.classList.add("mic-active");
        try {
            const result = await eel.listen_and_respond()();

            // Append user's voice input
            appendMessage(result.user_input, "user");

            // Handle bot response with typing effect and voice output
            appendMessageTypingWithVoice(result.response, "bot");
        } catch (error) {
            appendMessage("Error in voice processing", "bot");
        } finally {
            voiceBtn.classList.remove("mic-active");
        }
    });

});