import chromadb
from chromadb.utils import embedding_functions
import os 
import time 

class ChromaConf:
    
    def __init__(self, db_path="./data/chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection_name = "my_collection_codeGaurd"
        self.emb_func = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name, 
            embedding_function=self.emb_func
        )
        
    
    def check_cache_or_add(self, code_input, response_text=None):
        """
        Checks if the code_input exists in the cache. If it does, returns the cached response. 
        If not, and if response_text is provided, adds the new entry to the cache.
        
        """
        if not code_input:
    
            return None
        # query_text 
        results = self.collection.query(
            query_texts=[code_input],
            n_results=1
        )

        # threshold for similarity, you can adjust this based on your needs
        if results["documents"] and len(results["distances"][0]) > 0:
            if results["distances"][0][0] < 0.6:
                print("🎯 Cache Hit: Found similar logic in DB.")
                return results["documents"][0][0] 

        # if not found in cache and response_text is provided, add to cache
        if response_text:
            print("🆕 Cache Miss: Adding new audit to DB.")
            self.collection.add(
                documents=[response_text], 
                ids=[str(time.time())],
                metadatas=[{"input_snippet": code_input[:100]}]
            )
        
        return None