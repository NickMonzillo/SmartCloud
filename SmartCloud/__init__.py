from random import randint,choice
from os import listdir
from os.path import isdir, isfile
from wordplay import tuplecount,separate, eliminate_repeats
import pygame

EXCLUDE_WORDS = True  #excludes words that only occur once in the text.
                       #Reduces clutter in word cloud.

class Cloud(object):
    def __init__(self,width=500,height=500):
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        self.cloud = pygame.Surface((width,height))
        self.used_pos = []
        
    def render_word(self,word,size,color):
        '''Creates a surface that contains a word.'''
        pygame.font.init()
        font = pygame.font.Font(None,size)
        self.rendered_word = font.render(word,0,color)
        self.word_size = font.size(word)
        
    def plot_word(self,position):
        '''Blits a rendered word on to the main display surface'''
        posrectangle = pygame.Rect(position,self.word_size)
        self.used_pos.append(posrectangle)
        self.cloud.blit(self.rendered_word,position)

    def collides(self,position,size):
        '''Returns True if the word collides with another plotted word.'''
        word_rect = pygame.Rect(position,self.word_size)
        if word_rect.collidelistall(self.used_pos) == []:
            return False
        else:
            return True
        
    def expand(self,delta_width,delta_height):
        '''Makes the cloud surface bigger. Maintains all word positions.'''
        temp_surface = pygame.Surface((self.width + delta_width,self.height + delta_height))
        (self.width,self.height) = (self.width + delta_width, self.height + delta_height)
        temp_surface.blit(self.cloud,(0,0))
        self.cloud = temp_surface

    def smart_cloud(self,input,max_text_size=72,min_text_size=12):
        '''Creates a word cloud using the input.
           Input can be a file, directory, or text.'''
        if isdir(input):
            self.directory_cloud(input,max_text_size,min_text_size)
        elif isfile(input):
            text = read_file(input)
            self.text_cloud(text,max_text_size,min_text_size)
        elif isinstance(input, basestring):
            self.text_cloud(input,max_text_size,min_text_size)
        else:
            print 'Input type not supported.'
            print 'Supported types: String, Directory, .txt file'
            
    def directory_cloud(self,directory,max_text_size=72,min_text_size=12,expand_width=50,expand_height=50,max_count=100000):
        '''Creates a word cloud using files from a directory.
        The color of the words correspond to the amount of documents the word occurs in.'''
        worddict = assign_fonts(tuplecount(read_dir(directory)),max_text_size,min_text_size)
        sorted_worddict = list(reversed(sorted(worddict.keys(), key=lambda x: worddict[x])))
        colordict = assign_colors(dir_freq(directory))
        num_words = 0
        for word in sorted_worddict:
            self.render_word(word,worddict[word],colordict[word])
            if self.width < self.word_size[0]:
                #If the word is bigger than the surface, expand the surface.
                self.expand(self.word_size[0]-self.width,0)
            elif self.height < self.word_size[1]:
                self.expand(0,self.word_size[1]-self.height)
            position = [randint(0,self.width-self.word_size[0]),randint(0,self.height-self.word_size[1])]
            #the initial position is determined
            loopcount = 0
            while self.collides(position,self.word_size):
                if loopcount > max_count:
                #If it can't find a position for the word, create a bigger cloud.
                    self.expand(expand_width,expand_height)      
                    loopcount = 0
                position = [randint(0,self.width-self.word_size[0]),randint(0,self.height-self.word_size[1])]
                loopcount += 1
            self.plot_word(position)
            num_words += 1
            
    def text_cloud(self,text,max_text_size=72,min_text_size=12,expand_width=50,expand_height=50,max_count=100000):
        '''Creates a word cloud using plain text.'''
        worddict = assign_fonts(tuplecount(text),max_text_size,min_text_size)
        sorted_worddict = list(reversed(sorted(worddict.keys(), key=lambda x: worddict[x])))
        for word in sorted_worddict:
            self.render_word(word,worddict[word],(randint(0,255),randint(0,255),randint(0,255)))
            if self.width < self.word_size[0]:
                #If the word is bigger than the surface, expand the surface.
                self.expand(self.word_size[0]-self.width,0)
            elif self.height < self.word_size[1]:
                self.expand(0,self.word_size[1]-self.height)
            position = [randint(0,self.width-self.word_size[0]),randint(0,self.height-self.word_size[1])]
            loopcount = 0
            while self.collides(position,self.word_size):
                if loopcount > max_count:
                #If it can't find a position for the word, expand the cloud.
                    self.expand(expand_width,expand_height)
                    loopcount = 0
                position = [randint(0,self.width-self.word_size[0]),randint(0,self.height-self.word_size[1])]
                loopcount += 1
            self.plot_word(position)
            
    def display(self):
        '''Displays the word cloud to the screen.'''
        pygame.init()
        self.display = pygame.display.set_mode((self.width,self.height))
        self.display.blit(self.cloud,(0,0))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

    def save(self,filename):
        '''Saves the cloud to a file.'''
        pygame.image.save(self.cloud,filename)

def read_file(filename):
    '''Reads in a .txt file.'''
    with open(filename,'r') as f:
        content = f.read()
    return content

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

def assign_fonts(counts,maxsize,minsize):
    '''Defines the font size of a word in the cloud.
    Counts is a list of tuples in the form (word,count)'''
    valid_counts = []
    if EXCLUDE_WORDS:
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
