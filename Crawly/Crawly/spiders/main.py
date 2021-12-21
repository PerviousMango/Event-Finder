import scrapy
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel





class EventsScraper(scrapy.Spider):
    name = "Weaver"
    start_urls = [
    "https://www.eventbrite.com/d/kenya--nairobi/events/"
    ]

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'Crawled_Data.csv'
    }
    #setting our custom feed settings as we are dealing with a csv file
    #

    def parse(self, response, **kwargs):
        for stuff in response.css('div.eds-g-cell-3-12'):
            link = stuff.css('.eds-event-card-content a::attr(href)').get()
            title = stuff.css('.eds-event-card__formatted-name--is-clamped-three::text').get()
            date = stuff.css('.eds-text-color--ui-orange::text').get()
            location = stuff.css('.card-text--truncated__one::text').get()
            

            yield {'Link': link, 'Title': title, 'Date': date, 'Location': location}

        return (response)





df = pd.read_csv("Crawled_Data.csv")
df.drop_duplicates(inplace= True)

df.to_csv("Crawled_Noduplicate_Data.csv", index=True)
df2 = pd.read_csv("Crawled_Noduplicate_Data.csv", header=0, encoding='utf-8', engine='python')
df2.dropna()


def remove_nonAscii(text):
    return ''.join((c for c in str(text) if ord(c) < 128))


def make_lowercase(text):
    text = str(text).lower()
    return text

def remove_stopwords(text):
    text = text.split() 
    stops = set(stopwords.words("english"))
    text = [w for w in text if not w in stops]
    text = " ".join(text)
    return text

def remove_punctuation(text):
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    text = " ".join(text)
    return text

def remove_html(text):
    html_pattern = re.compile("<.*?>")
    return html_pattern.sub(r'', text)





df2['cleaned_title'] = df['Title'].apply(remove_nonAscii)
df2['cleaned_title'] = df2.cleaned_title.apply(func=make_lowercase)
df2['cleaned_title'] = df2.cleaned_title.apply(func=remove_stopwords)
df2['cleaned_title'] = df2.cleaned_title.apply(func=remove_punctuation)
df2['cleaned_title'] = df2.cleaned_title.apply(func=remove_html)
df2.dropna(subset=['cleaned_title'])





tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=1, stop_words='english')
df2['cleaned_title'] = df2['cleaned_title'].fillna('')

tfidf_matrix = tf.fit_transform(df2['cleaned_title'])
print(tfidf_matrix.shape)
print(df2['cleaned_title'])

cosine_sim = sigmoid_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df2.index, index=df2['cleaned_title']).drop_duplicates()
print(cosine_sim)



def recon(title, cosine_sim=cosine_sim): 
    #instead of title we have id, that we automatically fill in when we click on something

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:5]
    event_indices = [i[0] for i in sim_scores]
    print(df2['cleaned_title'].loc[event_indices])


recon('antidote women s circle')
