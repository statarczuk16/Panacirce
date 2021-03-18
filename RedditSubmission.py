import time
import datetime
from collections import Counter


class RedditSubmission:
    def __init__(self):
        self.init=True
        self.index=0
        self.comments = []
        self.title = "No Topic"
        self.self_text = "No Self Text"
        self.self_text_full = "No Full Self Text"
        self.hyperlinks = [[]]
        self.has_links = False
        self.url = "No URL"
        self.this_create_time = datetime.datetime.fromtimestamp(time.time())
        self.submission_create_time = datetime.date(1994,1,21)
        self.city = "NoCity"
        

    def set_city(self,city_in):
        self.city=city_in
    def set_submit_time(self,timestamp):
        self.submission_create_time = datetime.datetime.fromtimestamp(timestamp)
    def get_submit_time(self):
        return self.submission_create_time
    def get_submit_string(self):
        ret = ""
        ret += self.city + "_" + str(self.submission_create_time.year)+"_"+str(self.submission_create_time.month) + "_scraped_" + ".csv"
        return ret
    def set_title(self,title_str):
        self.title=title_str
    def get_title(self):
        return self.title
    def set_self_text(self,self_text_str):
        self.self_text=self_text_str
    def get_self_text(self):
        return self.self_text
    def set_self_text_full(self,self_text_str):
        self.self_text_full=self_text_str
    def get_self_text_full(self):
        return self.self_text_full  
    def set_url(self,url_str):
        self.url = url_str
    def get_url(self):
        return self.url

    def add_comment(self,comment_str):
        self.comments.insert(self.index,comment_str)
        self.index+=1
    def add_hyperlink(self,hyperlink_str):
        self.hyperlinks.insert(self.index-1,hyperlink_str)
        self.has_links=True
    def get_comment(self,index):
        try:
            return self.comments[index]
        except IndexError:
            return "Bad Index"
    def get_hyperlinks(self,index):
        try:
            return self.hyperlinks[index]
        except IndexError:
            return "Bad Index"
    def get_num_comments(self):
        return self.index

class RedditSubmissionClean(RedditSubmission):
    def __init__(self):
        
        self.wordsoup = [""]
        super().__init__()
    def finalize(self):
        self.occurence_count = Counter(self.wordsoup)
    def add_subject_words(self, words):
        self.wordsoup.extend(words)
    def get_subject_words(self):
        return self.wordsoup
    