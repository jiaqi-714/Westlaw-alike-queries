import sys
import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
# nltk.download('stem', quiet=True)
from nltk.stem import WordNetLemmatizer
import string

# normal posting = [[posting1], [posting2]] each posting means or 
# this or posting need to be true by themselve and further operation to get possible result
# compound posting = [[[posting1], [posting2]], [[posting1], [posting3]]] each posting means.
# that is posting1 and posting2 should be both true together in operation with further to generate possible result
# qurey will "collapse" into final answer during process

lemmatizer = WordNetLemmatizer()
debug = 0
stack = []

# convert list to lists of list, add two dummy items in start of each list to simulate postinglist

# check if this is list of lists
def checkListsOfList(input_list):
	return any(isinstance(el, list) for el in input_list)

# query AND
# inputs are wordA, wordB, postingList
# [wordPos, sentencePos, docId]
# since AND means both true for later use, so here need to form compound term for every item in wordA and wordB
def intersection(wordA, wordB, postingList):
	answer = []
	AIndex = []
	BIndex = []
	if isinstance(wordA, str):
		if wordA in postingList:
			AIndex = postingList[wordA]
		else:
			AIndex = []
	else:
		AIndex = wordA
	if isinstance(wordB, str):
		if wordB in postingList:
			BIndex = postingList[wordB]
		else:
			AIndex = []
	else:
		BIndex = wordB
	# print(AIndex, BIndex)
	# print(f"compare {AIndex[pointer1][2]} {BIndex[pointer2][2]}")
	for i in AIndex:
		if (checkListsOfList(i)):
			AdocId = i[0][2]
			iIslist = True
		else:
			AdocId = i[2]
			iIslist = False
		for c in BIndex:
			# print(c)
			if (checkListsOfList(c)):
				BdocId = c[0][2]
				cIslist = True
			else:
				BdocId = c[2]
				cIslist = False
			if AdocId == BdocId:
				# since AND means both true for later use, so here need to form compound term for every item in wordA and wordB
				# nest loop to generate all possible pair of word
				if not iIslist and not cIslist:
					temp = [i] + [c]
				elif iIslist and not cIslist:
					temp = i.copy()
					temp.append(c)
					# print("sss")
				elif not iIslist and cIslist:
					temp = c.copy()
					temp.append(i)
					# print("ddd")
				else:
					temp = i + c
					# print("aaa")
				answer.append(temp)
	# print(f"current AND answer = {answer}")
	return answer

# query OR
# inputs are wordA, wordB, postingList, wordA and wordB can be list
# posting list example[[wordPos, sentencePos, docId]]
# since or means either true for later use, so here need to form seperate term for every item in wordA and wordB
def conjunction(wordA, wordB, postingList):
	answer = []
	if isinstance(wordA, str):
		if wordA in postingList:
			pointer1 = 0
			AIndex = postingList[wordA]
		else:
			AIndex = []
	else:
		AIndex = wordA
	if isinstance(wordB, str):
		if wordB in postingList:
			pointer1 = 0
			BIndex = postingList[wordB]
		else:
			BIndex = []
	else:
		BIndex = wordB
	# simply append AIndex + BIndex means OR
	temp = AIndex + BIndex
	answer = temp
	# print(f"after OR operation = {answer}")
	return answer

# help function for positionalIntersection
def posCheck(Aposting, Bposting, k, precede):
	complete = False
	# print(k)
	if precede:
		# print(f"k = {k}, Bposting - Aposting = {(Bposting - Aposting)}")
		if (Bposting - Aposting) <= k and (Bposting - Aposting) > 0:
			complete = True
			return complete
	else:
		if abs(Bposting - Aposting) <= k:
			complete = True
			return complete
	return complete

