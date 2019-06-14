
# ****
# This program expects the text corpus to be present in the same directory, named as "corpus.txt"
#
# It outputs the n-Gram language model in an output file named as "n_GramLM.txt"
#
# This generates a simple Language model  without any back-off strategy
#
# Results in the output file are in logBase10 format as used conventionally in a Language model, while the STDOUT shows probabilities
#
# Enter the value of 'n' when prompted
#
# ****

import re
import collections
import math

def nGram(s,n):
    # This function returns the list of all nGrams in text sentence s given as input. 
    # n represents the ngram length 
    tokens = [token for token in s.split(" ") if token != ""]    
    sequences = [tokens[i:] for i in range(n)]
    ngrams = zip(*sequences)
    return [" ".join(ngram) for ngram in ngrams]   


def calLM(s,k):
    
    if k > 1:
        # make a resursive call for (n-1) gram LM
        lastCounts = calLM(s,k-1)

    # split corpus text on each sentence    
    s = s.split('eos')

    kGrams = []
    # for each sentence in corpus, extract the nGrams using function nGram(s,k) and add to kGrams list
    for i in s:
        if re.search('[a-z]',i):
            # if sentence is not empty, add 'bos' 'eos' symbol to the begin and end of each sentence
            s1 = 'bos '+ i + ' eos'
            temp = nGram(s1,k)
            kGrams += temp

    # 1-gram        
    if(k ==1):
        # get the counts for each 1-gram
        lastCounts = collections.Counter(kGrams)
        
        nCounts= lastCounts
        totCounts = 0

        # get the total word count from the corpus
        for key in nCounts:
            totCounts += nCounts[key]
            
        
        print(k,"-gram  (total count = ", totCounts , ")\n")
        res.write(repr(k) + "-gram\n")
        print ( "Prob.", "\t", "Counts" , "\t", "1-gram")
        print ("---------------------------------------------------------")
        
        # calculate probabilities for each 1-gram and to n_GramLM.txt
        for key in nCounts:
            prob = (nCounts[key] / totCounts)
            
            print ("", round(prob,2), "\t", nCounts[key], "\t", key)
            res.write(repr(math.log10(prob)) +  "\t" + repr(key) + "\n")

    # (n > 1) gram 
    else:
        #  get the counts for each n-gram
        nCounts = (collections.Counter(kGrams)) 

        print("\n\n",k , "-grams\n")
        res.write("\n\n" + repr(k) + "-grams\n")
        print ( "Prob.", "\t", "Count" , "\t", k,  "-gram")
        print ("---------------------------------------------------------")
        
        # calculate n-gram probabilities
        for key in nCounts:
            # get the n-1 gram from n gram using a reverse split
            k1 = key.rsplit(' ', 1)
            k1 = k1[0]

            # n-gram prob = n-gram count / (n-1)-gram count
            prob = (nCounts[key] / lastCounts[k1])
            print ("", round(prob,2), "\t", nCounts[key], "\t", key)
            res.write(repr(math.log10(prob)) +  "\t"  + repr(key) + "\n")
    
    # return the n-gram counts to higher grams (i.e. (n+1)-gram ) for reuse
    return nCounts


# Read the input corpus into s
file = open("corpus.txt", "r") 
s = file.read()
file.close() 

# res holds the cursor into the output LM file
res = open("n_GramLM.txt", "w+")

# preprocessing the corpus, replacing the '.' in each sentence end with 'eos' which represents end of sentence
s = s.lower()
s = re.sub(r'[\.]', ' eos', s)
s= s.replace('\n', '')
s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)

# Take the value of n in n-gram from user 
k = input("Enter the value of n: \n")
k = (int)(k)

nCounts = collections.Counter([])

# call the main LM function, which converts the text corpus to Language Model
# s: corpus text,  k: value of n in n-gram
a = calLM(s,k)

res.close()

