import json
import re
import os

# Get directory name and check if it exists
dir_name = input("Please enter Directory name: (e.g. 'KJV_by_verse_with_tags') ")
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
    book_dir = f"{dir_name}/{file_title}"
    if not os.path.exists(book_dir):
        os.mkdir(book_dir)

    chap_index = 1
    for chapter_num in chapters:
        print(f'Processing chapter: {chapter_num}')
        chapter_content = book[chapter_num]  # Get the actual chapter content
        chapter_dir = f"{book_dir}/Chapter_{chap_index:02d}"
        if not os.path.exists(chapter_dir):
            os.mkdir(chapter_dir)

        verse_index = 1
        for verse_num in chapter_content:
            verse_text = chapter_content[verse_num]
            verse_filename = f"{abbrev}_{chap_index}_{verse_index}.md"
            verse_path = os.path.join(chapter_dir, verse_filename)
            with open(verse_path, "w") as verse_file:
                verse_file.write(f"tags: #{bible_version} #{formatted_book_title} #{formatted_book_title}_{chap_index} #{formatted_book_title}_{chap_index}_{verse_index} ")
                verse_file.write(f"#{abbrev} #{abbrev}_{chap_index} #{abbrev}_{chap_index}_{verse_index}\n\n")
                verse_file.write(f"# {book_title} {chap_index}:{verse_index}\n\n")
                verse_file.write(f"{verse_text}\n")
            verse_index += 1
        chap_index += 1
    book_index += 1


