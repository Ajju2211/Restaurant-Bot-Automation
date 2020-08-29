import pandas as pd
from actionserver.controllers.faqs.similarity import Match
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from actionserver.controllers.faqs.filter import Filter


class FAQ:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.fuzz = fuzz
        # self.match = Match()

    def ask_faq(self, text, threshold=0.7, NLP=True):
        """Returns FAQ answer if similarity score exceeds threshold"""
        max_score = 0
        question_idx = 0
        filteredText = Filter(text).filterWords().lower()
        for i, q in enumerate(self.df['Question']):
            # s = self.fuzz.partial_ratio(text, q)
            # s = self.fuzz.token_set_ratio(text, q)
            filteredFaq  = Filter(q).filterWords().lower()
            if NLP:
                from controllers.faqs.similarity import Match
                match = Match()
                if match.compare(filteredText, filteredFaq)==0:
                    s = 100 + self.fuzz.partial_ratio(filteredText , filteredFaq)
                else:
                    s = match.compare(filteredText, filteredFaq)*100 + self.fuzz.partial_ratio(filteredText , filteredFaq)


            else:
                s = 100 + self.fuzz.partial_ratio(filteredText , filteredFaq)
            if s > max_score:
                max_score = s
                question_idx = i
        print("FAQ score:", max_score)
        thresholdReq = threshold*200
        if max_score > thresholdReq:
            return self.df['Answer'][question_idx]
        else:
            return None


if __name__ == "__main__":
    faq = FAQ("test_faq.csv")
    answer = faq.ask_faq("call USp",NLP=True)
    print(answer)
    answer = faq.ask_faq("call USp",threshold=0.65,NLP=False)
    print(answer)
