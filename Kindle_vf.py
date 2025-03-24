#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 19:39:20 2024

@author: abhinav
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap
from datetime import datetime

class Book:
    def __init__(self, title, date_of_last_highlight):
        self.title = title
        self.num_of_highlights = 0
        self.date_of_last_highlight = date_of_last_highlight
        self.highlights = []

# Function to update number of highlights by title
def update_entry_by_title(title, new_date, note):
    for book in Books:
        if book.title == title:
            book.num_of_highlights += 1
            book.highlights.append([str(book.num_of_highlights), ". ", note])
            book.date_of_last_highlight=new_date
            break

print("\n\n\nWelcome to the Kindle Note Formatting utility!\n\n");


try:
  load ("Saved_var");
except:
  print("Parsing the Kindle \"My Clippings.txt\" file. Please be patient!")
  file = open("My Clippings.txt", "r")
  raw_content = file.read()
  content= raw_content.split("\n")
  df = pd.DataFrame(content)
  #print(len(df))
  df.dropna(inplace=True)
  #print(len(df))
  df.columns = ["content"]
  #df.rename(columns = {'0':'content'}, inplace = True) 


BookTitles = {};
Books=[];

for i in range(0,len(content)):
    if i%5 ==0: 
        try:
            if content[i][0]=='\ufeff':
                if not(content[i][1:] in BookTitles):
                    BookTitles[content[i][1:]]=1;
                    date=[content[i+1].split(" ")[-4],"-",content[i+1].split(" ")[-3],"-",content[i+1].split(" ")[-2]]
                    date=''.join(date)
                    Books.append(Book(content[i][1:],date))
                    update_entry_by_title(content[i][1:], date, content[i+3])
                else:
                    BookTitles[content[i][1:]]+=1;
                    date=[content[i+1].split(" ")[-4],"-",content[i+1].split(" ")[-3],"-",content[i+1].split(" ")[-2]]
                    date=''.join(date)
                    update_entry_by_title(content[i][1:], date, content[i+3])
                    
            else:
                if not (content[i] in BookTitles):
                    BookTitles[content[i]]=1;
                    date=[content[i+1].split(" ")[-4],"-",content[i+1].split(" ")[-3],"-",content[i+1].split(" ")[-2]]
                    date=''.join(date)
                    Books.append(Book(content[i],date))
                    update_entry_by_title(content[i], date, content[i+3])
                    
                else:
                    BookTitles[content[i]]+=1;
                    date=[content[i+1].split(" ")[-4],"-",content[i+1].split(" ")[-3],"-",content[i+1].split(" ")[-2]]
                    date=''.join(date)
                    update_entry_by_title(content[i], date, content[i+3])
                    
        except:
            {}



sorted_object = sorted(Books, key=lambda x: datetime.strptime(x.date_of_last_highlight,'%d-%B-%Y'), reverse=True)

BookTitles=dict(sorted(BookTitles.items(), key=lambda item: item[1],reverse=True))

print(f"\nTotal number of books that have atleast one highlights: {len(sorted_object)}\n")
print("Top 30 books in order of the last date of highlighting are")
for i in range(0,min(len(sorted_object),31)):
    titles = [b.title for b in sorted_object]
    num_high = [b.num_of_highlights for b in sorted_object]
    dates = [b.date_of_last_highlight for b in sorted_object]
    print(f"{i+1}. {titles[i]} [{num_high[i]}] [{dates[i]}]")

BookTitleNum = int(input('\n Please enter the serial number of the book for which notes are required.'
                     '\n (Enter 0 if want to exit the utility) \t\t\t\t\t\t\t\t: '))


if BookTitleNum:
    SearchBookName=sorted_object[BookTitleNum-1].title
    
    Notes=sorted_object[BookTitleNum-1].highlights;
    print(f"\nName of the book: {SearchBookName}")
    print(f"\nNumber of highlights: {len(Notes)}\n")
    
    fname=SearchBookName.replace(" ", "_")
    
    f = open(f"{fname}.txt", "w")
    for i in Notes:
        f.write("".join(i)+"\n")
    f.close()
    print(f"Saved file as {fname}.txt in the current directory.")
    
    labels = ( '\n'.join(wrap(l, 20)) for l in list(BookTitles.keys())[0:5] )
    
    # width = 1.0     # gives histogram aspect to the bar diagram
    # plt.barh(list(BookTitles.keys())[0:5],list(BookTitles.values())[0:5])
    # #plt.ylabel(labels)
    # #plt.xticks(rotation=90)
    # plt.show()
    
    plt.figure(figsize=(10, 5))
    plt.bar(list(BookTitles.keys())[0:5],list(BookTitles.values())[0:5], color='green', align='center',width=0.3)
    plt.title('Top 5 books with highlighted text')
    plt.xticks(list(BookTitles.keys())[0:5],labels, rotation=0)
    plt.legend()
    plt.show()
else:
    print("\n \t \t \t また　ね!")