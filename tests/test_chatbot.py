import unittest
import json
import sys
import os

# Add parent directory to sys.path so chatbot and app can be imported from tests/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import chatbot
from app import app


class TestChatbotCore(unittest.TestCase):
    """Automated unit tests for chatbot.py rule-based logic."""

    def test_greeting_standard(self):
        response = chatbot.get_response("hello")
        self.assertIn("Hi! Welcome to BlueDesk", response)

    def test_greeting_capitalization_and_whitespace(self):
        response = chatbot.get_response("   HeLLo   ")
        self.assertIn("Hi! Welcome to BlueDesk", response)

    def test_greeting_punctuation(self):
        response = chatbot.get_response("Hello!")
        self.assertIn("Hi! Welcome to BlueDesk", response)
        response_hi = chatbot.get_response("Hi?!")
        self.assertIn("Hi! Welcome to BlueDesk", response_hi)

    def test_how_are_you(self):
        response = chatbot.get_response("How are you?")
        self.assertIn("doing well", response.lower())

    def test_how_are_you_variations(self):
        self.assertIn("doing well", chatbot.get_response("how are you doing").lower())
        self.assertIn("doing well", chatbot.get_response("hows it going").lower())

    def test_name_query(self):
        response = chatbot.get_response("What is your name?")
        self.assertIn("I'm BlueDesk", response)

    def test_capabilities_query(self):
        response = chatbot.get_response("What can you do?")
        self.assertIn("respond to a variety of common queries", response.lower())

    def test_thanks(self):
        response = chatbot.get_response("Thank you!")
        self.assertIn("welcome", response.lower())
        response_thx = chatbot.get_response("thanks a lot")
        self.assertIn("welcome", response_thx.lower())

    def test_goodbye(self):
        response = chatbot.get_response("Goodbye")
        self.assertIn("Goodbye", response)
        self.assertIn("Goodbye", chatbot.get_response("bye bye"))

    def test_help(self):
        response = chatbot.get_response("help")
        self.assertIn("rule-based help desk assistant", response.lower())

    def test_unknown_message(self):
        response = chatbot.get_response("Can you write a quantum simulation algorithm?")
        self.assertIn("not sure how to respond", response.lower())

    def test_empty_and_whitespace_input(self):
        self.assertEqual(chatbot.get_response(""), chatbot.RESPONSES["fallback"])
        self.assertEqual(chatbot.get_response("    "), chatbot.RESPONSES["fallback"])
        self.assertEqual(chatbot.get_response(None), chatbot.RESPONSES["fallback"])

    def test_avoid_false_positive_substrings(self):
        # "hi" should NOT trigger inside unrelated words like "this", "history", "white", "ship"
        res_this = chatbot.get_response("This is a complicated situation.")
        self.assertEqual(res_this, chatbot.RESPONSES["fallback"])

        res_history = chatbot.get_response("Tell me about world history.")
        self.assertEqual(res_history, chatbot.RESPONSES["fallback"])

        # "bye" should NOT trigger inside "lullaby" or "byte"
        res_byte = chatbot.get_response("A kilobyte is 1024 bytes.")
        self.assertEqual(res_byte, chatbot.RESPONSES["fallback"])


class TestFlaskChatEndpoint(unittest.TestCase):
    """Automated integration tests for Flask /api/chat endpoint."""

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"BlueDesk", response.data)

    def test_api_chat_success(self):
        response = self.client.post(
            "/api/chat",
            data=json.dumps({"message": "Hello"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("Hi! Welcome to BlueDesk", data["reply"])

    def test_api_chat_empty_body(self):
        response = self.client.post("/api/chat", data="", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_api_chat_missing_message_field(self):
        response = self.client.post(
            "/api/chat",
            data=json.dumps({"wrong_field": "Hello"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_api_chat_non_string_message(self):
        response = self.client.post(
            "/api/chat",
            data=json.dumps({"message": 12345}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_api_chat_method_not_allowed(self):
        response = self.client.get("/api/chat")
        self.assertEqual(response.status_code, 405)


if __name__ == "__main__":
    unittest.main()