# posting list example[[wordPos, sentencePos, docId]]
# process +n /n operation
# this is similar to or operation, but for restrict rule that word need to be close in range k
# if there any case in compound term matched, form compound and store them,
def positionalIntersection(wordA, wordB, k, precede, postingList):
	# print(f"precede = {precede}")
	answer = []
	if isinstance(wordA, str):
		if wordA in postingList:
			AIndex = postingList[wordA]
		else:
			AIndex = []
	else:
		AIndex = wordA
	if isinstance(wordB, str):
		if wordB in postingList:
			BIndex = postingList[wordB]
			# print(postingList[wordB])
		else:
			BIndex = []
	else:
		BIndex = wordB
	
	# nest loop to generate all possible pair
	# compound term need to be veritied in all of its posting
	# print(f"AIndex = {AIndex}, BIndex = {BIndex}, wordA = {wordA}, wordB = {wordB}")
	for A in AIndex:
		# print(f"A is {A}")
		if (checkListsOfList(A)):
			AdocId = A[0][2]
			AIslist = True
		else:
			AdocId = A[2]
			AIslist = False
		for B in BIndex:
			# print(f"B is {B}")
			if (checkListsOfList(B)):
				BdocId = B[0][2]
				BIslist = True
			else:
				BdocId = B[2]
				BIslist = False
			# print(AdocId, BdocId)
			if AdocId == BdocId:
				# compound term need to be verity in all of its posting
				if AIslist and BIslist:
					complete = False
					for Aword in A:
						for Bword in B:
							# print(Bword, Aword)
							# print(f"Bword[0] - Aword[0] = {Bword[0] - Aword[0]}")
							complete = posCheck(Aword[0], Bword[0], k, precede)
							if complete: break
						if complete: break
					if complete:
						temp = A + B
						answer.append(temp)
				# compound term need to be verity in all of its posting
				if AIslist and not BIslist:
					
					complete = False
					for Aword in A:
						complete = posCheck(Aword[0], B[0], k, precede)
						# print(f"{B}, {Aword} = {B[0] - Aword[0]}, complete = {complete}")
						if complete: break
					if complete:
						temp = A.copy()
						temp.append(B)
						# print(f"i am heee, temp = {temp}")
						answer.append(temp)
				# compound term need to be verity in all of its posting
				if not AIslist and BIslist:
					complete = False
					for Bword in B:
						# print(Bword, A)
						# print(f"Bword[0] - Aword[0] = {Bword[0] - A[0]}")
						complete = posCheck(A[0], Bword[0], k, precede)
						if complete: break
					if complete:
						temp = B.copy()
						temp.append(A)
						answer.append(temp)
				if not AIslist and not BIslist:
					complete = False
					# print(B, A)
					# print(f"Bword[0] - Aword[0] = {B[0] - A[0]}")
					complete = posCheck(A[0], B[0], k, precede)
					# print(complete)
					if complete:
						temp = [A] + [B]
						answer.append(temp)
						# print(f"A am hhh, A = {A}, B = {B}, temp = {temp}")
						# print(f"now {answer}")
	for i in AIndex:
		del i
	for i in BIndex:
		del i
	# print(f"after /n operation = {answer}")
	return answer

# posting list example[[wordPos, sentencePos, docId]]
def sentenceCheck(Aposting, Bposting, k, precede):
	complete = False
	if (precede):
		if Aposting[0] < Bposting[0] and Aposting[1] == Bposting[1]:
			complete = True
			return complete
	else:
		if Aposting[1] == Bposting[1]:
			complete = True
			return complete
	return complete

