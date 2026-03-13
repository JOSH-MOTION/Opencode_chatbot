import codetrain as ct
from codetrain import call_llm_simple
from utils.fetch_pages import fetch_all_pages
from utils.index_content import IndexStore


class ReceiveUrlsJob(ct.Job):
    def receive_order(self, manifest):
        return manifest.get("raw_urls", "")

    def prepare_order(self, order_data):
        raw_urls = order_data
        if isinstance(raw_urls, str):
            urls = [u.strip() for u in raw_urls.split(",") if u.strip()]
        else:
            urls = raw_urls

        valid_urls = []
        for url in urls:
            if not (url.startswith("http://") or url.startswith("https://")):
                url = "https://" + url
            valid_urls.append(url)

        return valid_urls

    def ship_order(self, manifest, order_data, result):
        manifest["urls"] = result
        return "default"


class FetchPagesJob(ct.Job):
    def receive_order(self, manifest):
        return manifest.get("urls", [])

    def prepare_order(self, order_data):
        urls = order_data
        all_pages = {}

        for url in urls:
            print(f"Fetching pages from: {url}")
            pages = fetch_all_pages(url, max_pages=20)
            all_pages.update(pages)
            print(f"Fetched {len(pages)} pages from {url}")

        return all_pages

    def ship_order(self, manifest, order_data, result):
        manifest["indexed_content"] = result
        return "default"


class IndexContentJob(ct.Job):
    def receive_order(self, manifest):
        return manifest.get("indexed_content", {})

    def prepare_order(self, order_data):
        indexed_content = order_data
        index_store = IndexStore()
        index_store.build(indexed_content)
        return index_store

    def ship_order(self, manifest, order_data, result):
        manifest["index_store"] = result
        manifest["chat_active"] = True
        return "default"


class ProcessQueryJob(ct.Job):
    def receive_order(self, manifest):
        return manifest.get("user_query", "")

    def prepare_order(self, order_data):
        user_query = order_data
        return user_query.strip()

    def ship_order(self, manifest, order_data, result):
        manifest["clean_query"] = result
        return "default"


class RetrieveContextJob(ct.Job):
    def receive_order(self, manifest):
        return {
            "clean_query": manifest.get("clean_query", ""),
            "index_store": manifest.get("index_store"),
        }

    def prepare_order(self, order_data):
        clean_query = order_data["clean_query"]
        index_store = order_data["index_store"]

        if index_store is None:
            return {"context": "", "results": []}

        results = index_store.retrieve(clean_query, top_k=5)

        context = ""
        for r in results:
            context += f"[Source: {r['url']}]\n{r['content'][:1500]}\n\n"

        return {"context": context, "results": results}

    def ship_order(self, manifest, order_data, result):
        manifest["context"] = result["context"]
        manifest["retrieved_results"] = result["results"]
        return "default"


class GenerateAnswerJob(ct.Job):
    def receive_order(self, manifest):
        return {
            "clean_query": manifest.get("clean_query", ""),
            "context": manifest.get("context", ""),
            "index_store": manifest.get("index_store"),
        }

    def prepare_order(self, order_data):
        clean_query = order_data["clean_query"]
        context = order_data["context"]
        index_store = order_data["index_store"]

        if not context or index_store is None:
            return {
                "in_context": False,
                "response": "I don't have any indexed content to answer your question. Please provide URLs first.",
            }

        prompt = f"""You are a helpful assistant that answers questions strictly based on the provided context.

RULES:
1. ONLY answer questions using information from the provided context
2. If the answer cannot be found in the context, politely say you cannot answer and mention that you can only answer questions about the provided URLs
3. Do NOT make up information
4. Be concise and helpful

Context:
{context}

Question: {clean_query}

Answer:"""

        response = call_llm_simple(prompt)

        response_lower = response.lower()
        no_info_phrases = [
            "cannot answer",
            "don't have",
            "don't know",
            "not in the context",
            "not provided",
            "no information",
        ]

        in_context = not any(phrase in response_lower for phrase in no_info_phrases)

        if not in_context:
            response = """I appreciate your question, but I'm only able to answer questions based on the content I've indexed from the URLs you provided.

Unfortunately, I cannot help with this particular question as it's not related to the content from your provided websites.

This conversation is now closed. If you'd like to ask questions about a different website, please start a new session.

Have a great day! """

        return {"in_context": in_context, "response": response}

    def ship_order(self, manifest, order_data, result):
        manifest["response"] = result["response"]
        manifest["in_context"] = result["in_context"]

        if not result["in_context"]:
            manifest["chat_active"] = False

        return "default"
