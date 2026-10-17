import re
import string

# Define conversational rule responses
RESPONSES = {
    "greeting": "Hi! Welcome to BlueDesk. How can I help you today?",
    "how_are_you": "I'm doing well, thank you for asking! How are you doing today?",
    "goodbye": "Goodbye! It was nice chatting with you. Have a great day ahead!",
    "name": "I'm BlueDesk, a simple rule-based conversational assistant.",
    "capabilities": "I can respond to a variety of common queries using predefined rules. Try saying hello, asking how I am, or asking for help.",
    "thanks": "You're very welcome! Always happy to help.",
    "help": "I'm a rule-based help desk assistant. You can try: 'Hello', 'How are you?', 'What can you do?', 'What is your name?', 'Thanks', or 'Goodbye'.",
    "fallback": "I'm not sure how to respond to that yet. Try asking for help to see what I understand."
}

# Explicit keyword / phrase sets for exact and boundary-aware intent matching
GREETING_TOKENS = {"hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"}
HOW_ARE_YOU_PHRASES = ["how are you", "how are you doing", "how r u", "how do you do", "hows it going", "how's it going"]
GOODBYE_TOKENS = {"bye", "goodbye", "see you", "see ya", "farewell", "cya", "take care", "exit", "quit"}
NAME_PHRASES = ["what is your name", "what's your name", "who are you", "whats your name"]
CAPABILITIES_PHRASES = ["what can you do", "what do you do", "what are your features", "how can you help", "what are your capabilities"]
THANKS_TOKENS = {"thank you", "thanks", "thank you so much", "thx", "many thanks", "appreciate it"}
HELP_TOKENS = {"help", "commands", "options", "menu", "what can i ask", "guide"}


def normalize_text(text: str) -> str:
    """
    Normalizes input text by:
    1. Converting to lowercase.
    2. Stripping leading/trailing whitespace.
    3. Normalizing multiple spaces to single spaces.
    4. Removing non-essential surrounding punctuation.
    """
    if not text:
        return ""
    text = text.strip().lower()
    # Replace common contractions and remove trailing punctuation marks
    text = re.sub(r'\s+', ' ', text)
    # Remove outer punctuation (like "hello!", "how are you?")
    text = text.strip(string.punctuation + " ")
    return text


def tokenize(text: str) -> list[str]:
    """Splits normalized text into distinct clean word tokens."""
    # Remove all punctuation for token extraction
    cleaned = re.sub(r'[' + re.escape(string.punctuation) + r']', ' ', text)
    return [word for word in cleaned.split() if word]


def get_response(message: str) -> str:
    """
    Evaluates the user's message using deterministic rule-based logic
    with if-elif-else statements and token/phrase matching.
    """
    if not message or not isinstance(message, str):
        return RESPONSES["fallback"]

    cleaned = normalize_text(message)
    if not cleaned:
        return RESPONSES["fallback"]

    tokens = tokenize(cleaned)
    token_set = set(tokens)

    # 1. Greetings Rule (e.g., 'hello', 'hi', 'hey', 'good morning')
    if cleaned in GREETING_TOKENS or (token_set & {"hello", "hi", "hey"} and len(tokens) <= 3):
        return RESPONSES["greeting"]

    # 2. How are you Rule
    elif any(phrase in cleaned for phrase in HOW_ARE_YOU_PHRASES):
        return RESPONSES["how_are_you"]

    # 3. Name Rule
    elif any(phrase in cleaned for phrase in NAME_PHRASES):
        return RESPONSES["name"]

    # 4. Capabilities / Features Rule
    elif any(phrase in cleaned for phrase in CAPABILITIES_PHRASES):
        return RESPONSES["capabilities"]

    # 5. Help Rule
    elif cleaned in HELP_TOKENS or "help" in token_set:
        return RESPONSES["help"]

    # 6. Thanks Rule
    elif cleaned in THANKS_TOKENS or (token_set & {"thanks", "thx"} and len(tokens) <= 4):
        return RESPONSES["thanks"]

    # 7. Goodbye Rule (Check token boundary so words like 'lullaby' don't trigger 'bye')
    elif cleaned in GOODBYE_TOKENS or (token_set & {"bye", "goodbye", "farewell"} and len(tokens) <= 4):
        return RESPONSES["goodbye"]

    # 8. Fallback for unrecognised message
    else:
        return RESPONSES["fallback"]


def run_terminal_chat():
    """
    Runs an interactive terminal loop for the chatbot.
    Demonstrates input(), print(), while loop, and termination conditions.
    """
    print("=" * 60)
    print(" Welcome to BlueDesk | Rule-Based Conversational Help Desk")
    print(" Type 'bye', 'quit', or 'exit' to end the session.")
    print("=" * 60)
    print(f"BlueDesk: {RESPONSES['greeting']}")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\nBlueDesk: {RESPONSES['goodbye']}")
            break

        if not user_input:
            continue

        normalized = normalize_text(user_input)
        if normalized in {"bye", "goodbye", "quit", "exit"}:
            print(f"BlueDesk: {RESPONSES['goodbye']}")
            break

        response = get_response(user_input)
        print(f"BlueDesk: {response}")


if __name__ == "__main__":
    run_terminal_chat()
