import sys
import os
import csv
import fnmatch
from RedditSubmission import RedditSubmissionClean
import panacirce_utilities as panUtils
from gensim.models.phrases import Phrases, Phraser
import io


in_path = sys.path[0]+os.path.sep+"scraped_data"
out_path = sys.path[0]+os.path.sep+"data_cleaned"
mode=0# 1= print occurence nums 0 = dont

for root, dir, files in os.walk(in_path):

        redditSubmissions = []
        redditSubmission = None
        documents = ["this is a test sentence", "jump start the phraser"]
        sentence_stream = [doc.split(" ") for doc in documents]
        phrases = Phrases(sentence_stream,min_count=10,threshold=2)
        for item in fnmatch.filter(files, "*"):
                print(item)
                file_path = root+os.path.sep+item
                with io.open(file_path, 'r', newline='', encoding="utf-8") as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        line_count = 0
                        for row in csv_reader:
                                if(row[0] == "#SelfTextFull#"):
                                        rowsplit=row[1].split()
                                        phrases.add_vocab([rowsplit])
                        phraser = Phraser(phrases)
                        csv_file.seek(0)
                        
                        for row in csv_reader:

                                if(row[0] == "#Title#"):
                                        if(redditSubmission is not None):
                                                redditSubmission.finalize()
                                                redditSubmissions.append(redditSubmission)
                                        redditSubmission = RedditSubmissionClean() 
                                        redditSubmission.set_title(row[1])
                                        
                                        topic_words = panUtils.get_topic_words(row[1])
                                        redditSubmission.add_subject_words(topic_words)
                                        #redditSubmission.add_subject_words(topic_words)
                                        #redditSubmission.add_subject_words(topic_words)
                                elif(row[0] == "#SelfText#"):
                                        if(redditSubmission is not None):
                                                redditSubmission.set_self_text(row[1])
                                                
                                                topic_words = panUtils.get_topic_words(row[1])
                                                
                                                redditSubmission.add_subject_words(topic_words)
                                                #redditSubmission.add_subject_words(topic_words)
                                elif(row[0] == "#SelfTextFull#"):
                                        if(redditSubmission is not None):
                                                redditSubmission.set_self_text_full(row[1])
                                elif("#Comment" in row[0]):
                                        if(redditSubmission is not None):
                                                redditSubmission.add_comment(row[1])
                                                rowsplit = row[1].split()
                                                row_phrases = phraser[rowsplit]
                                                redditSubmission.add_subject_words(row_phrases)
                                                topic_words = panUtils.get_topic_words(row[1])
                                                
                                                #redditSubmission.add_subject_words(topic_words)
                                elif("#Permalink" in row[0]):
                                        if(redditSubmission is not None):
                                                redditSubmission.set_url(row[1])                
                                elif("#Hyperlink" in row[0]):
                                        if(redditSubmission is not None):
                                                redditSubmission.add_hyperlink(row[1])
        
        print("done")

        try:
                data_path = out_path
                data_file = data_path+os.path.sep+"test_data_"+str(panUtils.get_date_from_now())+".csv"
                os.makedirs(data_path, exist_ok=True)
                with io.open(data_file, 'w', newline='', encoding="utf-8") as file:
                        writer = csv.writer(file)
                        index = 0
                        for sub in redditSubmissions:
                                count = sub.occurence_count
                                most_common_words=[]
                                #most_common_words = [word for word,cnt in count.most_common(20) if word != ""]
                                
                                for word,cnt in count.most_common():
                                        if(word==""):
                                                continue
                                        most_common_words.append(word)
                                        if mode == 1:
                                                most_common_words.append(cnt)
                                #most_common_words = [word,str(cnt) for word,cnt in count.most_common(20) if word != ""]
                                writer.writerow([sub.get_self_text_full()]+[sub.get_url()]+most_common_words)#+[""]+[sub.get_url()])
                        print("\n rows printed: " + str(len(redditSubmissions)))
                    
                                    
        except PermissionError:
                print("\nPermission Denied opening " + data_file)
          

                                
                                        
                                