# posting list example[[wordPos, sentencePos, docId]]
# process AND operation
# this is similar to OR operation
# but for restrict rule that word need to be in same sentence. 
# if there any case in compound term matched,form compound and store them,
def sentenceIntersection(wordA, wordB, precede, postingList):
	answer = []
	k = 0
	if isinstance(wordA, str):
		if wordA in postingList:
			pointer1 = 0
			AIndex = postingList[wordA]
		else:
			AIndex = []
	else:
		AIndex = wordA
	if isinstance(wordB, str):
		if wordB in postingList:
			pointer1 = 0
			BIndex = postingList[wordB]
		else:
			BIndex = []
	else:
		BIndex = wordB
	
	# nest loop to generate all possible pair
	# compound term need to be veritied in all of its posting
	for A in AIndex:
		if (checkListsOfList(A)):
			AdocId = A[0][2]
			AIslist = True
		else:
			AdocId = A[2]
			AIslist = False
		for B in BIndex:
			if (checkListsOfList(B)):
				BdocId = B[0][2]
				BIslist = True
			else:
				BdocId = B[2]
				BIslist = False
			if AdocId == BdocId:
				# compound term need to be verity in all of its posting
				if AIslist and BIslist:
					complete = False
					for Aword in A:
						for Bword in B:
							# print(Bword, Aword)
							# print(f"Bword[0] - Aword[0] = {Bword[0] - Aword[0]}")
							complete = sentenceCheck(Aword, Bword, k, precede)
							if complete: break
						if complete: break
					if complete:
						temp = A + B
						answer.append(temp)
				# compound term need to be verity in all of its posting
				if AIslist and not BIslist:
					complete = False
					for Aword in A:
						# print(B, Aword)
						# print(f"Bword[0] - Aword[0] = {B[0] - Aword[0]}")
						complete = sentenceCheck(Aword, B, k, precede)
						if complete: break
					if complete:
						temp = A.copy()
						temp.append(B)
						answer.append(temp)
				# compound term need to be verity in all of its posting
				if not AIslist and BIslist:
					complete = False
					for Bword in B:
						# print(Bword, A)
						# print(f"Bword[0] - Aword[0] = {Bword[0] - A[0]}")
						complete = sentenceCheck(A, Bword, k, precede)
						if complete: break
					if complete:
						temp = B.copy()
						temp.append(A)
						answer.append(temp)
				if not AIslist and not BIslist:
					complete = False
					# print(B, A)
					# print(f"Bword[0] - Aword[0] = {B[0] - A[0]}")
					complete = sentenceCheck(A, B, k, precede)
					if complete:
						temp = [A] + [B]
						answer.append(temp)
						# print(f"A am hhh, A = {A}, B = {B}, temp = {temp}")
						# print(f"now {answer}")
	
	for i in AIndex:
		del i
	for i in BIndex:
		del i
	return answer

# process OR operation
# check " ", call responed function to process positional intersection operation
def processOr(query):
	word = 0
	while word < len(query): 
		if (len(query) == 1) or query[word] == []:
			if isinstance(query[word], str):
				query[word] = conjunction(query[word], [], postingList)
			else:
				return query
		if query[word] == " ":
			query[word] = conjunction(query[word - 1], query[word + 1], postingList)
			del query[word + 1]
			del query[word - 1]
		# if do not meet the delimiter keep moving. else stop for a while to check the result just make
		else: word = word + 1
	return query

# check "&", call responed function to process positional intersection operation
def processAnd(query):
	word = 0
	while word < len(query): 
		# print(f"current query is {query}")
		if (len(query) == 1) or query[word] == []:
			return query
		if query[word] == "&":
			query[word] = intersection(query[word - 1], query[word + 1], postingList)
			del query[word + 1]
			del query[word - 1]
		# if do not meet the delimiter keep moving. else stop for a while to check the result just make
		else: word = word + 1
	return query

# def positionalIntersection(wordA, wordB, k, precede, postingList):
# check '+n' '/n', call responed function to process positional intersection operation
def processPosIntersection(query):
	word = 0
	while word < len(query): 
		if (len(query) == 1) or query[word] == []:
			return query
		if query[word][0] == "/" or query[word][0] == "+":
			if (query[word][0]== "/"):
				precede = False
			else:
				precede = True
			if (query[word][1].isdigit()):
				# print(f"i am here fukcing, k = {int(query[word][1:])}, precede = {precede}")
				query[word] = positionalIntersection(query[word - 1], query[word + 1], int(query[word][1:]), precede, postingList)
				del query[word + 1]
				del query[word - 1]
			else: word = word + 1
		# if do not meet the delimiter keep moving. else stop for a while to check the result just make
		else: word = word + 1
	return query

