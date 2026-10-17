/**
 * BlueDesk Client Application
 * Handles secure DOM rendering, Flask API communications, quick prompts,
 * conversation clearing, accessible announcements, and persistent theme switching.
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM References
  const htmlRoot = document.documentElement;
  const themeToggleBtn = document.getElementById('theme-toggle');
  const chatForm = document.getElementById('chat-form');
  const userInput = document.getElementById('user-input');
  const sendBtn = document.getElementById('send-btn');
  const messagesContainer = document.getElementById('messages-container');
  const clearChatBtn = document.getElementById('clear-chat-btn');
  const promptChips = document.querySelectorAll('.prompt-chip');
  const initialTimeSpan = document.getElementById('initial-time');
  const srAnnouncements = document.getElementById('sr-announcements');

  let isProcessing = false;

  // Initialize initial welcome message timestamp
  if (initialTimeSpan) {
    initialTimeSpan.textContent = formatCurrentTime();
  }

  /* ==========================================================================
     Theme Management (Local Storage + System Preference)
     ========================================================================== */
  function initializeTheme() {
    const savedTheme = localStorage.getItem('bluedesk-theme');
    if (savedTheme === 'dark' || savedTheme === 'light') {
      applyTheme(savedTheme);
    } else {
      // Check system color scheme preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      applyTheme(prefersDark ? 'dark' : 'light');
    }
  }

  function applyTheme(theme) {
    htmlRoot.setAttribute('data-theme', theme);
    localStorage.setItem('bluedesk-theme', theme);

    if (themeToggleBtn) {
      const isDark = theme === 'dark';
      const labelText = isDark ? 'Switch to light mode' : 'Switch to dark mode';
      themeToggleBtn.setAttribute('aria-label', labelText);
      const textSpan = themeToggleBtn.querySelector('.theme-toggle-text');
      if (textSpan) {
        textSpan.textContent = isDark ? 'Light mode' : 'Dark mode';
      }
    }
  }

  function toggleTheme() {
    const currentTheme = htmlRoot.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(newTheme);
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', toggleTheme);
  }

  // Listen for system theme changes if user has not explicitly chosen
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('bluedesk-theme')) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });

  initializeTheme();

  /* ==========================================================================
     Time formatting helper
     ========================================================================== */
  function formatCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  /* ==========================================================================
     Accessible announcements
     ========================================================================== */
  function announceToScreenReader(message) {
    if (srAnnouncements) {
      srAnnouncements.textContent = message;
    }
  }

  /* ==========================================================================
     Safe DOM Message Rendering (No unsafe innerHTML)
     ========================================================================== */
  function appendMessage(sender, text, isBot = false) {
    const row = document.createElement('div');
    row.className = `message-row ${isBot ? 'bot-row' : 'user-row'}`;

    const avatar = document.createElement('div');
    avatar.className = `avatar ${isBot ? 'bot-avatar' : 'user-avatar'}`;
    avatar.setAttribute('aria-hidden', 'true');
    avatar.textContent = isBot ? 'BD' : 'You';

    const bubble = document.createElement('div');
    bubble.className = `message-bubble ${isBot ? 'bot-bubble' : 'user-bubble'}`;

    const header = document.createElement('div');
    header.className = 'bubble-header';

    const senderSpan = document.createElement('span');
    senderSpan.className = 'sender-name';
    senderSpan.textContent = sender;

    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-time';
    timeSpan.textContent = formatCurrentTime();

    header.appendChild(senderSpan);
    header.appendChild(timeSpan);

    const textDiv = document.createElement('div');
    textDiv.className = 'bubble-text';
    // STRICT: Safe textContent assignment prevents XSS
    textDiv.textContent = text;

    bubble.appendChild(header);
    bubble.appendChild(textDiv);

    row.appendChild(avatar);
    row.appendChild(bubble);

    messagesContainer.appendChild(row);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    if (isBot) {
      announceToScreenReader(`BlueDesk responded: ${text}`);
    }
  }

  /* ==========================================================================
     Typing / Processing Indicator
     ========================================================================== */
  function showLoadingIndicator() {
    const row = document.createElement('div');
    row.className = 'message-row bot-row';
    row.id = 'typing-indicator';

    const avatar = document.createElement('div');
    avatar.className = 'avatar bot-avatar';
    avatar.setAttribute('aria-hidden', 'true');
    avatar.textContent = 'BD';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble bot-bubble';

    const dots = document.createElement('div');
    dots.className = 'typing-dots';
    dots.setAttribute('aria-label', 'BlueDesk is thinking');

    for (let i = 0; i < 3; i++) {
      const dot = document.createElement('span');
      dot.className = 'typing-dot';
      dots.appendChild(dot);
    }

    bubble.appendChild(dots);
    row.appendChild(avatar);
    row.appendChild(bubble);

    messagesContainer.appendChild(row);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function removeLoadingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
      indicator.remove();
    }
  }

  /* ==========================================================================
     Message Submission Flow
     ========================================================================== */
  async function sendMessage(rawMessage) {
    const message = rawMessage.trim();
    if (!message || isProcessing) {
      return;
    }

    isProcessing = true;
    sendBtn.disabled = true;
    userInput.disabled = true;

    // Render user message to UI safely
    appendMessage('You', message, false);
    userInput.value = '';

    // Show loading indicator
    showLoadingIndicator();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
      });

      removeLoadingIndicator();

      if (!response.ok) {
        throw new Error(`Server returned status: ${response.status}`);
      }

      const data = await response.json();
      if (data && data.reply) {
        appendMessage('BlueDesk', data.reply, true);
      } else {
        appendMessage('BlueDesk', "I received an unformatted response from the desk. Please try again.", true);
      }
    } catch (err) {
      removeLoadingIndicator();
      console.error('Chat request error:', err);
      appendMessage('BlueDesk', "Unable to connect to the help desk service. Please ensure the local server is running.", true);
    } finally {
      isProcessing = false;
      sendBtn.disabled = false;
      userInput.disabled = false;
      userInput.focus();
    }
  }

  // Handle Chat Form Submit
  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    sendMessage(userInput.value);
  });

  // Handle Quick Prompts
  promptChips.forEach((chip) => {
    chip.addEventListener('click', () => {
      const promptText = chip.getAttribute('data-prompt');
      if (promptText && !isProcessing) {
        sendMessage(promptText);
      }
    });
  });

  /* ==========================================================================
     Clear Conversation Functionality
     ========================================================================== */
  function clearConversation() {
    if (isProcessing) return;

    // Reset messages container to initial welcome state
    messagesContainer.innerHTML = '';

    const row = document.createElement('div');
    row.className = 'message-row bot-row';
    row.setAttribute('data-initial', 'true');

    const avatar = document.createElement('div');
    avatar.className = 'avatar bot-avatar';
    avatar.setAttribute('aria-hidden', 'true');
    avatar.textContent = 'BD';

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble bot-bubble';

    const header = document.createElement('div');
    header.className = 'bubble-header';

    const senderSpan = document.createElement('span');
    senderSpan.className = 'sender-name';
    senderSpan.textContent = 'BlueDesk';

    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-time';
    timeSpan.textContent = formatCurrentTime();

    header.appendChild(senderSpan);
    header.appendChild(timeSpan);

    const textDiv = document.createElement('div');
    textDiv.className = 'bubble-text';
    textDiv.textContent = 'Hi! Welcome to BlueDesk. How can I help you today?';

    bubble.appendChild(header);
    bubble.appendChild(textDiv);
    row.appendChild(avatar);
    row.appendChild(bubble);

    messagesContainer.appendChild(row);
    userInput.value = '';
    userInput.focus();

    announceToScreenReader('Conversation has been cleared.');
  }

  if (clearChatBtn) {
    clearChatBtn.addEventListener('click', clearConversation);
  }

  // Initial focus on input
  userInput.focus();
});
