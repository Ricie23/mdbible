import json
import re
import os
#TODO it is creating an md for the full chapeter and that is not needed. 
os.mkdir("by_verse")

with open("json/ESV.json") as file:
    data = json.load(file)
    books = data["books"]
with open("json/abbrev_map.json") as abbrev_file:
    abbrev = json.load(abbrev_file)

abbrev_map = {}
for entry in abbrev:
    abbrev_map.update(entry)

book_index = 1
for book_title in books:
    file_title = str.replace(book_title, " ", "_")
    file_title = f"{book_index:02d}_{file_title}"
    book = books[f"{book_title}"]
    chapters = [chapter for chapter in book]
    os.mkdir(f"by_verse/{file_title}")
    fulltexts = []
    abbrev = abbrev_map[book_title]
    chap_index = 1

    for chapter in chapters:
        verses = [verse for verse in chapter]
        indeces = [verses.index(verse) for verse in chapter]
        verses = []

        for index in indeces:
            chunks = [i for i in chapter[index]]
            verse = " ".join([chunk[0]
                              for chunk in chunks if not isinstance(chunk[0], list)])
            verse = re.sub(r'\s([?.,;!"](?:\s|$))', r'\1', verse)
            verses.append(verse)

        with open(f"by_verse/{file_title}/Chapter_{chap_index:02d}.md", "w") as file:
            chapter_dir = f"by_verse/{file_title}/Chapter_{chap_index:02d}"
            os.mkdir(chapter_dir)
            verse_index = 1
            for verse in verses:
                verse_filename = f"{abbrev}_{chap_index}_{verse_index}.md"
                verse_path = os.path.join(chapter_dir, verse_filename)
                with open(verse_path, "w") as verse_file:
                    verse_file.write(f"{verse}\n")
                    verse_index += 1
            os.remove(f"by_verse/{file_title}/Chapter_{chap_index:02d}.md")
            chap_index += 1
    book_index += 1