# def positionalIntersection(wordA, wordB, k, precede, postingList):
# check '+s' '/s', call responed function to process sentence intersection operation
def processSentenceIntersection(query):
	word = 0
	while word < len(query): 
		if (len(query) == 1) or query[word] == []:
			return query
		if query[word][0] == "/" or query[word][0] == "+":
			if (query[word][0]== "/"):
				precede = False
			else:
				precede = True
			if (query[word][1] == "s"):
				query[word] = sentenceIntersection(query[word - 1], query[word + 1], precede, postingList)
				del query[word + 1]
				del query[word - 1]
			else: word = word + 1
		# if do not meet the delimiter keep moving. else stop for a while to check the result just make
		else: word = word + 1
	return query

# generate the final output from query be processed
def resultProcess(query):
	result = []
	query = query[0]
	for i in query:
		# if i is bunch of posting list
		if checkListsOfList(i):
			if i[0] == []:
				return result
			CdocID = i[0][2]
			# check if all of posting have same docid
			# for c in i:
			# 	allSame = True
			# 	if c[2] != CdocID:
			# 		allSame = False
			# 		break
			# if allSame:
			if CdocID not in result:
				result.append(CdocID)
		# if i is one posting list
		else:
			if i == []:
				return result
			result.append(i[2])
	# print(result)
	result = list(set(result))
	result.sort()
	return result

# convert input qurey to list can be processed
def queryLemmatize(query):

	if isinstance(query, str):
		query = query.replace("\n", "").split(" ")

	# extract all Parantheses from query
	word = 0
	while word < len(query):
		# print(query[word])
		if query[word].startswith("(") and len(query[word]) != 1:
			query.insert(word, "(")
			query[word + 1] = query[word + 1][1:]
		elif query[word].endswith(")") and len(query[word]) != 1:
			query.insert(word + 1, ")")
			query[word] = query[word][:-1]
		else:
			word = word + 1

	# extract all the quotation mark, insert space if needed
	word = 0
	while word < len(query):
		# print(query[word])
		if query[word].startswith('"') and len(query[word]) != 1:
			if word >= 1:
				# check if there need to insert or(space) before quotation mark
				if query[word - 1][0] != '+' and query[word - 1][0] != '/' \
				and query[word - 1][0] != '&' and query[word - 1][0] != ' '\
				and query[word - 1][0] != '(' and query[word - 1][0] != ')':
					query.insert(word, ' ')
					word = word + 1
			query.insert(word, '"')
			query[word + 1] = query[word + 1][1:]
			# concatnate the phrase by +1
			pointer = word + 1
			while(pointer < len(query)):
				if query[pointer].endswith('"'):
					break
				query.insert(pointer + 1, f'+1')
				pointer = pointer + 2
		elif query[word].endswith('"') and len(query[word]) != 1:
			# if this word is not in the end of query
			if query[word] != query[-1]:
				# check if there need to insert or(space) before quotation mark
				if query[word + 1][0] != '+' and query[word + 1][0] != '/'\
				and query[word + 1][0] != '&' and query[word + 1][0] != ' '\
				and query[word + 1][0] != '(' and query[word + 1][0] != ')':
					query.insert(word + 1, ' ')
			query.insert(word + 1, '"')
			query[word] = query[word][:-1]
		else:
			word = word + 1
	# print(query)
	
	wordTag = nltk.pos_tag(query)
	# print(wordTag)
	for word in range(len(wordTag) - 1, -1, -1):
		# remove 's or s'
		if wordTag[word][1][0] == "N" and query[word].endswith("'s"):
			query[word] = query[word][:-2]
		if wordTag[word][1][0] == "N" and query[word].endswith("s'"):
			query[word] = query[word][:-1]
		# lemmatize verb and noun
		if wordTag[word][1][0] == "N" or wordTag[word][1][0] == "V":
			query[word] = lemmatizer.lemmatize(query[word], pos = (wordTag[word][1][0]).lower())
	# print(query)

	# add space(or) to query if needed
	word = 0
	while word < len(query):
		if word + 1 != len(query):
			if not query[word + 1].startswith("+") and not query[word + 1].startswith("/")\
			and not query[word + 1].startswith("&") and not query[word].startswith("+")\
			and not query[word].startswith("/") and not query[word].startswith("&")\
			and not query[word].startswith("(") and not query[word + 1].startswith(")")\
			and not query[word].startswith('"') and not query[word + 1].startswith('"')\
			and not query[word].startswith(' ') and not query[word + 1].startswith(' '):
				query.insert(word + 1, " ")
				word = word + 2
				continue
			else:
				word = word + 1
		else:
			word = word + 1
	
	# change all quotation mark to Parantheses
	word = 0
	firstQuotation = True
	while word < len(query):
		if query[word] == '"' and firstQuotation:
			query[word] = '('
			firstQuotation = False
		if query[word] == '"' and not firstQuotation:
			query[word] = ')'
			firstQuotation = True
		word = word + 1
	print(f"input query = {query}")
	return query

