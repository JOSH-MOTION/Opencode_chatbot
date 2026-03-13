from hustle import create_initial_hustle, create_query_hustle
import warnings

warnings.filterwarnings("ignore")


def index_urls(urls_input):
    """Index URLs and return the manifest with indexed content."""
    manifest = {
        "raw_urls": urls_input,
        "urls": [],
        "indexed_content": {},
        "index_store": None,
        "chat_active": True,
    }

    initial_hustle = create_initial_hustle()
    initial_hustle.run(manifest)

    return manifest


def ask_question(manifest, query):
    """Ask a question using the indexed content."""
    if not manifest.get("chat_active", False):
        return {
            "response": "This conversation is closed. Please start a new session with new URLs.",
            "chat_active": False,
        }

    manifest["user_query"] = query

    query_hustle = create_query_hustle()
    query_hustle.run(manifest)

    return {
        "response": manifest.get("response", ""),
        "chat_active": manifest.get("chat_active", True),
    }


def main():
    print("=" * 60)
    print("Website Q&A Chatbot")
    print("=" * 60)
    print("\nThis chatbot will answer questions based on website content.")
    print("You can provide one or multiple URLs (comma-separated).")
    print("Type 'quit' to exit at any time.\n")

    while True:
        urls_input = input("Enter URL(s): ").strip()

        if urls_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if not urls_input:
            print("Please enter at least one URL.\n")
            continue

        print("\nIndexing website(s)... This may take a while.\n")

        try:
            manifest = index_urls(urls_input)

            if not manifest.get("indexed_content"):
                print(
                    "Failed to fetch any content from the URLs. Please check the URLs and try again.\n"
                )
                continue

            num_pages = len(manifest.get("indexed_content", {}))
            print(f"Successfully indexed {num_pages} page(s)!")
            print("You can now ask questions about the content.\n")
            print("-" * 60)

            while True:
                query = input("You: ").strip()

                if query.lower() in ["quit", "exit", "q", "bye"]:
                    print("Goodbye! Thanks for chatting!")
                    return

                if not query:
                    continue

                result = ask_question(manifest, query)

                print(f"\nBot: {result['response']}\n")

                if not result["chat_active"]:
                    print(
                        "Session ended. To ask about different websites, restart the chatbot."
                    )
                    break

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again with different URLs.\n")


if __name__ == "__main__":
    main()
