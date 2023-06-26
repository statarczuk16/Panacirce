Copyright Notice:
-----------------
© 2021 statarczuk16
The files within this repository are copyrighted by statarczuk16 unless otherwise noted
and may not be redistributed without written permission.

# About

This is a Python program that uses natural language processing and a Latent Dirichlet allocation model to scrape data from a set of Reddit subreddits and then find ten topics that summarize what people on those subreddits talk about. The output is presented as a wordcloud representing the words that make up each topic.

# Install/Use

* Run the python scripts in the following order:
* panacirce_scraper.py - scrapes data from Reddit and outputs to "scraped_data" folder
  * Scrapes data from minTimeOfInterest to maxTimeOfInterest
  * Scrapes data from assigned subreddits (default: subreddits = [['Chicago','flair:"Ask CHI"'],['Boston','flair:tourism'],['NYC',""],['LosAngeles',""],['Seattle',""]])
    * Second argument is a flair filter, though it is not currently used by the scraper
    * Submissions that are not "self" (text-only submissions as opposed to links) and auto-moderators posts are filtered out
    * Hyperlinks are extracted, though not used for anything yet.
* panacirce_cleaner.py - cleans data created by panacirce_cleaner
  * Goes through each .csv file in scraped_data and consolidates each reddit submission into one row of data containing
    * phrased self text submissions
    * permalink to subsmission
    * a column for each most common wordcloud
* panacirce_lda.py - uses LDA to create a word cloud from all cleaned_data and displays

![Output Example](https://github.com/statarczuk16/Panacirce/blob/main/example_topic_cloud_output.png
)

# Future 

* panacirce_model_builder
  * uses cleaned_data which has been manually identified with a topic to build a predictive model
    * To create training data:
      * Set panacirce_cleaner.py :: mode to "1", which will output occurrences for each most common word
      * eg "these are most common words" -> "these 5 are 3 most 2 common 1 words 1"
      * replace left most column with 1 or 0 indicating whether or not the list of words matches the topic you want to detect.
      * eg, if you see "restaurant" or "burger" or whatever, a 1 would indicate this list of words indicates the topic of food
      * place resulting file in "training_data" folder and run panacirce_model_builder.py





