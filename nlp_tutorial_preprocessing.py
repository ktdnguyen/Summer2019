# https://www.nltk.org/
# https://text-processing.com/demo/
# https://www.geeksforgeeks.org/python-lemmatization-with-nltk/

import io
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer 
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

corpus_fname = "corpus_raw.txt"


# corpus_raw: raw document strings
corpus_fin=open(corpus_fname)
corpus_raw=corpus_fin.readlines()

# corpus_clean1: lists of lowercase, lemmatized, filtered keywords
corpus_clean1=[]

for doc in corpus_raw:

	####################################################################################
	# NLP preprocessing
	####################################################################################
	
	print("\nprocessing document............................")
	print(doc)

	# lowercase
	#print("\napply lowercase............................")
	sentence=doc.lower()
	#print(doc)
	#print(sentence)


	# tokenize
	tokens = nltk.word_tokenize(sentence)
	#print("\ntokenizing............................")
	#print(tokens)

	# tokenize while removing punctuation
	tokenizer = RegexpTokenizer(r'\w+')
	tokens_nopunct = tokenizer.tokenize(sentence)
	#print("\nremove punctuation using regular expression............................")
	#print(sentence)
	#print(tokens)
	#print(tokens_nopunct)

	# tagging (add part of speech)
	tagged = nltk.pos_tag(tokens_nopunct)
	#print("\ntagging............................")
	#print(tagged)

	# stemming and lemmatizing
	# lemmatizing with WordNet
	lemmatizer = WordNetLemmatizer()
	tokens_lemma=[]
	#print("\nlemmatizing with WordNet............................")
	for token in tokens_nopunct:
		lemmas = lemmatizer.lemmatize(token)
		tokens_lemma.append(lemmas)
		#print(token,"\t",lemmas)
		
	# recode variants of a word to a canonical version
	recode_list={ 	('musical','music'),
					('musicality','music')
				}
				
	tokens_lemma2=tokens_lemma.copy()
	for item in recode_list:
		for index,token in enumerate(tokens_lemma):
			if token==item[0]:
				tokens_lemma2[index]=item[1]
	#print("\nhand-lemmatizing using a list I created............................")
	#print(len(tokens_lemma),tokens_lemma)
	#print(len(tokens_lemma2),tokens_lemma2)
				
			
	# stemming with Porter
	if False:
		ps = PorterStemmer() 
		#print("\nstemming with Porter............................")
		for token in tokens_nopunct:
			porter = ps.stem(token)
			print(token,"\t",porter)


	# remove stopwords
	stopWords = set(stopwords.words('english'))
	#print("\nlist stopwords............................")
	#print(stopWords)

	#print("\nremove stopwords from list of tokens............................")
	tokens_filter_stopwords = []
	for token in tokens_lemma2:
		if token not in list(stopWords)+['really','really really','much']:
			tokens_filter_stopwords.append(token)
	#print(tokens)
	#print(tokens_nopunct)
	#print(tokens_lemma)
	#print(tokens_lemma2)
	#print(tokens_filter_stopwords)
	
	corpus_clean1.append(tokens_filter_stopwords)
	

print("\nprint tokens for first 10 doc in corpus_clean1............................")
for doc in corpus_clean1[0:10]:
	print(doc)



####################################################################################
# NLP analysis - Generation 1 - bag of words, n-grams, frequency, tf-idf
####################################################################################


# bigram lists (n-grams where n=2) of cleaned tokens for each document
if False:
	corpus_bigrams=[]
	for doc in corpus_clean1:
		bigrams = list(nltk.bigrams(doc))
		#print("\nbigrams............................")
		#print(doc)
		#print(bigrams)
		
		corpus_bigrams.append(bigrams)

	print("\nprint bigrams for each doc in corpus_clean1............................")
	for doc in corpus_bigrams:
		print("\n")
		print(doc)
		

# keyword frequency dictionaries for each document
corpus_freqdict=[]
for doc in corpus_clean1:
	freqDict={}
	for token in doc:
		if token in freqDict:
			freqDict[token]+=1
		else:
			freqDict[token]=1
	#print("\ntoken frequency dictionary............................")
	#print(freqDict)
	corpus_freqdict.append(freqDict)
	
print("\nprint frequency dictionaries for first 10 docs in corpus_clean1............................")
for doc_dict in corpus_freqdict[0:10]:
	print("\n")
	for key in doc_dict:
			print(key,"\t",doc_dict[key])
		
		
# overall keyword frequency dictionary
total_corpus_freqdict={}
for dict in corpus_freqdict:
	for token in dict:
		if token in total_corpus_freqdict:
			total_corpus_freqdict[token]+=dict[token]
		else:
			total_corpus_freqdict[token]=dict[token]
		
#print("\nprint keyword frequency for all doc in total_corpus_freqdict............................")
#for token in total_corpus_freqdict:
#	print(token ,"\t" ,total_corpus_freqdict[token])


#sort total_corpus_freqdict by frequency
sorted_freqdict = sorted(total_corpus_freqdict.items(), key=lambda kv: kv[1], reverse=True)
total_corpus_freqdict = {item[0]:item[1] for item in sorted_freqdict}
print("\nprint keyword frequency for top 100 keywords in total_corpus_freqdict sorted............................")
for token in list(total_corpus_freqdict.keys())[0:100]:
	print(token ,"\t" ,total_corpus_freqdict[token])

####################################################################################
# NLP analysis - Generation 2 - latent topics, chunked phrases, semantic analysis, collocation, synonyms, antonyms
####################################################################################




