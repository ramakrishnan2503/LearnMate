from sentence_transformers import SentenceTransformer, util
import difflib


def search_transcript_semantic(transcript, keyword):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  

    keyword_embedding = model.encode(keyword, convert_to_tensor=True)
    sentence_embeddings = model.encode([entry[0] for entry in transcript], convert_to_tensor=True)

    
    similarities = util.pytorch_cos_sim(keyword_embedding, sentence_embeddings)[0]

    threshold = 0.7
    matches = [(transcript[i][0], transcript[i][1]) for i in range(len(transcript)) if similarities[i] > threshold]

    return matches


