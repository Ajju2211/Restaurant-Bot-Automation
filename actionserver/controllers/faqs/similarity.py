import spacy


class Match:
    """Ref: https://spacy.io/"""
    def __init__(self):
        """Load language model."""
        # spacy.prefer_gpu()
        # self.nlp = spacy.load("en_core_web_sm")
        self.nlp = spacy.load("en_core_web_md")
        # self.nlp = spacy.load("en_core_web_lg") # Switch to large version for performance

    def compare(self, s1, s2):
        p1 = self.nlp(s1)
        p2 = self.nlp(s2)
        if p1.vector_norm>=0.5 and p2.vector_norm>=0.5:
            return p1.similarity(p2)
        # Valid word but no vector_norm is zero
        elif p1.has_vector and p2.has_vector:
            return 0.55
        # Invalid word
        else:
            return 0

if __name__ == "__main__":
    """Example"""
    match = Match()
    s1 = "How much is the cost of one student's school fees?"
    s2 = "How much do I need to pay for my child's school fees?"
    score = match.compare(s1, s2)
    print("Similarity score:", score)
