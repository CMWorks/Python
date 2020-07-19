# Image OCR and Translator
Simple program that uses Tesseract-OCR to extract text from images

## Table of contents
* [Introduction](#Introduction)
* [Technologies](#Technologies)
* [Installation](#Installation)
* [Guide](#Guide)

## Introduction
Simple program that takes a screenshot of a specified location of your screen, extracts the text from the image given the language, and translates all non-English language to English
The program gives you different options on how to preprocess the image. You can use linear or Gaussian thresholds, invert the colors, and rotate the image.
The program also displays the preprocessed image so the user can see what the effects are doing, all in real time.

## Technologies
- Python 3.6
- [Tesseract-OCR 5.0](https://github.com/UB-Mannheim/tesseract/wiki) *Though other versions will work*

## Installation
Download and install Tesseract-ORC from 'https://github.com/UB-Mannheim/tesseract/wiki'
**It is _extremely_ important that you install it into this exact location otherwise the program will not work**
**If it still does not work, make sure that the tesseract.exe is located in 'C:/Program Files/Tesseract-OCR/tesseract.exe' and the tessdata folder is located in 'C:/Program Files/Tesseract-OCR/tessdata/'**
Download and place the python and run.bat file anywhere, does not matter where. Then run the run.bat file to start.

## Guide
***This program works best on multi-monitor systems. Single monitor systems will work, just not as well.***
When you first start the program, three windows will popup. The first is the Python console, the second being the main GUI, and the last being the image output.
You can minimize, *not close as that would close the entire program*, the Python console as there is no need for it.
![Main GUI](http:cmworks.github.io/src/auto_trans_gui.png)
As for the GUI, there are 4 parts to it:
- language detection
- preprocessing
- bounds
- output

### language detection
Depending on what language data you selected to install with Tesseract-OCR, you can select different languages for the program to extract from an image.
For example: by default, eng (English) is select. This means that the program will extract English text from an image.
  If you installed and selected another language, lets say jpn (Japanese), then the program will extract Japanese text from an image, then translates it to English using Google translates.

### preprocessing
The program gives you three options on how you want the image to be preprocessed. You can select the type of threshold, Linear or Gaussian, you can rotate the image if the text is not straight, and you can invert the colors.
You also have the ability to change the variables for the threshold algorithms. Grayscale Cutoff is for linear and Gaussian Constant is for Gaussian.

### bounds
In specify where on your main screen you want the program to use as the image, you can click on the button 'Set Bounds'.
This will start a timer in the 'Out Text' text area. When the timer hits 0, it will record your mouse's location. The first time it will use the mouse's location as the upper left corner of the bounds.
Then, the timer will start again, and this time it will record the bottom right corner of the bounds.
To change the bounds again, just click the button again and do it over.

### output
On the right side of the GUI is a text area with label 'Out Text'. This is where the program will output the text that it extracted from the image.
Next to 'Get Bounds' is another button called 'Get Text'. Clicking this button will get the text from the image and output it to the text area.
Below the text area is a checkbox labeled 'Auto Update', selecting this will auto-grab the text so you don't have to constantly click 'get text'

As for the image output, it shows preprocessed right before it the program extracts the text from it. This is useful since it allows you to try to get the image into an **optimal form of black text on a white background**.
If you are having troubles extracting text. It is usually because the preprocessed image is not black text on white background.
