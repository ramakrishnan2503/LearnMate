import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Example text for processing
text = "Natural Language Processing (NLP) is a field of artificial intelligence that focuses on the interaction between computers and humans using natural language."

# Process the text using spaCy
doc = nlp(text)

# Tokenization
print("Tokens:")
for token in doc:
    print(token.text)

# Part-of-speech tagging
print("\nPart-of-speech tagging:")
for token in doc:
    print(f"{token.text}: {token.pos_}")

# Named Entity Recognition (NER)
print("\nNamed Entity Recognition:")
for ent in doc.ents:
    print(f"{ent.text}: {ent.label_}")
