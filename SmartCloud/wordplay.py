def separate(text):
    '''Takes text and separates it into a list of words'''
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    words = text.split()
    standardwords = []
    for word in words:
        newstr = ''
        for char in word:
            if char in alphabet or char in alphabet.upper():
               newstr += char
        if newstr != '':
            standardwords.append(newstr)
    return map(lambda x: x.lower(),standardwords)

def eliminate_repeats(text):
    '''Returns a list of words that occur in the text. Eliminates stopwords.'''
    bannedwords = ['the','is','are','and','of','to','a','an','for','it','i','in','on','do','in','that','have','be','this','from','these','','its','he','as','you','at','but','his','by','they','we','say','her','she','or','was','will','than','which','their','there']
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    words = text.split()
    standardwords = []
    for word in words:
        newstr = ''
        for char in word:
            if char in alphabet or char in alphabet.upper():
               newstr += char
        if newstr not in standardwords and newstr != '' and newstr not in bannedwords:
            standardwords.append(newstr)
        
    return map(lambda x: x.lower(),standardwords)

def wordcount(text):
    '''Returns the count of the words in a file.'''
    bannedwords = ['the','is','are','and','of','to','a','an','for','it','i','in','on','do','in','that','have','be','this','from','these','','its','he','as','you','at','but','his','by','they','we','say','her','she','or','was','will','than','which','their','there']
    wordcount = {}
    separated = separate(text)
    for word in separated:
        if word not in bannedwords:
            if not wordcount.has_key(word):
                wordcount[word] = 1
            else:
                wordcount[word] += 1
    #for w in sorted(wordcount, key=wordcount.get, reverse=True):
        #print w + ': ' + str(wordcount[w])
    return wordcount

def tuplecount(text):
    '''Changes a dictionary into a list of tuples.'''
    worddict = wordcount(text)
    countlist = []
    for key in worddict.keys():
        countlist.append((key,worddict[key]))
    countlist = list(reversed(sorted(countlist,key = lambda x: x[1])))
    return countlist








    
    
