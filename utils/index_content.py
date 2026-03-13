from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def build_index(pages_content):
    """Build TF-IDF index from pages content."""
    if not pages_content:
        return None, None, None

    urls = list(pages_content.keys())
    documents = [pages_content[url] for url in urls]

    vectorizer = TfidfVectorizer(
        stop_words="english", max_features=5000, ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    return vectorizer, tfidf_matrix, urls


def retrieve_top_docs(query, vectorizer, tfidf_matrix, urls, pages_content, top_k=5):
    """Retrieve top k most relevant documents for a query."""
    if vectorizer is None or tfidf_matrix is None:
        return []

    query_vec = vectorizer.transform([query])

    similarities = cosine_similarity(query_vec, tfidf_matrix)[0]

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        if idx < len(similarities) and similarities[idx] > 0.01:
            results.append(
                {
                    "url": urls[idx],
                    "content": pages_content[urls[idx]],
                    "score": float(similarities[idx]),
                }
            )

    return results


class IndexStore:
    def __init__(self):
        self.vectorizer = None
        self.tfidf_matrix = None
        self.urls = []
        self.pages_content = {}

    def build(self, pages_content):
        self.pages_content = pages_content
        self.urls = list(pages_content.keys())
        documents = [pages_content[url] for url in self.urls]

        if not documents:
            return

        self.vectorizer = TfidfVectorizer(
            stop_words="english", max_features=5000, ngram_range=(1, 2)
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)

    def retrieve(self, query, top_k=5):
        if self.vectorizer is None or self.tfidf_matrix is None:
            return []

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        top_indices = np.argsort(similarities)[::-1][:top_k]

        if not len(top_indices) or similarities[top_indices[0]] == 0:
            top_indices = range(len(self.urls))[:top_k]

        results = []
        for idx in top_indices:
            if idx < len(self.urls):
                results.append(
                    {
                        "url": self.urls[idx],
                        "content": self.pages_content[self.urls[idx]],
                        "score": float(similarities[idx])
                        if idx < len(similarities)
                        else 0.0,
                    }
                )

        return results


if __name__ == "__main__":
    test_content = {
        "http://example.com/page1": "Python is a great programming language. It is used for web development.",
        "http://example.com/page2": "JavaScript is another popular language for web development.",
        "http://example.com/page3": "Machine learning is a subset of artificial intelligence.",
    }

    store = IndexStore()
    store.build(test_content)

    results = store.retrieve("programming language")
    for r in results:
        print(f"Score: {r['score']:.3f} - URL: {r['url']}")
