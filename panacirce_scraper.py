from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import panacirce_utilities as panUtils
from RedditSubmission import RedditSubmission
import csv
import re
from praw.models import MoreComments
import praw
from IPython import display
import math
from pprint import pprint
import pandas as pd
import numpy as np
import nltk
import os
import sys
import io
import fnmatch
import matplotlib.pyplot as plt
import seaborn as sns
from psaw import PushshiftAPI
import datetime
from dateutil import relativedelta

sns.set(style='darkgrid', context='talk', palette='Dark2')
#nltk.downloader.download('vader_lexicon')
reddit = praw.Reddit(client_id='OoukjCe93uaWtg',
                     client_secret='ikBFH9CknEeY__tXGFLrxPPNFoc',
                     user_agent='ducksaws')
api = PushshiftAPI(reddit)

hyperlinkRe = re.compile(r'\[.+\]\(.+\)')

print(sys.path[0])

data_path = sys.path[0]+os.path.sep+"scraped_data"
timeCityMin = dict()
timeCityMax = dict()
#minTimeOfInterest = panUtils.get_utc_from_month_year(1,2008)
minTimeOfInterest = panUtils.get_utc_from_month_year(1,2019)
maxTimeOfInterest = panUtils.get_utc_from_month_year(3,2019)
#maxTimeOfInterest = panUtils.get_utc_from_now()
for root, dir, files in os.walk(data_path):
        for item in fnmatch.filter(files, "*scraped*"):
            #print(item)
            temp=item.split("_")
            city=temp[0]
            year=temp[1]
            month=temp[2]
            if(len(month)==1):
                month = "0"+month
            try:
                time = panUtils.get_utc_from_month_year(int(month),int(year))
                if city not in timeCityMin.keys():
                    timeCityMin[city]=time
                    timeCityMax[city]=time
                if timeCityMin[city] > time:
                    timeCityMin[city] = time
                if timeCityMax[city] < time:
                    timeCityMax[city] = time
            except Exception as e:
                print("scraped data filename badly formatted")
                print(e)
for city in timeCityMax:
    print("Data already scraped: ")
    print(city)
    print("     from " + timeCityMin[city].strftime("%m/%Y") + " to " + timeCityMax[city].strftime("%m/%Y"))
            
            



