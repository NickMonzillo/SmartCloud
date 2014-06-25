This program is designed as an easy to use way of visualizing word frequencies in text.

Installation:
From the command line run:
```
//pip install SmartCloud
```

HOW TO USE:
```
//import SmartCloud
```

Create a Cloud object.

Use the method smart_cloud() to create the word cloud of the text, file, or directory. 
max_text_size and min_text_size are the values of the highest and lowest allowable font sizes, respectively.

From there, display the cloud to the screen using the display() method or create an image file using the save() method.

Added Directory support:
Create a word cloud from a directory of text files by using the directory_cloud() method on a Cloud object.
This creates a cloud with font size based on word frequencies and colors based on how many documents the word occurs in.
The more red a word is, the more documents in the directory it occurs in.
