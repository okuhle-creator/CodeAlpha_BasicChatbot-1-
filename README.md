# BlueDesk | A Rule-Based Conversational Help Desk

**CodeAlpha Python Programming Internship — Task 4: Basic Chatbot**

BlueDesk is a clean, modern conversational help desk powered by a deterministic Python rule-based chatbot. It demonstrates how a program responds to user inputs through predefined rules, Python conditional control structures (`if-elif-else`), token and boundary-aware pattern matching, reusable functions, and robust input/output processing.

The project features both an interactive terminal interface and an institutional, responsive web application built with Flask, vanilla JavaScript, and modern CSS custom properties with persistent light/dark mode support.

---

## 1. Project Objectives

- **Demonstrate Core Python Concepts:** Organise conversational rules using standard control flow (`if-elif-else`), reusable functions, safe string normalisation, and loops (`while`).
- **Deterministic Rule-Based Matching:** Implement exact and boundary-aware keyword matching so that user queries trigger predictable, explainable responses without false-positive substrings (e.g. distinguishing `"hi"` from `"this"` or `"bye"` from `"byte"`).
- **Institutional Web Interface:** Build a responsive web interface designed with navy blue, medium blue, pale blue-grey, and white tones, avoiding generic AI/neon gimmicks.
- **Persistent Theme Switching:** Provide a light/dark theme switch that changes CSS custom properties, respects system preferences, and persists across reloads via `localStorage`.
- **Zero Third-Party AI APIs:** The application is self-contained and runs locally without external API keys, machine-learning models, or internet dependencies once installed.

---

## 2. Features

- **Dual-Interface System:**
  - **Web Help Desk:** Powered by Flask with real-time JSON messaging over `/api/chat`.
  - **Terminal Console:** Standalone CLI interface using standard `input()`, `print()`, and an interactive `while` loop.
- **Refined Institutional Design:**
  - Distinctive BlueDesk wordmark and brand status indicator ("Ready").
  - Clear conversation workspace with right-aligned user bubbles and left-aligned chatbot bubbles.
  - Interactive quick-action prompts ("Say hello", "How are you?", "What can you do?", "Say goodbye").
  - "Clear conversation" control that resets the thread without full page reload.
  - Accessible screen reader announcements via ARIA live regions and safe DOM rendering (`textContent` to prevent XSS).
- **Light & Dark Theme Toggle:**
  - One-click toggle between crisp institutional light mode and deep navy/charcoal dark mode.
  - Persisted in browser `localStorage`.
- **Comprehensive Automated Test Suite:**
  - 19 automated unit and integration tests verifying matching logic, boundary safety, empty input handling, and Flask API endpoints.

---

## 3. Technologies Used

- **Language:** Python 3.10+
- **Backend Framework:** Flask 3.0.3 (lightweight WSGI web application framework)
- **Frontend:** HTML5, CSS3 (CSS Custom Properties & Flexbox), Vanilla JavaScript (ES6+ Fetch API)
- **Testing:** Python `unittest` framework

---

## 4. Rule-Based Python Logic Explained

The chatbot core is located in `chatbot.py`. It does not use probabilistic models or external AI services. Instead, it relies on deterministic rules:

### Normalisation & Tokenisation Pipeline
1. **`normalize_text(text)`**: Strips leading and trailing whitespace, converts characters to lowercase, collapses multiple spaces into single spaces, and removes surrounding non-essential punctuation (e.g. converting `"  Hello!  "` to `"hello"`).
2. **`tokenize(text)`**: Splits normalised text into individual word tokens with punctuation stripped to verify exact word boundaries.

### Conditional Matching (`if-elif-else`)
The core function `get_response(message: str) -> str` evaluates incoming queries sequentially:

```python
if cleaned in GREETING_TOKENS or (token_set & {"hello", "hi", "hey"} and len(tokens) <= 3):
    return RESPONSES["greeting"]
elif any(phrase in cleaned for phrase in HOW_ARE_YOU_PHRASES):
    return RESPONSES["how_are_you"]
elif any(phrase in cleaned for phrase in NAME_PHRASES):
    return RESPONSES["name"]
elif any(phrase in cleaned for phrase in CAPABILITIES_PHRASES):
    return RESPONSES["capabilities"]
elif cleaned in HELP_TOKENS or "help" in token_set:
    return RESPONSES["help"]
elif cleaned in THANKS_TOKENS or (token_set & {"thanks", "thx"} and len(tokens) <= 4):
    return RESPONSES["thanks"]
elif cleaned in GOODBYE_TOKENS or (token_set & {"bye", "goodbye", "farewell"} and len(tokens) <= 4):
    return RESPONSES["goodbye"]
else:
    return RESPONSES["fallback"]
```

