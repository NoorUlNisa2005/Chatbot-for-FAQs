"""Terminal interface for the FAQ chatbot.  Run:  python main_cli.py"""

from faq_bot import FAQChatbot


def main() -> None:
    bot = FAQChatbot()
    print("=" * 60)
    print("  ShopEasy FAQ Chatbot   (type 'exit' to quit)")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nYou : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot : Goodbye! 👋")
            break

        reply = bot.get_response(user_input)
        print(f"Bot : {reply.answer}")
        if reply.matched_question:
            print(f"      (matched: \"{reply.matched_question}\" | confidence {reply.score:.0%})")
        if reply.suggestions:
            print("      Related questions:")
            for s in reply.suggestions:
                print(f"        - {s}")

        if user_input.lower() in {"exit", "quit", "bye"}:
            break


if __name__ == "__main__":
    main()
