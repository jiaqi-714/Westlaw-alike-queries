# Import Module
import os
import sys
import string
import re
import nltk
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import json

# print(nltk.data.path)

# Folder inputPath
inputPath = sys.argv[1]
outputPath = sys.argv[2]
originalCwd = os.getcwd()
# Change the directory
os.chdir(inputPath)

# Punctuation needed to be remove(without ')
excludePunctuation = string.punctuation.replace("'", "") + "\n"
excludeTable = str.maketrans(excludePunctuation, ' '*len(excludePunctuation))
lemmatizer = WordNetLemmatizer()
postingList = {}
numberDocuments = 0
numberTokens = 0
numberTerms = 0
debug = 0

# Read text File
def read_text_file(file_path, docId):
	with open(file_path, 'r') as f:
		# read file as whole string, convert to lowercase
		content = f.read().lower()
		# spilt whole file to sentences (list of string)
		content = sent_tokenize(content)
		# remove punctuation
		for sentence in range(len(content)):
			# delete '.'
			content[sentence] = content[sentence].replace(".", "")
			# replace Punctuation needed to be remove(without ') to " "
			content[sentence] = content[sentence].translate(excludeTable)

			# split string to word by space
			content[sentence] = content[sentence].split(" ")
			for word in range(len(content[sentence]) - 1, -1, -1):
				# delete number
				if content[sentence][word] == '' or content[sentence][word].isnumeric():
					del content[sentence][word]
				
			# general wordtag to check the plural and verb, use for convert them to stem
			wordTag = nltk.pos_tag(content[sentence])
			# if debug: print(wordTag)
			for word in range(len(wordTag) - 1, -1, -1):
				# remove 's or s'
				if content[sentence][word].endswith("'s"):
					content[sentence][word] = content[sentence][word][:-2]
				if content[sentence][word].endswith("s'"):
					content[sentence][word] = content[sentence][word][:-1]
				# lemmatize verb and noun
				content[sentence][word] = lemmatizer.lemmatize(content[sentence][word], pos = ("v"))
				if wordTag[word][1][0] == "N":
					 content[sentence][word] = lemmatizer.lemmatize(content[sentence][word], pos = ("n"))
 
		# generate postinglist
		wordPos = 0
		sentencePos = 0
		for sentence in content:
			for word in sentence:
				if debug: print(word, wordPos, sentencePos, docId, end = ' ')
				if word in postingList:
					postingList[word].append([wordPos, sentencePos, int(docId)])
				else:
					postingList[word] = [[wordPos, sentencePos, int(docId)]]
				wordPos = wordPos + 1
			if debug: print()
			global numberTokens
			numberTokens = numberTokens + len(sentence)
			sentencePos = sentencePos + 1

# iterate through all file
for file in os.listdir():
	# Check whether file is in text format or not
	# if file.endswith(".txt"):
	file_path = f"{inputPath}/{file}"
	# call read text file function
	if debug: print(file)
	read_text_file(file_path, file)
	numberDocuments = numberDocuments + 1

if debug:
	for key in postingList:
		print(key, '->', postingList[key])

# dump postingList to file
os.chdir(originalCwd)
with open(outputPath, 'w') as convert_file:
		convert_file.write(json.dumps(postingList))
numberTerms = len(postingList)
print(f"Total number of documents: {numberDocuments}")
print(f"Total number of tokens: {numberTokens}")
print(f"Total number of terms: {numberTerms}")
