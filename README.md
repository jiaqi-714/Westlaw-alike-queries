# Westlaw-alike-queries
 Westlaw is a popular commercial information retrieval system. You can search for documents by Boolean Terms and Connector queries
For example:
STATUTE ACTION /S FEDERAL /2 TORT /3 CLAIM
    
where STATUTE, ACTION, FEDERAL, TORT, CLAIM are the search terms and space, /S, /2, /3 are the connectors.

In this project, you are going to implement a retrieval system in Python3 called SimplyBoolean, which you have already encountered in the assignment. As a core requirement for this project, you must implement SimplyBoolean using a positional index.

SimplyBoolean is a retrieval system that supports Westlaw alike queries. It supports the following reduced set of connectors:
" ", space, +n, /n, +s, /s, &
    
as well as parentheses. Note that the connectors of your query will be processed in exactly the order above. Further details of these connectors can be found in the Quick Reference Guide of WestLaw available from WebCMS.

Different to Westlaw, SimplyBoolean does not support various forms of search terms, except a normal search term (i.e. single-word, those without " ") and a phrase.

Term matching (including terms in a phrase) in SimplyBoolean follows the below:
Search in SimplyBoolean is case insensitive.
Full stops for abbreviations are ignored. e.g., U.S., US are the same.
Singular/Plural is ignored. e.g., cat, cats, cat's, cats' are all the same.
Tense is ignored. e.g., breaches, breach, breached, breaching are all the same.
A sentence can only end with a full stop, a question mark, or an exclammation mark.
Except the above, all other punctuation should be treated as token dividers.
All (whole) numeric tokens such as years, decimals, integers are ignored. You should not index these tokens and hence should not consider them for proximity queries such as +n. E.g. you should not index '123' (wholly numeric) but should index 'abc123' (partially numeric).

