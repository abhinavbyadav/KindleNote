#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 22 09:46:59 2025

@author: abhinav
"""

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
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from PIL import Image
from io import BytesIO


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

def save_pdf(title, image_path, text_file, output_pdf):
    # Read text from the file
    with open(text_file, 'r', encoding='utf-8') as file:
        text_content = file.read()
    
    # Create a new PDF file
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter
    margin = 50
    text_width = width - 2 * margin
    
    
    # Add title with wrapping
    c.setFont("Helvetica-Bold", 14)
    title = title
    title_lines = simpleSplit(title, "Helvetica-Bold", 14, text_width)
    title_y_position = height - 50
    for line in title_lines:
        c.drawCentredString(width / 2, title_y_position, line)
        title_y_position -= 16  # Line spacing
        
    
    # Add date
    c.setFont("Helvetica", 10)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawCentredString(width / 2, height - 90, f"Date: {date_str}")
    
    # Draw image
    img = Image.open(image_path)
    img_width, img_height = img.size
    aspect = img_height / img_width
    new_width = width - 100  # Keeping some margin
    new_height = new_width * aspect
    if new_height > height / 2:
        new_height = height / 2
        new_width = new_height / aspect
    c.drawInlineImage(image_path, 50, height - new_height - 110, new_width, new_height)
    
    # Add text with wrapping
    text_y_position = height / 2 - 110
    c.setFont("Helvetica", 12)
    lines = []
    for line in text_content.split('\n'):
        wrapped_lines = simpleSplit(line, "Helvetica", 12, text_width)
        lines.extend(wrapped_lines)
    
    page_num = 1
    total_pages = (len(lines) // ((height - 100) // 15)) + 1
    
    for i, line in enumerate(lines):
        c.drawString(margin, text_y_position, line)
        text_y_position -= 15  # Line spacing
        
        if text_y_position < 50 or i == len(lines) - 1:
            # Add page number
            c.setFont("Helvetica", 10)
            c.drawString(width / 2 - 30, 30, f"Page {page_num} of {int(total_pages)}")
            c.showPage()
            c.setFont("Helvetica", 12)
            text_y_position = height - 50
            page_num += 1
            
    
    c.save()
    print(f"PDF saved as {output_pdf}")


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
    plt.savefig("img_buffer.png", bbox_inches='tight')
    plt.close()
    plt.show()
    
    # Saving PDF
    save_pdf(SearchBookName, "img_buffer.png",f"{fname}.txt",f"{fname}.pdf")
else:
    print("\n \t \t \t また　ね!")
