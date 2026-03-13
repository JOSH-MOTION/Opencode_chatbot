import codetrain as ct
from jobs import (
    ReceiveUrlsJob,
    FetchPagesJob,
    IndexContentJob,
    ProcessQueryJob,
    RetrieveContextJob,
    GenerateAnswerJob,
)


def create_initial_hustle():
    """Create hustle for initial URL indexing."""
    receive_urls = ReceiveUrlsJob()
    fetch_pages = FetchPagesJob()
    index_content = IndexContentJob()

    receive_urls >> fetch_pages >> index_content

    return ct.Hustle(start=receive_urls)


def create_query_hustle():
    """Create hustle for processing user queries."""
    process_query = ProcessQueryJob()
    retrieve_context = RetrieveContextJob()
    generate_answer = GenerateAnswerJob()

    process_query >> retrieve_context >> generate_answer

    return ct.Hustle(start=process_query)
