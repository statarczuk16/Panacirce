import time
import datetime
from collections import Counter
import math
import string

class ModelBuilder:
    def __init__(self):
        self.num_messages = {"yes":0,"no":0}
        self.log_class_priors = {}
        self.word_counts = {}
        self.vocab = set()

    def get_word_counts(self, words):
            word_counts = {}
            word_ = ""
            count = 0
            for word in words:
                try:
                    count = int(word)
                    try:
                        word_counts[word_] = word_counts.get(word, 0.0) + count
                    except:
                        print("X")
                except:
                    word_ = word
                
            return word_counts

    def fit(self, X,Y):
        self.num_messages = {}
        self.log_class_priors = {}
        self.word_counts = {}
        self.vocab = set()
    
        n = len(X)
        self.num_messages['spam'] = sum(1 for label in Y if label == '1')
        self.num_messages['ham'] = sum(1 for label in Y if label == '0')
        self.log_class_priors['spam'] = math.log(self.num_messages['spam'] / n)
        self.log_class_priors['ham'] = math.log(self.num_messages['ham'] / n)
        self.word_counts['spam'] = {}
        self.word_counts['ham'] = {}
    
        for x, y in zip(X, Y):
            c = 'spam' if y == '1' else 'ham'
            counts = self.get_word_counts(x)
            for word, count in counts.items():
                if word not in self.vocab:
                    self.vocab.add(word)
                if word not in self.word_counts[c]:
                    self.word_counts[c][word] = 0.0
    
                self.word_counts[c][word] += count

    def predict(self, X):
        result = []
        for x in X:
            counts = self.get_word_counts(x)
            spam_score = 0
            ham_score = 0
            for word, _ in counts.items():
                if word not in self.vocab: continue
                
                # add Laplace smoothing
                log_w_given_spam = math.log( (self.word_counts['spam'].get(word, 0.0) + 1) / (self.num_messages['spam'] + len(self.vocab)) )
                log_w_given_ham = math.log( (self.word_counts['ham'].get(word, 0.0) + 1) / (self.num_messages['ham'] + len(self.vocab)) )
    
                spam_score += log_w_given_spam
                ham_score += log_w_given_ham
    
            spam_score += self.log_class_priors['spam']
            ham_score += self.log_class_priors['ham']
    
            if spam_score > ham_score:
                result.append(1)
            else:
                result.append(0)
        return result       
        