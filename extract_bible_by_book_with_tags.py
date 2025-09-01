import json
import re
import os

os.mkdir("by_book_with_tags")
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
    abbrev = abbrev_map[book_title]
    formatted_book_title = str.replace(book_title, " ", "_")
    file_title = f"{book_index:02d}_{formatted_book_title}"
    book = books[f"{book_title}"]
    chapters = [chapter for chapter in book]
    fulltexts = []

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

        fulltexts.append(verses)

    with open(f"by_book_with_tags/{file_title}.md", "w") as file:
        file.write(f"# {book_title}\n\n")
        file.write(f"tags: #ESV #{formatted_book_title} #{abbrev}\n\n")
        chap_index = 1
        for chapter in fulltexts:
            file.write(f"### Chapter {chap_index}\n")
            file.write(f"#{abbrev}_{chap_index}\n\n")
            verse_index = 1
            for verse in chapter:
                file.write(f"##### #{abbrev}_{chap_index}_{verse_index}. \n {verse}\n")
                verse_index += 1
            file.write("\n")
            chap_index += 1
    book_index += 1