### Preventing False Substring Matches
Common naive chatbots use `if "hi" in message:`, which incorrectly triggers on `"This is great"` or `"white"`. BlueDesk inspects discrete word tokens and checks string sets so words like `"this"`, `"history"`, `"white"`, and `"byte"` never trigger greeting or farewell rules erroneously.

---

## 5. Conversational Rules Reference

| Intent | Sample User Input | Predefined BlueDesk Response |
|---|---|---|
| **Greeting** | `"Hello"`, `"Hi"`, `"Hey"`, `"Good morning"` | `"Hi! Welcome to BlueDesk. How can I help you today?"` |
| **Wellbeing** | `"How are you?"`, `"How are you doing?"` | `"I'm doing well, thank you for asking! How are you doing today?"` |
| **Identity** | `"What is your name?"`, `"Who are you?"` | `"I'm BlueDesk, a simple rule-based conversational assistant."` |
| **Capabilities** | `"What can you do?"`, `"How can you help?"` | `"I can respond to a variety of common queries using predefined rules. Try saying hello, asking how I am, or asking for help."` |
| **Gratitude** | `"Thank you"`, `"Thanks"`, `"Appreciate it"` | `"You're very welcome! Always happy to help."` |
| **Help / Menu** | `"Help"`, `"Commands"`, `"Guide"` | `"I'm a rule-based help desk assistant. You can try: 'Hello', 'How are you?', 'What can you do?', 'What is your name?', 'Thanks', or 'Goodbye'."` |
| **Farewell** | `"Bye"`, `"Goodbye"`, `"See you"` | `"Goodbye! It was nice chatting with you. Have a great day ahead!"` |
| **Unrecognised** | *(Any unrecognized query)* | `"I'm not sure how to respond to that yet. Try asking for help to see what I understand."` |

---

## 6. Project Directory Structure

```text
CodeAlpha_BasicChatbot/
├── app.py                      # Flask web server and /api/chat endpoints
├── chatbot.py                  # Core rule engine & standalone CLI interface
├── requirements.txt            # Minimal Python dependencies (Flask, Werkzeug)
├── README.md                   # Complete documentation & usage guide
├── .gitignore                  # Git exclusions for venv, caches, and logs
├── templates/
│   └── index.html              # Institutional HTML5 web desk interface
├── static/
│   ├── css/
│   │   └── style.css           # Institutional design system & dark mode
│   └── js/
│       └── app.js              # Vanilla JS frontend logic & theme persistence
└── tests/
    └── test_chatbot.py         # Automated unit & integration test suite
```

---

## 7. Prerequisites & Installation

### Prerequisites
- Python 3.10, 3.11, or 3.12 installed on your system.
- Git (optional, for version control).

### Step-by-Step Setup

1. **Open your terminal / command prompt and navigate to the project directory:**
   ```bash
   cd CodeAlpha_BasicChatbot
   ```

2. **Create a virtual environment:**
   - **Windows:**
     ```powershell
     python -m venv .venv
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     ```

3. **Activate the virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
     > **Tip for PowerShell Script Execution:** If you encounter `PSSecurityException` or `Execution_Policies` restriction, activate for the current session only without altering global system security:
     > ```powershell
     > Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
     > .\.venv\Scripts\Activate.ps1
     > ```
   - **Windows (Command Prompt `cmd`):**
     ```cmd
     .\.venv\Scripts\activate.bat
     ```
   - **macOS / Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 8. How to Run the Applications

### A. Run the Web Help Desk
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```
- Try typing messages in the message composer.
- Click any of the Quick Prompts ("Say hello", "How are you?", etc.).
- Click the **Dark mode** toggle in the top-right navigation.
- Click **Clear conversation** to reset the messages.

### B. Run the Standalone Terminal Chatbot
The core rule engine works independently in your console:
```bash
python chatbot.py
```
**Example Terminal Session:**
```text
============================================================
 Welcome to BlueDesk | Rule-Based Conversational Help Desk
 Type 'bye', 'quit', or 'exit' to end the session.
============================================================
BlueDesk: Hi! Welcome to BlueDesk. How can I help you today?

You: Hello
BlueDesk: Hi! Welcome to BlueDesk. How can I help you today?

You: What is your name?
BlueDesk: I'm BlueDesk, a simple rule-based conversational assistant.

