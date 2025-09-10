import json
import re
import os

# Get directory name and check if it exists
dir_name = input("Please enter Directory name: (e.g. 'KJV_by_book_with_tags') ")
if os.path.exists(dir_name):
    print(f"Directory '{dir_name}' already exists!")
    overwrite = input("Do you want to continue and potentially overwrite files? (y/n): ").lower()
    if overwrite != 'y':
        print("Operation cancelled.")
        exit()
else:
    os.mkdir(dir_name)

# Get available Bible versions from json folder
json_files = [f for f in os.listdir("json") if f.endswith('.json') and f != 'abbrev_map.json']
bible_versions = [f.replace('.json', '') for f in json_files]

print("\nAvailable Bible versions:")
for i, version in enumerate(bible_versions, 1):
    print(f"{i}. {version}")

# Get user selection
while True:
    try:
        selection = int(input(f"\nSelect a Bible version (1-{len(bible_versions)}): "))
        if 1 <= selection <= len(bible_versions):
            bible_version = bible_versions[selection - 1]
            print(f"Selected: {bible_version}")
            break
        else:
            print(f"Please enter a number between 1 and {len(bible_versions)}")
    except ValueError:
        print("Please enter a valid number")

with open(f"json/{bible_version}.json") as file:
    data = json.load(file)
    books = data['books']

with open("json/abbrev_map.json") as abbrev_file:
    abbrev = json.load(abbrev_file)

abbrev_map = {}

for entry in abbrev:
    abbrev_map.update(entry)

book_index = 1
for book_title in books:
    print(f"Processing {book_title}...")
    abbrev = abbrev_map[book_title]
    formatted_book_title = str.replace(book_title, " ", "_")
    file_title = f"{book_index:02d}_{formatted_book_title}"
    book = books[f"{book_title}"]
    chapters = [chapter for chapter in book]
    fulltexts = []

    for chapter_num in chapters:
        chapter_content = book[chapter_num]  # Get the actual chapter content
        chapter_verses = []
        
        # Extract verses from the chapter
        for verse_num in chapter_content:
            verse_text = chapter_content[verse_num]
            chapter_verses.append(verse_text)
        
        fulltexts.append(chapter_verses)

    with open(f"{dir_name}/{file_title}.md", "w") as file:
        file.write(f"tags: #{bible_version} #{formatted_book_title} #{abbrev}\n\n")
        file.write(f"# {book_title}\n\n")
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

