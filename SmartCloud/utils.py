from os import listdir
from wordplay import eliminate_repeats, read_file
def dir_freq(directory):
    '''Returns a list of tuples of (word,# of directories it occurs)'''
    content = dir_list(directory)
    i = 0
    freqdict = {}
    for filename in content:
        filewords = eliminate_repeats(read_file(directory + '/' + filename))
        for word in filewords:
            if freqdict.has_key(word):
                freqdict[word] += 1
            else:
                freqdict[word] = 1
    tupleize = []
    for key in freqdict.keys():
        wordtuple = (key,freqdict[key])
        tupleize.append(wordtuple)
    return tupleize

def dir_list(directory):
    '''Returns the list of all files in the directory.'''
    try:
        content = listdir(directory)
        return content
    except WindowsError as winErr:
        print("Directory error: " + str((winErr)))

def read_dir(directory):
    '''Returns the text of all files in a directory.'''
    content = dir_list(directory)
    text = ''
    for filename in content:
        text += read_file(directory + '/' + filename)
        text += ' '
    return text

def assign_colors(dir_counts):
    '''Defines the color of a word in the cloud.
    Counts is a list of tuples in the form (word,occurences)
    The more files a word occurs in, the more red it appears in the cloud.'''
    frequencies = map(lambda x: x[1],dir_counts)
    words = map(lambda x: x[0],dir_counts)
    maxoccur = max(frequencies)
    minoccur = min(frequencies)
    colors = map(lambda x: colorize(x,maxoccur,minoccur),frequencies)
    color_dict = dict(zip(words,colors))
    return color_dict

def colorize(occurence,maxoccurence,minoccurence):
    '''A formula for determining colors.'''
    if occurence == maxoccurence:
        color = (255,0,0)
    elif occurence == minoccurence:
        color = (0,0,255)
    else:
        color = (int((float(occurence)/maxoccurence*255)),0,int(float(minoccurence)/occurence*255))
    return color

def assign_fonts(counts,maxsize,minsize,exclude_words):
    '''Defines the font size of a word in the cloud.
    Counts is a list of tuples in the form (word,count)'''
    valid_counts = []
    if exclude_words:
        for i in counts:
            if i[1] != 1:
                valid_counts.append(i)
    else:
        valid_counts = counts
    frequencies = map(lambda x: x[1],valid_counts)
    words = map(lambda x: x[0],valid_counts)
    maxcount = max(frequencies)
    font_sizes = map(lambda x:fontsize(x,maxsize,minsize,maxcount),frequencies)
    size_dict = dict(zip(words, font_sizes))
    return size_dict

def fontsize(count,maxsize,minsize,maxcount):
    '''A formula for determining font sizes.'''
    size = int(maxsize - (maxsize)*((float(maxcount-count)/maxcount)))
    if size < minsize:
        size = minsize
    return size