You: How are you?
BlueDesk: I'm doing well, thank you for asking! How are you doing today?

You: goodbye
BlueDesk: Goodbye! It was nice chatting with you. Have a great day ahead!
```

### C. Run the Automated Test Suite
Execute the full test suite using Python's built-in `unittest` runner:
```bash
python -m unittest discover -s tests -v
```

---

## 9. Automated Test Verification Results

All unit and integration tests execute successfully:

```text
test_api_chat_empty_body (tests.test_chatbot.TestFlaskChatEndpoint) ... ok
test_api_chat_method_not_allowed (tests.test_chatbot.TestFlaskChatEndpoint) ... ok
test_api_chat_missing_message_field (tests.test_chatbot.TestFlaskChatEndpoint) ... ok
test_api_chat_non_string_message (tests.test_chatbot.TestFlaskChatEndpoint) ... ok
test_api_chat_success (tests.test_chatbot.TestFlaskChatEndpoint) ... ok
test_home_page_loads (tests.test_chatbot.TestFlaskChatEndpoint) ... ok
test_avoid_false_positive_substrings (tests.test_chatbot.TestChatbotCore) ... ok
test_capabilities_query (tests.test_chatbot.TestChatbotCore) ... ok
test_empty_and_whitespace_input (tests.test_chatbot.TestChatbotCore) ... ok
test_goodbye (tests.test_chatbot.TestChatbotCore) ... ok
test_greeting_capitalization_and_whitespace (tests.test_chatbot.TestChatbotCore) ... ok
test_greeting_punctuation (tests.test_chatbot.TestChatbotCore) ... ok
test_greeting_standard (tests.test_chatbot.TestChatbotCore) ... ok
test_help (tests.test_chatbot.TestChatbotCore) ... ok
test_how_are_you (tests.test_chatbot.TestChatbotCore) ... ok
test_how_are_you_variations (tests.test_chatbot.TestChatbotCore) ... ok
test_name_query (tests.test_chatbot.TestChatbotCore) ... ok
test_thanks (tests.test_chatbot.TestChatbotCore) ... ok
test_unknown_message (tests.test_chatbot.TestChatbotCore) ... ok

----------------------------------------------------------------------
Ran 19 tests in 0.045s

OK
```

---

## 10. Known Limitations

- **Rule-Bound Intelligence:** BlueDesk is strictly a deterministic, rule-based program. It cannot generate novel answers, understand complex grammatical nuances, or answer questions outside its predefined rule set.
- **Local Deployment:** As a Flask web application with a live Python backend, it requires a Python WSGI environment to run. It cannot be hosted as a static site on GitHub Pages without a backend server (e.g. Render, Railway, PythonAnywhere, or a local server).

---

## 11. GitHub Upload Instructions

Use the exact repository name: **`CodeAlpha_BasicChatbot`**

### Option A: Using the Git CLI
1. Open terminal inside `CodeAlpha_BasicChatbot/`:
   ```bash
   git init
   git add .
   git commit -m "Build BlueDesk rule-based chatbot"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPOSITORY_URL
   git push -u origin main
   ```
   *(Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL, such as `https://github.com/your-username/CodeAlpha_BasicChatbot.git`)*.

### Option B: Using GitHub Web UI
1. Create a new repository named `CodeAlpha_BasicChatbot` on GitHub.
2. Select **Upload an existing file**.
3. Drag and drop all files from `CodeAlpha_BasicChatbot/` (ensuring the `templates/`, `static/`, and `tests/` folders are included).
4. Commit changes directly to `main`.

---

## 12. Internship Video Demonstration Checklist

For your CodeAlpha Task 4 LinkedIn / video submission, showcase:
1. **Introduction:** State your name and mention the CodeAlpha Python Programming Internship Task 4.
2. **Terminal Version:** Run `python chatbot.py` and demonstrate a conversation showing greeting, asking how it is, asking its name, and exiting with `bye`.
3. **Web Interface:** Run `python app.py` and open `http://127.0.0.1:5000`.
4. **Theme Toggle:** Demonstrate toggling between Light and Dark modes.
5. **Quick Prompts:** Click the quick prompt chips to demonstrate responsive button actions.
6. **Custom Message:** Type a custom question and show the fallback message for unrecognised queries.
7. **Clear Action:** Click "Clear conversation" to demonstrate state reset.
8. **Automated Tests:** Run `python -m unittest discover -s tests -v` in terminal to show 100% passing tests.

---

## Acknowledgements

Developed as part of the **CodeAlpha Python Programming Internship - Task 4: Basic Chatbot**.
