// context_simulation.js
// Welcome to SkillBridge AI — your personal roadmap mentor
// This script simulates how SkillBridge AI remembers recent chat messages
// and forgets older ones when the context limit is reached.

// Step 1: Create an array to store chat messages
let chatHistory = [];

// Step 2: Set the maximum context limit (number of messages remembered)
const CONTEXT_LIMIT = 5;

// Step 3: Function to add a message to chat history
function addMessage(sender, text) {
  chatHistory.push({ sender, text });

  // Step 4: If chat exceeds the limit, remove the oldest message
  if (chatHistory.length > CONTEXT_LIMIT) {
    chatHistory.shift();
  }

  // Print the current chat history
  console.log("💬 Current SkillBridge Chat Context:");
  chatHistory.forEach((msg) => {
    console.log(`${msg.sender}: ${msg.text}`);
  });
  console.log("----------------------------");
}

// Step 5: Simulate a conversation with SkillBridge AI
console.log("👋 Welcome to SkillBridge AI — Bridge your skills to success!\n");

addMessage("User", "Hi SkillBridge!");
addMessage("SkillBridge AI", "Hello! I’m your personal learning mentor. How can I help you today?");
addMessage("User", "Can you help me plan a roadmap for full-stack development?");
addMessage("SkillBridge AI", "Of course! Let’s start by identifying your current skills.");
addMessage("User", "I know HTML, CSS, and basic JavaScript.");
addMessage("SkillBridge AI", "Perfect! We’ll build on that and include React, Node.js, and MongoDB in your next phase.");
addMessage("User", "That sounds great, thank you!");
