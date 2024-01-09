from pickle import dump, load
import pandas as pd

from flair.data import Sentence
from flair.nn import Classifier

df = load(open('/afs/cs.wisc.edu/u/l/e/leng/private/STAT628-M3/preprocess/vegan_review_', 'rb'))

print('load model')
tagger1 = Classifier.load('ner-ontonotes-large') # for product
tagger2 = Classifier.load('chunk') # chunking verb and noun phrases

txt = df['text'].tolist()

print('detect product:')
product = []
c = 0
for t in txt:
    s = Sentence(t)
    tagger1.predict(s)
    
    p = []
    if len(s.get_labels()) > 0:
        for e in s.get_labels():
            if e.value == 'PRODUCT':
                p.append(e.data_point.text.replace('the ', ''))
    
    product.append(p)
    
    c += 1
    if c%500 == 0:
        print(c, end = '\t')
        
with open('/afs/cs.wisc.edu/u/l/e/leng/private/STAT628-M3/product','wb') as filepath: 
    dump(product, filepath)        
        
        
    
print('\ndetect phrase:')    
phrase = []
c = 0
for t in txt:
    s = Sentence(t)
    tagger2.predict(s)
    
    p = []
    if len(s.get_labels()) > 0:
        for e in s.get_labels():
            if e.value == 'NP':
                p.append(e.data_point.text)
    
    phrase.append(p)
    
    c += 1
    if c%500 == 0:
        print(c, end = '\t')

with open('/afs/cs.wisc.edu/u/l/e/leng/private/STAT628-M3/phrase','wb') as filepath: 
    dump(phrase, filepath)
        
print('\nclean phrases')       
f = open(r'food_vocab.txt','r')
food = list(f)
f.close()
food = [f.rstrip('\n') for f in food]

def clean_phrase(p):
    stop_words = ['The ', 'A ', 'An ', 'My ', 'Favorite ', 'Great ', 'Good ', 'Incredible ', 'Amazing ', 'Really ', 'Nice ']
    for s in stop_words:
        p = p.replace(s, '')
        p = p.replace(s.lower(), '')
    return p

food_phrase = []
c = 0
for p_list in phrase:
    p_food = []
    for p in p_list:
        p_ = p.split(' ')
        if len(list( set(p_) & set(food)) ) > 0:
            p_food.append(clean_phrase(p))
    food_phrase.append(p_food)
    
    c += 1
    if c%5000 == 0:
        print(c, end = '\t')
    
with open('/afs/cs.wisc.edu/u/l/e/leng/private/STAT628-M3/food_phrase','wb') as filepath: 
    dump(food_phrase, filepath)