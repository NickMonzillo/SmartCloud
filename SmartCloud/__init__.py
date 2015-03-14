from random import randint,choice
from os.path import isdir, isfile
from wordplay import tuplecount,separate, read_file
from utils import dir_freq, dir_list, read_dir, assign_colors, colorize, assign_fonts, fontsize
import pygame

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

    def smart_cloud(self,input,max_text_size=72,min_text_size=12,exclude_words = True):
        '''Creates a word cloud using the input.
           Input can be a file, directory, or text.
           Set exclude_words to true if you want to eliminate words that only occur once.'''
        self.exclude_words = exclude_words
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
        worddict = assign_fonts(tuplecount(read_dir(directory)),max_text_size,min_text_size,self.exclude_words)
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
        worddict = assign_fonts(tuplecount(text),max_text_size,min_text_size,self.exclude_words)
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
