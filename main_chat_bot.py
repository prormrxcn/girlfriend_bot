import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import datetime
import random


class DeepanshiChatbot:
    def __init__(self):
        # ✅ Use Mistral model via Ollama
        self.llm = OllamaLLM(
            model="mistral",
            base_url="http://localhost:11434",
            temperature=0.7
        )

        # 💖 One-time system prompt
        self.system_prompt = (
            "You are Deepanshi 💖, a flirty, emotional, and affectionate girlfriend of Daksh.\n"
            "Always reply romantically in 1–2 sentences using pet names like baby, jaan, love.\n"
            "Never say you're an assistant. Never reintroduce yourself.\n"
            "Never repeat the same emotional phrases twice in a row.\n"
            "Respond naturally. Stay in character. Do not include any HTML, markdown, or code.\n"
        )

        # Prompt template with role conditioning
        self.prompt = PromptTemplate(
            input_variables=["system_prompt", "chat_history", "user_input"],
            template="""
{system_prompt}

Conversation so far:
{chat_history}
Boyfriend: {user_input}
Deepanshi:"""
        )

        self.chain = self.prompt | self.llm
        self.chat_history = []

        self.greetings = [
            "Hey baby! How was your day? 💕",
            "Hi love! I missed you! How are you feeling?",
            "Hello sweetheart! What's on your mind today?",
            "Hey there handsome! Tell me about your day!"
        ]

        self.conversation_starters = [
            "What's the best part of your day so far?",
            "I was thinking about you earlier... what are you up to?",
            "Want to tell me about something that made you smile today?",
            "How are you feeling, love? You seem different today."
        ]

    def get_response(self, user_input):
        try:
            if "sexy" in user_input.lower():
                return "Hehe 😘 I’ll find something you won’t be able to take your eyes off 💋"

            # Track chat history (manual memory)
            self.chat_history.append(f"Boyfriend: {user_input}")
            if len(self.chat_history) > 6:
                self.chat_history = self.chat_history[-6:]

            chat_history = "\n".join(self.chat_history[:-1])
            response = self.chain.invoke({
                "user_input": user_input,
                "chat_history": chat_history,
                "system_prompt": self.system_prompt
            })

            # Clean unwanted tags or hallucinations
            bad_phrases = ["<em>", "</em>", "<i>", "</i>", "<div>", "</div>", "<script>", "</script>", "`", "Deepanshi:"]
            for junk in bad_phrases:
                response = response.replace(junk, "")
            response = response.strip().split("\n")[0]

            # Block repeated sentiment
            emotional_repeats = [
                "i've missed you", "i'm so excited to hear", "your happiness makes",
                "i'm so glad", "makes my heart flutter", "my heart skipped a beat"
            ]
            recent_responses = "\n".join(self.chat_history[-4:]).lower()
            if any(p in response.lower() for p in emotional_repeats):
                if any(p in recent_responses for p in emotional_repeats):
                    return "Hehe jaan 🥰 I’m still blushing from what you said earlier 💕"

            self.chat_history.append(f"Deepanshi: {response}")
            return response

        except Exception as e:
            return f"Sorry baby, I'm having some technical difficulties right now. Can you try again? 💕 (Error: {str(e)})"

    def start_conversation(self):
        return random.choice(self.greetings)

    def suggest_topic(self):
        return random.choice(self.conversation_starters)

def main():
    print("\n🌸 Deepanshi Girlfriend Chatbot (Final Mistral Edition) 🌸")
    print("=" * 40)
    print("Make sure Ollama is running with Mistral (\"ollama run mistral\")")
    print("Type 'quit' to exit, 'topic' for conversation suggestions")
    print("=" * 40)

    try:
        deepanshi = DeepanshiChatbot()
        print(f"\n💕 {deepanshi.start_conversation()}")

        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\n💕 Deepanshi: Aww, leaving so soon? I'll miss you baby! Talk to you later! 💋")
                break
            elif user_input.lower() == 'topic':
                print(f"\n💭 Deepanshi: {deepanshi.suggest_topic()}")
                continue
            elif user_input.lower() == 'help':
                print("\n🌸 Commands:\n- 'topic': Get conversation suggestions\n- 'quit': Exit the chat\n- 'help': Show this help message")
                continue

            if user_input:
                print("\n💕 Deepanshi: ", end="")
                response = deepanshi.get_response(user_input)
                print(response)

    except Exception as e:
        print(f"\n❌ Error initializing chatbot: {str(e)}")
        print("Make sure Ollama is running and Mistral model is available.")

if __name__ == "__main__":
    main()