import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
def checkListsOfList(input_list):
	return any(isinstance(el, list) for el in input_list)
lemmatizer = WordNetLemmatizer()
# Showers & continued & throughout & in i
# Showers continued & throughout was & in
wordTag = nltk.pos_tag(["  "])
print(wordTag)
# ml[0].extend([[1, 0, 2], [11, 1, 2]])
# print(checkListsOfList([[0, 0, 1], [1, 0, 1]]))
# ml = []
# ml = ml + [[0, 0, 1]] +  [[0, 0, 1], [1, 0, 1], [1, 0, 2]]
# ml.append([2, 3, 5])

# ml = [0, 1, 2, 3, 4, 5, 6]
# join = ml[0:4]
# print(join)
# print(ml)
for i in range(1, 5):
    print(i)
# for i in ml:
#     print(i)
# steph +s right
# steph /s right
# (oliver & is) +3 right
# oliver & is /3 right
# steph & is /3 right
# steph & right /3 is
# steph & right +3 is
# i & Showers continued & throughout in
# ]],


# [[[455, 20, 1], [29, 0, 1]],
#  [[455, 20, 1], [45, 1, 1]],
#  [[455, 20, 1], [55, 2, 1]],
#  [[455, 20, 1], [84, 3, 1]],
#  [[455, 20, 1], [94, 4, 1]],
#  [[455, 20, 1], [105, 4, 1]],
#  [[455, 20, 1], [131, 5, 1]],
#  [[455, 20, 1], [148, 6, 1]],
#  [[455, 20, 1], [158, 6, 1]],
#  [[455, 20, 1], [164, 6, 1]],
#  [[455, 20, 1], [210, 9, 1]],
#  [[455, 20, 1], [220, 9, 1]],
#  [[455, 20, 1], [233, 9, 1]],
#  [[455, 20, 1], [238, 10, 1]],
#  [[455, 20, 1], [273, 11, 1]],
#  [[455, 20, 1], [321, 14, 1]],
#  [[455, 20, 1], [333, 15, 1]],
#  [[455, 20, 1], [356, 16, 1]],
#  [[455, 20, 1], [367, 17, 1]],
#  [[455, 20, 1], [410, 18, 1]],
#  [[455, 20, 1], [432, 19, 1]],
#  [[455, 20, 1], [435, 19, 1]],
#  [[455, 20, 1], [454, 19, 1]],
#  [[455, 20, 1], [456, 20, 1]],
#  [[455, 20, 1], [461, 21, 1]],
#  [[455, 20, 1], [464, 22, 1]],
#  [[455, 20, 1], [467, 23, 1]],
#  [[455, 20, 1], [470, 24, 1]]]


# (steph +1 is) +5 pretty
# (technology & impact) +2 (including & any)

# (continued & (throughout steph))
# ((continued & throughout) steph)

# ((continued & throughout) & (steph & right) girl)

# steph "res ipsa loquitur" play "steph"
# "Computer Terminal also"
# Computer +1 Terminal +2 also
# "Computer Terminal also said it sold" & "the technology for Woodco" "computer generated labels"
# "circumstances involving" +3 "control"
# trade +1 ban +1 against
# Computer +1 Terminal +1 also +1 said +1 it +1 sold
# officials +2 (unilateral /s boycott)
# officials +3 unilateral /s boycott
# officials +2 unilateral /s boycott
# shipowners +30 (unilateral /s boycott)
# officials +3 (boycott /s minority)
# officials +4 (boycott /s minority)
# Cavendish +s billion
# billion +s Cavendish
# billion /s Cavendish

# "major product"
((market company) & profit)