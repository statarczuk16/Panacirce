import sys
from gensim.models import LdaModel
import os

in_path = sys.path[0]+os.path.sep+"data_cleaned_new"
model_location = sys.path[0]+os.path.sep+'models'+os.path.sep+"10_topic_lda_model"
lda = LdaModel.load(model_location)

with io.open(in_path, 'r', newline='', encoding="utf-8") as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        line_count = 0