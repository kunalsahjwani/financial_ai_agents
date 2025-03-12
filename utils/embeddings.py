from typing import Union, List, Tuple
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    """Wrapper for sentence-transformers embedding model"""
    
    def __init__(self, model_name='sentence-transformers/paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimensions = 384  # Dimension for the chosen model
    
    def get_embedding_and_usage(self, text: Union[str, List[str]]) -> Tuple[Union[List[List[float]], List[float]], dict]:
        """Get embedding with usage information"""
        if isinstance(text, str):
            embedding = self.model.encode(text)
            embedding_list = embedding.tolist()
            usage = {"prompt_tokens": len(text.split()), "total_tokens": len(text.split())}
            return embedding_list, usage
        else:
            embeddings = self.model.encode(text)
            embedding_list = embeddings.tolist()
            total_tokens = sum(len(t.split()) for t in text)
            usage = {"prompt_tokens": total_tokens, "total_tokens": total_tokens}
            return embedding_list, usage
    
    def get_embedding(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """Get embedding without usage information"""
        if isinstance(text, str):
            return self.model.encode(text).tolist()
        return self.model.encode(text).tolist()