flairs = [[]]
# for sub in reddit.subreddit("LosAngeles").hot(limit=None):
#     if sub.link_flair_text and sub.link_flair_text not in flairs:
#         print(sub.link_flair_text)
#         flairs.append(sub.link_flair_text)
subreddits = [['Chicago','flair:"Ask CHI"'],['Boston','flair:tourism'],['NYC',""],['LosAngeles',""],['Seattle',""]]
for city, flair in subreddits:
    print("Scraping " + city + " " + flair)
    #redditSubmissions = set()
    redditSubmissionsByMonth = dict()
    subs_found = 0
    subs_used = 0
    self_posts = 0
    not_enough_comments = 0
    #if flair == "":
    #    submissions = None #reddit.subreddit(city).hot(limit=None)
    #else:
    #    submissions = None #reddit.subreddit(city).search(flair, limit=None, sort='top',syntax='lucene')

    searchTime = minTimeOfInterest
    while(searchTime <= maxTimeOfInterest):
        #print(searchTime)
        searchTime=searchTime + relativedelta.relativedelta(months=+1)
        if(city in timeCityMin and searchTime>=timeCityMin[city] and city in timeCityMax and searchTime<timeCityMax[city]):
            print("Already have data for " + city + " from " + str(timeCityMin[city]) + " to " + str(timeCityMax[city]))
            searchTime=timeCityMax[city]
            continue
        after = searchTime
        before = searchTime + relativedelta.relativedelta(months=+1, days=-1)
        submissions = list(api.search_submissions(
                                                after=searchTime,
                                                before=before,
                                                subreddit=city,
                                                limit=None
                                                    ))    
        print(searchTime)
        print(str(len(submissions)))
        if(len(submissions)==0):
            continue
        redditSubmissionsByMonth = dict()
        for submission in submissions:
            subs_found+=1
            if(not submission.is_self):
                continue
            self_posts+=1
            #print("comments", end='')
            if(len(submission.comments) < 3):
                #print("0")
                not_enough_comments+=1
                continue
            redditSubmission = RedditSubmission()
            redditSubmission.set_city(city)
            redditSubmission.set_title(panUtils.getKeyWordsFromString(submission.title))
            redditSubmission.set_self_text_full(panUtils.getStringLettersNumbers(submission.selftext))
            redditSubmission.set_self_text(panUtils.getKeyWordsFromString(submission.selftext))
            redditSubmission.set_url(panUtils.sanitizeURL(submission.permalink))
            redditSubmission.set_submit_time(submission.created_utc)
            
            submission.comments.replace_more(limit=30)
            
            for top_level_comment in submission.comments.list():
                #print("|", end='')
                
                if isinstance(top_level_comment, MoreComments):
                    continue
                try: 
                    if(top_level_comment.author.name == "AutoModerator"):
                       # print("A", end='')
                        continue
                except:
                    pass#print("!", end='')
                result = hyperlinkRe.search(top_level_comment.body)
                if(result is None):
                    pass#print("x", end='')
                else:
                    pass#print("H", end='')

                hyperLinks = panUtils.getHyperlinksFromString(
                    top_level_comment.body)
                cleanStr = panUtils.getKeyWordsFromString(
                    top_level_comment.body)
                redditSubmission.add_comment(cleanStr)
                redditSubmission.add_hyperlink(hyperLinks)
                #print("")
            dateCategory = redditSubmission.get_submit_string()
            if(not (dateCategory in redditSubmissionsByMonth.keys())):
                redditSubmissionsByMonth[dateCategory] = set()
            redditSubmissionsByMonth[dateCategory].add(redditSubmission)
            subs_used+=1
            #redditSubmissions.add(redditSubmission)
            # postComments.add(cleanStrSmall)
            # postLinks.add(tuple(hyperLinks))

        for csv_file_by_date in redditSubmissionsByMonth:
            data_path = sys.path[0]+os.path.sep+"scraped_data"
            data_file = data_path+os.path.sep+csv_file_by_date
            os.makedirs(data_path, exist_ok=True)
            try:
                with io.open(data_file, 'w', newline='', encoding="utf-8") as file:
                    writer = csv.writer(file)
                    print("Writing to " + data_file)
                    for sub in redditSubmissionsByMonth[csv_file_by_date]:
                        try:
                            numComments = sub.get_num_comments()

                            writer.writerow(["#Title#"]+[sub.get_title()])
                            writer.writerow(["#RedditDate#"]+[sub.get_submit_time()])
                            writer.writerow(["#Permalink#"]+[sub.get_url()])
                            writer.writerow(["#SelfText#"]+[sub.get_self_text()])
                            writer.writerow(["#SelfTextFull#"]+[sub.get_self_text_full()])
                            for i in range(numComments):
                                # print(sub.get_comment(i))
                                writer.writerow(["#Comment"+str(i)+"#"]+[sub.get_comment(i)])
                                thing1 = sub.get_hyperlinks(i)
                                for j in range(len(sub.get_hyperlinks(i))):
                                    writer.writerow(["#Hyperlink"+str(j)+"#"] + [sub.get_hyperlinks(i)[j]])
                        except UnicodeEncodeError as e:
                            print(e)
                            print("\n\n\n\nBadly sanitized - cannot write to CSV file")
                            print(["#Title#"]+[sub.get_title()])
                            print(["#RedditDate#"]+[sub.get_submit_time()])
                            print(["#Permalink#"]+[sub.get_url()])
                            print(["#SelfText#"]+[sub.get_self_text()])
                            print(["#SelfTextFull#"]+[sub.get_self_text_full()])
                            continue

                                            
            except PermissionError:
                print("\nPermission Denied opening " + data_file)
            
        print("Done")
        print("Found:      " + str(subs_found) + " submissions ")
        print("Used:       " + str(subs_used))
        print("Self Posts: " + str(self_posts))
        print("Not Enough Comments: " + str(not_enough_comments))
        