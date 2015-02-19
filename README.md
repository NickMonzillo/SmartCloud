This program is designed as an easy to use way of visualizing word frequencies in text.

Installation:

From the command line run:

```
pip install SmartCloud
```

HOW TO USE:

```
import SmartCloud
```

Instantiate a Cloud object.

```
c = Cloud()
```

Use the method smart_cloud() to create the word cloud of the text, file, or directory. 
max_text_size and min_text_size are the values of the highest and lowest allowable font sizes, respectively.

```
c.smart_cloud(example_dir)
```

From there, display the cloud to the screen using the display() method or create an image file using the save() method.

```
c.display()
```

Added Directory support:
Create a word cloud from a directory of text files by using the directory_cloud() method on a Cloud object.
This creates a cloud with font size based on word frequencies and colors based on how many documents the word occurs in.
The more red a word is, the more documents in the directory it occurs in.

Examples:
From the wikipedia article on the universe (http://en.wikipedia.org/wiki/Universe):

I created the following images using the samrt_cloud method on a directory of samples from the article.

![alt tag](https://github.com/NickMonzillo/SmartCloud/blob/master/SmartCloud/media/exclude_dir.png)

This uses the EXCLUDE_WORDS variable and is how the application displays a directory.

![alt tag](https://github.com/NickMonzillo/SmartCloud/blob/master/SmartCloud/media/exclude_text.png)

This image is a result of using the smart_cloud() method on a .txt file in the directory. 
The method identifies it as a file rather than a directory and creates the visualization accordingly.
