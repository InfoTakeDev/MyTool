#!/usr/bin/python
# -*- coding: utf-8 -*-
#import argparse
import pathlib
#import uuid
import os
import sys
# import langdetect
from ebooklib import epub


class Txt2Epub:
    def __init__(
        self,
        book_identifier=None,
        book_title=None,
        book_author=None,
        book_language="Big5",
    ):
        self.book_identifier = book_identifier # or str(uuid.uuid4())
        self.book_title = book_title
        self.book_author = book_author
        self.book_language = book_language

    def create_epub(self, title: str, output_file: pathlib.Path = None,
                    chapters: dict = None):
        
        # create new EPUB book
        book = epub.EpubBook()

        # set metadata
        book.set_identifier(self.book_identifier)
        book.set_title(self.book_title)
        book.set_language(self.book_language)
        book.add_author(self.book_author or "Unknown")

        # create chapters
        spine = ["nav"]
        toc = []
        for chapter_title, chapter_content in chapters.items():
            # write chapter title and contents
            chapter = epub.EpubHtml(
                title=chapter_title,
                file_name=f"chap_{chapter_title}.xhtml",
                lang=self.book_language,
            )
            chapter.content = "<h1>{}</h1>{}".format(
                chapter_title,
                "".join("<p>{}</p>".format(chapter_content)),
            )

            # add chapter to the book and TOC
            book.add_item(chapter)
            spine.append(chapter)
            toc.append(chapter)

        # update book spine and TOC
        book.spine = spine
        book.toc = toc

        # add navigation files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # generate new file path if not specified
        
        # create EPUB file
        epub.write_epub(output_file, book)

def toBig5(from_file: str, out_file: str):
    from opencc import OpenCC

    all_text = ""
    with open(from_file, 'r') as f:
        content = f.readlines()
        for line in content:
            all_text += line
    # s2tw
    cc = OpenCC('s2tw')
    all_text = cc.convert(all_text)

    with open(out_file, 'w') as f:
        f.write(all_text)


def genTxt(src_filename: str, foldername: str, title: str):
    
    all_text = ""
    
    with open(f'{src_filename}', 'r') as f:
        content = f.readlines()
        for line in content:
            all_text += line

    if not os.path.exists(foldername):
        os.mkdir(foldername)   

    content = ""
    ch_count = 0
    book_count = 1
    for line in all_text.split('\n'):
        line = line.strip()
        if line.startswith('第') and '章' in line:
            
            ch_count += 1

            if content and ch_count == 51:
                with open(f'{foldername}/{title} {book_count}.txt', 'w') as f:
                    f.write(content + '\n')
                    book_count += 1
                
                ch_count = 0
                content = ""
            
        content += line + '\n'

    if content:
        with open(f'{foldername}/{title} {book_count}.txt', 'w') as f:
            f.write(content + '\n') 


def genToEpub(src_filename: str, output_folder:str ,book_title: str):
    
    content = ""
    chapters = {}
    chapter_content = ""
    old_chapter = ""

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)  
    
    with open(src_filename, 'r') as f:
        content = f.readlines()
        for line in content:
            if line.startswith('第') and '章' in line:
                if old_chapter:
                    chapters[old_chapter] = chapter_content
                old_chapter = line
                chapter_content = ""
            else:
                chapter_content += line

    if old_chapter:
        chapters[old_chapter] = chapter_content
    
    if not os.path.exists(epub_folder):
        os.mkdir(epub_folder) 

    t2e = Txt2Epub(book_title, book_title, "bart")
    t2e.create_epub(book_title, f"{output_folder}/{book_title}.epub", chapters)




if __name__ == '__main__':
    all_text = ""
    
    title = "無敵六皇子"

    original_name = '無敵六皇子.txt'
    big5_name =  '無敵六皇子_big5.txt'
   
    txt_folder = f'{title}_txt'
    epub_folder = f'{title}_epub'

    # toBig5(original_name, big5_name)

    #genTxt(big5_name, txt_folder, title)
    
    # 
    # List all files in the directory
    files = os.listdir(txt_folder)
        # Print the list of files
    for file in files:
        src_file = f"{txt_folder}/{file}"
        output_folder =  "/home/bart/workspace/MyTool/novel2epub/無敵六皇子_epub"
        title = src_file.split('/')[-1].split(".txt")[0]
        genToEpub(src_file, output_folder, title)
