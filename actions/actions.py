import os
import yaml
from difflib import get_close_matches
from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from groq import Groq


# ============================================================
# CONFIG
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"

client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# ACTION
# ============================================================

class ActionLlamaExplain(Action):

    def name(self) -> Text:
        return "action_llama_explain"

    def __init__(self) -> None:
        self.kb_path = os.path.join(os.getcwd(), "data", "knowledge.yml")
        self.kb: Dict[str, str] = {}
        self.kb_loaded = False
        self.match_cutoff = 0.75

    # --------------------------------------------------------
    # KB LOADING
    # --------------------------------------------------------

    def load_kb(self) -> None:
        if self.kb_loaded:
            return

        try:
            with open(self.kb_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                if isinstance(data, dict):
                    self.kb = data
        except Exception:
            self.kb = {}

        self.kb_loaded = True

    # --------------------------------------------------------
    # HELPERS
    # --------------------------------------------------------

    def is_greeting(self, text: str) -> bool:
        greetings = ["hi", "hello", "hey", "salam", "bonjour"]
        return text.lower().strip() in greetings

    def is_too_short(self, text: str) -> bool:
        return len(text.strip()) < 4

    def find_in_kb(self, message: str) -> Optional[str]:
        self.load_kb()

        if not self.kb:
            return None

        text = message.lower().strip()
        keys = list(self.kb.keys())
        lowered_keys = [k.lower() for k in keys]

        # 1️⃣ Exact match
        for i, k in enumerate(lowered_keys):
            if text == k:
                return self.kb[keys[i]]

        # 2️⃣ Substring match
        for i, k in enumerate(lowered_keys):
            if k in text or text in k:
                return self.kb[keys[i]]

        # 3️⃣ Fuzzy match (safe)
        matches = get_close_matches(
            text,
            lowered_keys,
            n=1,
            cutoff=self.match_cutoff
        )
        if matches:
            idx = lowered_keys.index(matches[0])
            return self.kb[keys[idx]]

        return None

    # --------------------------------------------------------
    # RUN
    # --------------------------------------------------------

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get("text", "").strip()

        # ❌ Empty input
        if not user_message:
            dispatcher.utter_message(text="Could you repeat that?")
            return []

        # 👋 Greetings
        if self.is_greeting(user_message):
            dispatcher.utter_message(
                text="Hello 👋 I’m Hubi, your assistant for construction and housing services. How can I help you?"
            )
            return []

        # 🛑 Very short messages
        if self.is_too_short(user_message):
            dispatcher.utter_message(
                text="Hi 👋 Please ask a complete question so I can help you better."
            )
            return []

        # ----------------------------------------------------
        # 1️⃣ STATIC KNOWLEDGE BASE
        # ----------------------------------------------------

        kb_answer = self.find_in_kb(user_message)
        if kb_answer:
            dispatcher.utter_message(text=kb_answer)
            return []

        # ----------------------------------------------------
        # 2️⃣ GROQ (LLAMA-3) FALLBACK
        # ----------------------------------------------------

        try:
            completion = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Hubi, a professional assistant specialized in "
                            "construction, urban planning, housing permits, and home maintenance. "
                            "Answer clearly, accurately, and concisely."
                        ),
                    },
                    {
                        "role": "user",
                        "content": user_message,
                    },
                ],
                temperature=0.3,
                max_completion_tokens=512,
            )

            answer = completion.choices[0].message.content.strip()

            if answer:
                dispatcher.utter_message(text=answer)
            else:
                dispatcher.utter_message(
                    text="Sorry, I couldn't find a reliable answer."
                )

        except Exception as e:
            dispatcher.utter_message(
                text="Sorry, I'm having trouble connecting to the assistant right now."
            )

        return []
