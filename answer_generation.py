from crawler import get_all_urls
from llama_index import VectorStoreIndex, SimpleWebPageReader
import openai
import os
from places import find_place_from_name

from llama_index import get_response_synthesizer
from llama_index.query_engine import RetrieverQueryEngine
# import QueryBundle
from llama_index import QueryBundle

# import NodeWithScore
from llama_index.schema import NodeWithScore
from typing import List

# Retrievers
from llama_index.retrievers import (
    BaseRetriever,
    VectorIndexRetriever,
    KeywordTableSimpleRetriever,
)
from llama_index import (
    VectorStoreIndex,
    SimpleKeywordTableIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
)

class CustomRetriever(BaseRetriever):
    """Custom retriever that performs both semantic search and hybrid search."""

    def __init__(
        self,
        vector_retriever: VectorIndexRetriever,
        keyword_retriever: KeywordTableSimpleRetriever,
        mode: str = "AND",
    ) -> None:
        """Init params."""

        self._vector_retriever = vector_retriever
        self._keyword_retriever = keyword_retriever
        if mode not in ("AND", "OR"):
            raise ValueError("Invalid mode.")
        self._mode = mode

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        """Retrieve nodes given query."""

        vector_nodes = self._vector_retriever.retrieve(query_bundle)
        keyword_nodes = self._keyword_retriever.retrieve(query_bundle)

        vector_ids = {n.node.node_id for n in vector_nodes}
        keyword_ids = {n.node.node_id for n in keyword_nodes}

        combined_dict = {n.node.node_id: n for n in vector_nodes}
        combined_dict.update({n.node.node_id: n for n in keyword_nodes})

        if self._mode == "AND":
            retrieve_ids = vector_ids.intersection(keyword_ids)
        else:
            retrieve_ids = vector_ids.union(keyword_ids)

        retrieve_nodes = [combined_dict[rid] for rid in retrieve_ids]
        return retrieve_nodes

def generate_output(input_text):
    place_dict = find_place_from_name(input_text)
    url = place_dict['places'][0]['websiteUri']
    name = place_dict['places'][0]['displayName']['text']
    address = place_dict['places'][0]['formattedAddress']

    default_prompt = "What are the indications for people with disability coming to this place? If none is provided don't make it up."
    information = generate_answer(url, default_prompt)
    answer = f"""{name} ({url})\n{address} \n\n{information}"""
    return answer



def generate_answer(url, prompt):
    openai.api_key = os.environ['OPEN_AI_API_KEY']
    keywords = ['handicap', 'tarifs', 'price', 'pmr', 'acces', 'mobility', 'disable', 'disability', 'pratique', 'practical', 'venu',
                'venir']
    urls = get_all_urls(url, keywords)
    # define custom retriever
    if url not in urls:
        urls.append(url)
    documents = SimpleWebPageReader(html_to_text=True).load_data(
        urls
    )
    # initialize service context (set chunk size)
    service_context = ServiceContext.from_defaults(chunk_size=1024)
    node_parser = service_context.node_parser

    nodes = node_parser.get_nodes_from_documents(documents)
    storage_context = StorageContext.from_defaults()
    storage_context.docstore.add_documents(nodes)
    vector_index = VectorStoreIndex(nodes, storage_context=storage_context)
    keyword_index = SimpleKeywordTableIndex(nodes, storage_context=storage_context)
    vector_retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=2)
    keyword_retriever = KeywordTableSimpleRetriever(index=keyword_index)
    custom_retriever = CustomRetriever(vector_retriever, keyword_retriever)

    # define response synthesizer
    response_synthesizer = get_response_synthesizer()

    # assemble query engine
    custom_query_engine = RetrieverQueryEngine(
        retriever=custom_retriever,
        response_synthesizer=response_synthesizer,
    )

    # vector query engine
    vector_query_engine = RetrieverQueryEngine(
        retriever=vector_retriever,
        response_synthesizer=response_synthesizer,
    )
    # keyword query engine
    keyword_query_engine = RetrieverQueryEngine(
        retriever=keyword_retriever,
        response_synthesizer=response_synthesizer,
    )
    response = vector_query_engine.query(prompt)
    print(response)
    return response