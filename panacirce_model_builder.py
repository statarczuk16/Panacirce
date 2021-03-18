import sys
import os
import csv
import fnmatch
from RedditSubmission import RedditSubmissionClean
from ModelBuilder import ModelBuilder
import panacirce_utilities as panUtils

data_path = sys.path[0]+os.path.sep+"training_data"

for root, dir, files in os.walk(data_path):

        try: 
                data_Y = []
                data_y_num = []
                data_X = [[]]
                redditSubmissions = set()
                redditSubmission = None
                
                for item in fnmatch.filter(files, "*"):
                        file_path = root+os.path.sep+item
                        
                        with open(file_path) as csv_file:
                                csv_reader = csv.reader(csv_file, delimiter=',')
                                line_count = 0
                                for row in csv_reader:
                                        data_Y.append((row[0]))#holds 1 and 0
                                        data_y_num.append(int(row[0]))
                                        data_X.append(row[2:])# row 1 is permalinks, after that is words and counts
                                        line_count+=1
                    
                #print(data_all)   
                #data_Y.pop(0)
                data_X.pop(0)#first space is blank for some reason (bad initialization code?)
                #data_Y.pop(0)
                # separated = panUtils.separate_by_class(data_all)    
                # for label in separated:
                #         print(label)
                #         for row in separated[label]:
                #                 print(row)     
                builder = ModelBuilder()
                builder.fit(data_X[:150],data_Y[:150])
                pred = builder.predict(data_X[:])
                true = data_y_num[:]
                accuracy = sum(1 for i in range(len(pred)) if pred[i] == true[i]) / float(len(pred))
                print("{0:.4f}".format(accuracy)) 
        except PermissionError:
                print("\nPermission Denied opening " + data_file)
        #except:
         #   print("\nOther Error")    

                                
                                        
                                




