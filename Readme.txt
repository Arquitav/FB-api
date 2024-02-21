## Documentation for Facebook Automation Script

This document serves as a comprehensive guide to understanding and utilizing the provided Python script for automating various tasks related to Facebook post management. This script includes functionality for posting text and photos, fetching post content, moving posted images to a designated folder, and managing a list of post identifiers.

## Overview

The script is designed to automate the following tasks:
- Post text messages directly to a Facebook page or user profile.
- Post photos to a specific album on Facebook.
- Retrieve and display the content of a post using its ID.
- Move posted photos to a designated "published" folder on the local file system.
- Interact with a Google Sheets document to fetch numbers and prompts for posting.
- Keep track of used numbers and post IDs in a local text file.

## Dependencies

To run this script, you will need:
- Python 3.x installed on your system.
- The `facebook-sdk`, `gspread`, `oauth2client`, and `shutil` Python libraries.
- A valid Facebook Access Token with permissions to post on your Facebook page or profile.
- A Google Sheets API service account with access to the specific Google Sheet used by the script.

## Setup

### Installing Required Libraries

Install the required Python libraries using pip:

```bash
pip install facebook-sdk gspread oauth2client
```

### Facebook Access Token

1. Obtain a Facebook Access Token by creating a Facebook App and generating a token with the necessary permissions (`publish_to_groups`, `manage_pages`, `publish_pages`).
2. Save the token in a JSON file named `access_token.json` in the following format:

```json
{
  "access_token": "YOUR_ACCESS_TOKEN_HERE"
}
```

### Google Sheets API Service Account

1. Enable the Google Sheets API in the Google Developers Console.
2. Create a service account and download the credentials JSON file.
3. Share your Google Sheet with the service account's email address.
4. Rename the credentials file to `client_secret.json` and place it in the same directory as the script.

## Script Components

### Load Token

`load_token()`: Loads the Facebook Access Token from `access_token.json`.

### Post Text

`post_text(text)`: Posts a text message to Facebook.

### Get Post Content

`get_post_content(post_id)`: Retrieves the content of a Facebook post using its ID.

### Post Photo

`post_photo(file_dir, prompt)`: Posts a photo to a specific Facebook album using the album's ID.

### Get File Directory

`get_file_dir(number)`: Fetches the full path of an image based on a provided number.

### Move Image to Folder

`move_img_to_folder(image_path, destination_folder)`: Moves a posted image to the "published" folder.

### Google Sheets Interaction

- `get_column_numbers()`: Fetches a list of numbers from the first column of a specified Google Sheet.
- `get_column_prompts()`: Fetches a list of prompts from the third column of the same Google Sheet.
- `get_prompt(current_number, column_number_list, column_prompt_list)`: Retrieves a prompt based on the current number.

### Hashtags and Number Management

- `prompt_hashtags(prompt)`: Adds hashtags to each word in the provided prompt.
- `get_next_number(current_number, column_number_list)`: Finds the next number in the list.
- `get_current_number()`: Reads the current number from a local text file.
- `update_current_number(new_current_number)`: Updates the current number in the text file.
- `add_used_number(used_number, post_id)`: Adds a used number and its corresponding post ID to a text file.

### Utility Functions

- `time_counter(seconds)`: A countdown timer used to wait between posts due to Facebook's rate limits.

## Usage

Before running the script, ensure all setup steps are completed. Then, you can execute the script with:

```bash
python your_script_name.py
```

The script will automatically:
- Fetch numbers and prompts from the Google Sheet.
- Post text or photos to Facebook based on the prompts.
- Move posted photos to a designated folder.
- Update the local text files with the used numbers and post IDs.

## Conclusion

This script streamlines the process of managing posts on Facebook, especially for users looking to automate their social media interactions based on a schedule or a list of prompts. By integrating with Google Sheets, it also allows for easy management of post content and sequencing.
