from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
puctuations = ("?", ".", ";", ":", "!")
class Filter:
    def __init__(self,sentence): 
    	self.stop_words = set(stopwords.words('english'))
    	self.word_tokens = word_tokenize(sentence)
    def filterWords(self):
    	filtered_sentence = [w for w in self.word_tokens if not w in self.stop_words]
    	filtered_sentence = ' '.join(map(str, filtered_sentence))
    	return self.removePuctuation(filtered_sentence)
    def removePuctuation(self,sentence):
    	return "".join(ch for ch in sentence if ch not in puctuations)


if __name__ == "__main__":
	fs = Filter("Where can I find fee structure of Semister")
	print(fs.filterWords())





