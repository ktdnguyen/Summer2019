# https://www.nltk.org/
# https://text-processing.com/demo/
# https://www.geeksforgeeks.org/python-lemmatization-with-nltk/


import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


sentence_og="The music in this cafe is very schizophrenic. Musicals are very fun. I really wanted to see school of rock."

####################################################################################
# NLP preprocessing
####################################################################################

# lowercase
print("\napply lowercase............................")
sentence=sentence_og.lower()
print(sentence_og)
print(sentence)


# tokenize
tokens = nltk.word_tokenize(sentence)
print("\ntokenizing............................")
print(tokens)

# tokenize while removing punctuation
tokenizer = RegexpTokenizer(r'\w+')
tokens_nopunct = tokenizer.tokenize(sentence)
print("\nremove punctuation using regular expression............................")
print(sentence)
print(tokens)
print(tokens_nopunct)

# tagging (add part of speech)
tagged = nltk.pos_tag(tokens_nopunct)
print("\ntagging............................")
print(tagged)

# stemming and lemmatizing
# lemmatizing with WordNet
lemmatizer = WordNetLemmatizer()
tokens_lemma=[]
print("\nlemmatizing with WordNet............................")
for token in tokens_nopunct:
	lemmas = lemmatizer.lemmatize(token)
	tokens_lemma.append(lemmas)
	print(token,"\t",lemmas)
	
# recode variants of a word to a canonical version
recode_list={ 	('musical','music'),
				('musicality','music')
			}
			
tokens_lemma2=tokens_lemma.copy()
for item in recode_list:
	for index,token in enumerate(tokens_lemma):
		if token==item[0]:
			tokens_lemma2[index]=item[1]
print("\nhand-lemmatizing using a list I created............................")
print(len(tokens_lemma),tokens_lemma)
print(len(tokens_lemma2),tokens_lemma2)
			
		

# stemming with Porter
if False:
	ps = PorterStemmer() 
	print("\nstemming with Porter............................")
	for token in tokens_nopunct:
		porter = ps.stem(token)
		print(token,"\t",porter)


# remove stopwords
stopWords = set(stopwords.words('english'))
print("\nlist stopwords............................")
print(stopWords)

print("\nremove stopwords from list of tokens............................")
tokens_filter_stopwords = []
for token in tokens_lemma2:
	if token not in list(stopWords)+['really','really really']:
		tokens_filter_stopwords.append(token)
print(tokens)
print(tokens_nopunct)
print(tokens_lemma)
print(tokens_lemma2)
print(tokens_filter_stopwords)


####################################################################################
# NLP analysis - Generation 1 - bag of words, n-grams, frequency, tf-idf
####################################################################################

# bigrams (n-grams where n=2) of cleaned 
bigrams = list(nltk.bigrams(tokens_filter_stopwords))
print("\nbigrams............................")
print(tokens_filter_stopwords)
print(bigrams)

# keyword frequency
freqDict={}
for token in tokens_filter_stopwords:
	if token in freqDict:
		freqDict[token]+=1
	else:
		freqDict[token]=1
print("\ntoken frequency dictionary............................")
print(freqDict)
for key in freqDict:
	print(key,"\t",freqDict[key])

####################################################################################
# NLP analysis - Generation 2 - latent topics, chunked phrases, semantic analysis, collocation, synonyms, antonyms
####################################################################################






