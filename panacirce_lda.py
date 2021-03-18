import sys
import os
import csv
import fnmatch
from RedditSubmission import RedditSubmissionClean
#from ModelBuilder import ModelBuilder
import panacirce_utilities as panUtils
from gensim.corpora import Dictionary
from gensim.models import LdaModel
import logging
import re
import matplotlib.pyplot as plt
import wordcloud
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors
import math 
import io
#from pyLDAvis import gensim
from collections import Counter
possible_num_topics = [10]#[4, 6, 8, 10, 12, 16]
config=logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s",
                filemode='w',
                level=logging.DEBUG)
log_path = sys.path[0]+os.path.sep+'logs'
os.makedirs(log_path, exist_ok=True)

for num_topics in possible_num_topics:
        log_location = sys.path[0]+os.path.sep+'logs'+os.path.sep+"log_"+str(num_topics)+'_gensim.log'
        fileh = logging.FileHandler(log_location, 'w')
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        fileh.setFormatter(formatter)
        log = logging.getLogger()
        for hdlr in log.handlers[:]:  # remove all old handlers
                log.removeHandler(hdlr)
        log.addHandler(fileh)      # set the new handler

        print(log_location)
        logging.info("start log")
        
        data_path = sys.path[0]+os.path.sep+"data_cleaned"
        fig_dim = int(math.sqrt(num_topics)+1)
        for root, dir, files in os.walk(data_path):

                try: 
                        data_Y = []
                        data_X = [[]]
                        redditSubmissions = set()
                        redditSubmission = None
                        docs = [[]]
                        corpus = [[]]
                        dct = Dictionary([["initialize","the","dictionary"],["cat","meow"]])
                        for item in fnmatch.filter(files, "*"):
                                file_path = root+os.path.sep+item
                                
                                with io.open(file_path, 'r', newline='', encoding="utf-8") as csv_file:
                                        csv_reader = csv.reader(csv_file, delimiter=',')
                                        line_count = 0
                                        for row in csv_reader:
                                                document=row[2:]
                                                docs.append(document)
                                                dct.add_documents([document])
                                                #data_Y.append(row[0])#holds 1 and 0
                                                #data_X.append(row[2:])# row 1 is permalinks, after that is words and counts
                                                line_count+=1
                        dct.filter_extremes(no_below=10, no_above=0.75)
                        #no words that appear in less than ten documents
                        #no words that appear in more than 75% of documents
                        corpus = [dct.doc2bow(doc) for doc in docs]
                        print('Number of unique tokens: %d' % len(dct))
                        print('Number of documents: %d' % len(corpus))
                        
                        #num_topics = 10#number of topics found by lda
                        chunksize = 2000#number of documents parsed by model in one pass
                        passes = 10#how many iterations to train the model over
                        iterations = 400#similiar 
                        eval_every = 1 

                        # Make a index to word dictionary.
                        temp = dct[0]  # This is only to "load" the dictionary.
                        id2word = dct.id2token

                        lda_model = LdaModel(
                        corpus=corpus,
                        id2word=id2word,
                        chunksize=chunksize,
                        alpha='auto',
                        eta='auto',
                        iterations=iterations,
                        num_topics=num_topics,
                        passes=passes,
                        eval_every=eval_every
        )
                        p = re.compile("(-*\d+\.\d+) per-word .* (\d+\.\d+) perplexity")
                        try:
                                matches = [p.findall(l) for l in open(log_location)]
                                matches = [m for m in matches if len(m) > 0]
                                tuples = [t[0] for t in matches]
                                perplexity = [float(t[1]) for t in tuples]
                                liklihood = [float(t[0]) for t in tuples]
                                iter = list(range(0,len(tuples)*10,10))
                                plt.plot(iter,liklihood,c="black")
                                plt.ylabel("log liklihood")
                                plt.xlabel("iteration")
                                plt.title("Topic Model Convergence")
                                plt.grid()
                                #plt.show()
                                plt.savefig(sys.path[0]+os.path.sep+'logs'+os.path.sep+"_"+str(num_topics)+"_convergence_liklihood.pdf")
                                plt.clf()
                                plt.close()
                        except FileNotFoundError:
                                print("FileNotFound: " + log_location)

                        top_topics = lda_model.top_topics(corpus) #, num_words=20)

                        # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
                        avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
                        print('Average topic coherence: %.4f.' % avg_topic_coherence)

                        from pprint import pprint
                        pprint(top_topics)

                        cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  # more colors: 'mcolors.XKCD_COLORS'

                        cloud = WordCloud(stopwords=panUtils.get_stopwords(),
                                        background_color='white',
                                        width=2500,
                                        height=1800,
                                        max_words=20,
                                        colormap='tab10',
                                        color_func=lambda *args, **kwargs: cols[i],
                                        prefer_horizontal=1.0)

                        topics = lda_model.show_topics(num_topics=num_topics,num_words=20,formatted=False)
                        
                        fig, axes = plt.subplots(fig_dim, fig_dim, figsize=(10,10), sharex=True, sharey=True)

                        for i, ax in enumerate(axes.flatten()):
                                fig.add_subplot(ax)
                                try:
                                        topic_words = dict(topics[i][1])
                                        cloud.generate_from_frequencies(topic_words, max_font_size=300)
                                        plt.gca().imshow(cloud)
                                        plt.gca().set_title('Topic ' + str(i), fontdict=dict(size=16))
                                        plt.gca().axis('off')
                                except (ValueError, IndexError):
                                        print("Bad Index")
                        #vis = gensim.prepare(lda_model, corpus, id2word)
                        #vis
                       
                        plt.subplots_adjust(wspace=0, hspace=0)
                        plt.axis('off')
                        plt.margins(x=0, y=0)
                        plt.tight_layout()
                        plt.show()
                        
                        plt.savefig(log_path+os.path.sep+"_"+str(num_topics)+"_convergence_cloud.png")
                        plt.clf()
                        plt.close()
                        
                        lda_model.save(log_path+os.path.sep+"_"+str(num_topics)+"_lda_model")
                        """ topics = lda_model.show_topics(num_topics=num_topics,num_words=15,formatted=False)
                        data_flat = [w for w_list in data_ready for w in w_list]
                        counter = Counter(data_flat)

                        out = []
                        for i, topic in topics:
                                for word, weight in topic:
                                        out.append([word, i , weight, counter[word]])

                        df = pd.DataFrame(out, columns=['word', 'topic_id', 'importance', 'word_count'])        

                        # Plot Word Count and Weights of Topic Keywords
                        fig, axes = plt.subplots(fig_dim, fig_dim, figsize=(16,10), sharey=True, dpi=160)
                        cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]
                        for i, ax in enumerate(axes.flatten()):
                                ax.bar(x='word', height="word_count", data=df.loc[df.topic_id==i, :], color=cols[i], width=0.5, alpha=0.3, label='Word Count')
                                ax_twin = ax.twinx()
                                ax_twin.bar(x='word', height="importance", data=df.loc[df.topic_id==i, :], color=cols[i], width=0.2, label='Weights')
                                ax.set_ylabel('Word Count', color=cols[i])
                                ax_twin.set_ylim(0, 0.030); ax.set_ylim(0, 3500)
                                ax.set_title('Topic: ' + str(i), color=cols[i], fontsize=16)
                                ax.tick_params(axis='y', left=False)
                                ax.set_xticklabels(df.loc[df.topic_id==i, 'word'], rotation=30, horizontalalignment= 'right')
                                ax.legend(loc='upper left'); ax_twin.legend(loc='upper right')

                        fig.tight_layout(w_pad=2)   
                        plt.savefig(sys.path[0]+os.path.sep+'logs'+os.path.sep+"_"+str(num_topics)+"_convergence_chart.png")
                        plt.clf()
                        plt.close()  """
                except PermissionError:
                        print("\nPermission Denied opening " + data_file)
                #except:
                #   print("\nOther Error")    

                                        
                                             
                                        




