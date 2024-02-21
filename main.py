import shutil
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import facebook as fb
import os
import time

# Load authorization token
def load_token():
    with open("access_token.json", "r") as file:  # Token expires on April 18th
        config = json.load(file)
    return config["access_token"]

# Post text only
def post_text(text):
    graph_api = fb.GraphAPI(load_token())
    response = graph_api.put_object("me", "feed", message=text)
    post_id = response["id"]
    print("Text post successful")
    return print(post_id)

# Get content of a post by its ID
def get_post_content(post_id):
    graph_api = fb.GraphAPI(load_token())
    content = graph_api.get_object(f"{post_id}")
    return print(content)

# Post a photo
def post_photo(file_dir, prompt):
    graph_api = fb.GraphAPI(load_token())
    album_id = "YOUR_ALBUM_ID"  # AI album
    with open(file_dir, 'rb') as image_file:
        post_img = graph_api.put_photo(image_file, album_path=album_id + "/photos", message=prompt)
        print("Image posted successfully")
    post_id = post_img["id"]
    return post_id

# Get the full path of the image according to the entered image number
def get_file_dir(number):
    images_folder = r"path\to\your\images\folder"
    number_str = str(number) + " "
    for file in os.listdir(images_folder):
        if file.startswith(number_str):
            print(file)
            full_path = f"{images_folder}\{file}"
            return full_path
    return None

# Move the published image to another folder "published"
def move_img_to_folder(image_path, destination_folder):
    shutil.move(image_path, destination_folder)
    return print("Image moved to 'published' folder")

# Obtain a list with all the numbers from column 1
def get_column_numbers():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Python Project").get_worksheet(2)  # Open the spreadsheet at the indicated index

    column = sheet.col_values(1)
    column_values = sheet.get(f"A2:A{len(column)}")
    column_list = []

    for row in column_values:
        column_list.append(int(row[0]))

    return column_list

# Get a list with all the prompts from column 3
def get_column_prompts():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Python Project").get_worksheet(2)

    column = sheet.col_values(3)
    column_values = sheet.get(f"C2:C{len(column)}")
    prompts_list = []

    for row in column_values:
        prompts_list.append(str(row[0]))

    return prompts_list

# From the list of numbers, compare with the given number to obtain the index and get the value of that index from the prompt column
def get_prompt(current_number, column_number_list, column_prompt_list):
    index_num = column_number_list.index(int(current_number))
    prompt = column_prompt_list[index_num]
    print(prompt)
    return prompt

# Add hashtags to each word of the prompt
def prompt_hashtags(prompt):
    elements_after_split = prompt.split(",")
    stripped_elements = []
    for element in elements_after_split:
        stripped_element = element.strip()
        stripped_elements.append(stripped_element)

    stripped_elements.pop(-1)
    predefined_hashtags = ["#AI", "#AI_art", "#Artificial_Intelligence"]

    new_elements = []
    for element in stripped_elements:
        replaced_element = element.replace("'", ' ').replace('-', ' ')
        replaced_element = replaced_element.replace(' ', '_')
        new_elements.append(f"#{replaced_element}")

    new_elements.extend(predefined_hashtags)
    new_prompt = " ".join(new_elements)

    print(new_prompt)
    return new_prompt

# Get the next number from the column
def get_next_number(current_number, column_number_list):
    index_num = column_number_list.index(int(current_number))
    next_number = column_number_list[int(index_num) + 1]
    return next_number

# Get the current number from a txt file
def get_current_number():
    file_path = "current_number.txt"
    with open(file_path, 'r') as file:
        current_number = file.read().strip()
        print("Current number:", current_number)
    return current_number

# Update the current number to a new one in the txt file
def update_current_number(new_current_number):
    file_path = "current_number.txt"
    with open(file_path, "w") as file:
        file.write(str(new_current_number))
    return print("Current number updated:", new_current_number)

# Add the processed number to a txt file of used numbers
def add_used_number(used_number, post_id):
    file_path = "used_numbers.txt"
    try:
        with open(file_path, 'r') as file:
            existing_numbers = file.read().splitlines()
    except FileNotFoundError:
        existing_numbers = []

    used_number_str = str(used_number)
    if used_number_str in existing_numbers:
        print("Number already added")
    else:
        with open(file_path, 'a') as file:
            file.write(f"{used_number_str}, {post_id}\n")
            print("Current number saved")

# Time counter
def time_counter(seconds):
    for remaining_seconds in range(seconds, 0, -1):
        print("                      ", end="\r")
        print(f"Seconds remaining: {remaining_seconds}", end='\r')
        time.sleep(1)
    print("----   time completed   -----")

if __name__ == "__main__":

    column_number_list = get_column_numbers()
    column_prompt_list = get_column_prompts()
    published_folder = r"path\to\your\published\images\folder"
    
    i = 0
    while i <= 200:
        print("Cycle:", i, "started")        
        if i != 0:
            time_counter(18)

        number = get_current_number()
        prompt = get_prompt(number, column_number_list, column_prompt_list)
        prompt_with_hashtags = prompt_hashtags(prompt)

        file_dir = get_file_dir(number)

        post_id = post_photo(file_dir, prompt_with_hashtags)
        add_used_number(number, post_id)
        move_img_to_folder(file_dir, published_folder)
        update_current_number(get_next_number(number, column_number_list))
        print("Cycle:", i, "completed")
        i += 1
