# Design Doc: Website Q&A Chatbot

## Requirements

Create a chatbot that:
1. Accepts one or more URLs from the user
2. Indexes all pages from those URLs
3. Answers user queries strictly from the indexed content
4. Politely refuses to answer questions outside the URL context
5. Restricts the user from asking more questions after a refusal

## Hustle Design

### Pattern: RAG (Retrieval Augmented Generation)

### Flow:
```mermaid
flowchart TD
    start[Start] --> receive[Receive URLs]
    receive --> fetch[Fetch Pages]
    fetch --> index[Index Content]
    index --> ready[Ready for Queries]
    ready --> query[User Query]
    query --> retrieve[Retrieve Relevant Context]
    retrieve --> answer[Generate Answer]
    answer --> check{In Context?}
    check -->|Yes| respond[Respond to User]
    check -->|No| refuse[Politely Refuse]
    refuse --> end[End Chat]
```

## Utilities

1. **fetch_pages.py**
   - Uses: `requests`, `BeautifulSoup`
   - Purpose: Fetch all pages from a given URL

2. **index_content.py**
   - Uses: `scikit-learn` (TF-IDF)
   - Purpose: Index and store content for retrieval

3. **retrieve_context.py**
   - Purpose: Find relevant context from indexed content

4. **call_llm.py**
   - Uses: `codetrain.call_llm_simple`
   - Purpose: Generate answers using LLM

## Manifest Design

```python
manifest = {
    "urls": [],              # List of URLs provided by user
    "indexed_content": {},    # URL -> content mapping
    "index": None,           # TF-IDF index
    "user_query": "",        # Current user query
    "context": "",           # Retrieved context
    "response": "",          # LLM response
    "in_context": True,      # Whether query is answerable
    "chat_active": True      # Whether chat is still active
}
```

## Job Design

1. **ReceiveUrlsJob**
   - prep: Read URLs from user input
   - exec: Validate URLs
   - post: Store in manifest["urls"]

2. **FetchPagesJob**
   - prep: Read URLs from manifest
   - exec: Scrape all pages from URLs
   - post: Store content in manifest["indexed_content"]

3. **IndexContentJob**
   - prep: Read indexed_content
   - exec: Build TF-IDF index
   - post: Store index in manifest["index"]

4. **ProcessQueryJob**
   - prep: Read user query
   - exec: Retrieve relevant context
   - post: Store context in manifest["context"]

5. **GenerateAnswerJob**
   - prep: Read context and query
   - exec: Determine if answerable, generate response
   - post: Store response and in_context flag
