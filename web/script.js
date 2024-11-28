document.addEventListener("DOMContentLoaded", () => {
    const chatbox = document.getElementById("chatbox");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const voiceBtn = document.getElementById("voice-btn");

    const appendMessage = (message, sender) => {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("mb-2", sender === "user" ? "text-right" : "text-left");
        msgDiv.innerHTML = `<span class="inline-block px-4 py-2 bg-${sender === "user" ? "blue" : "gray"}-200 rounded">${message}</span>`;
        chatbox.appendChild(msgDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    };

    sendBtn.addEventListener("click", async () => {
        const input = userInput.value.trim();
        if (input) {
            appendMessage(input, "user");
            const response = await eel.get_response(input)();
            appendMessage(response, "bot");
            userInput.value = "";
        }
    });

    voiceBtn.addEventListener("click", async () => {
        const result = await eel.listen_and_respond()();
        appendMessage(result.user_input, "user");
        appendMessage(result.response, "bot");
    });
});