# process Parantheses
def processParantheses(query):
	# use stack to hold Parantheses
	word = 0
	stack = []
	while word < len(query): 
		if (len(query) == 1):
			return query
		if query[word] == "(":
			stack.append([query[word], word])
		# pop stack when me ), cut the query where in that Parantheses and do operation in there
		if query[word] == ")":
			leftPara = stack.pop()
			rightPara = [query[word], word]
			queryInPara = query[leftPara[1] + 1 : rightPara[1]]
			# print(f"queryInPara = {queryInPara}, leftPara = {leftPara}, rightPara = {rightPara}")
			# delete all of the item in Parantheses since they are processed, keep leftest one for store the result of this Parantheses
			for i in range(leftPara[1], rightPara[1]):
				# print(f"delete {query[leftPara[1] + 1]}")
				del query[leftPara[1] + 1]
			# print(f"query AFTER DELETE = {query}, len = {len(query)}")
			# do the operation in Parantheses, store result in leftest item of that Parantheses
			query[leftPara[1]] = innerParanthesesProcess(queryInPara, postingList)
			# reset the pointer to leftest item for later loop
			word = leftPara[1]
			# print(f"change query[{leftPara[1]}] to {query[leftPara[1]]}")
		# if do not meet the delimiter keep moving. else stop for a while to check the result just make
		word = word + 1
	return query

# generate the result for Parantheses only, used for later process
def innerParanthesesProcess(query, postingList):
	# answer = []
	# print(f"query is {query}")
	query = processParantheses(query)
	# print(f"after Parantheses {query}")
	query = processOr(query)
	# print(f"after OR {query}")
	query = processPosIntersection(query)
	# print(f"after /n {query}")
	query = processSentenceIntersection(query)
	# print(f"after /s {query}")
	query = processAnd(query)
	# print(f"after AND {query}")
	return query[0]

# ['shower', '/', 'continue', 'throughout', '/', 'dog']
# general function of process query
def queryProcess(query, postingList):
	# answer = []
	query = processParantheses(query)
	# print(f"after Parantheses {query}")
	query = processOr(query)
	# print(f"after OR {query}")
	query = processPosIntersection(query)
	# print(f"after /n +n {query}")
	query = processSentenceIntersection(query)
	# print(f"after /s +s{query}")
	query = processAnd(query)
	# print(f"after AND {query}")
	result = resultProcess(query)
	return result


# Opening JSON file
with open(sys.argv[1]) as json_file:
	postingList = json.load(json_file)
	# print(data)
# print(queryLemmatize("dismantling"))
# print(postingList["dismantle"])
try:
	while True:
		query = input().lower()
		#any other work here
		query = queryLemmatize(query)
		# print(f"query is {query}")
		result = queryProcess(query, postingList)
		for i in result:
			print(i)
		# print(f"result = {queryProcess(query, postingList)}")
except EOFError as e:
	print(e)