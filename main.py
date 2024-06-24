import os
import io
import sys
import requests
from dotenv import load_dotenv
import pandas as pd


def get_repo_details(owner, repo, token):
    # GitHub API URL for the repository
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"

    # Headers to include in the request
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Making the GET request to the GitHub API
    response = requests.get(url, headers=headers)

    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the JSON response
        repo_details = response.json()
        parsed_details = list()

        # Printing some details about the repository
        for index, detail in enumerate(repo_details):
            temp_dict = dict()
            temp_dict['User'] = detail['login']
            temp_dict['Contributions'] = detail['contributions']
            parsed_details.append(temp_dict)

        return parsed_details
    else:
        print(f"Failed to fetch repository details. Status code: {response.status_code}")


def get_max_contributor(owner, repo, token):
    result = get_repo_details(owner, repo, token)

    if not result:
        print(f"No contributors found for repository '{owner}/{repo}'")
        sys.exit()

    max_contributor = max(result, key=lambda x: x['Contributions'])
    
    if check_if_bot(max_contributor['User']):
        print('Bot found as max contributor. Retrieving next highest contributor...')
        next_contributor = get_next_highest_contributor(result, max_contributor['User'])
        return next_contributor
    return max_contributor['User']


def get_next_highest_contributor(contributors, bot_contributor):
    # Filter out the bot contributor
    non_bot_contributors = [contributor for contributor in contributors if contributor['User'] != bot_contributor]
    
    # Find the next highest contributor
    next_highest_contributor = max(non_bot_contributors, key=lambda x: x['Contributions'])
    return next_highest_contributor['User']


# Function to check if a github_username is a bot
def check_if_bot(github_username):
    bot_keywords = ['-bot', 'bot', '[bot]']
    return any(keyword in github_username.lower() for keyword in bot_keywords)


# Function to extract the markdown table from the file
def extract_markdown_table(content):
    lines = content.split('\n')
    table_lines = []
    in_table = False

    for line in lines:
        if '|' in line:  # A basic check to see if the line might be part of a table
            in_table = True
            table_lines.append(line.strip())
        elif in_table:
            # If we encounter a non-table line after being in a table, we break
            break
    
    return "\n".join(table_lines)


def get_users_list(owner, users, token):
    # URL to the raw markdown file in the GitHub repository
    url = f"https://raw.githubusercontent.com/{owner}/{users}"
    
    # Headers to include in the request
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # Making the GET request to the GitHub API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = response.text

        # Extract the markdown table
        markdown_table = extract_markdown_table(content)

        # Use io.StringIO to treat the string as a file
        table_io = io.StringIO(markdown_table)

        # Read the table using pandas
        df = pd.read_csv(table_io, sep="|", engine="python", skipinitialspace=True)

        # Strip whitespace from column names and data
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        # Drop empty columns if they exist
        if "" in df.columns:
            df = df.drop(columns=[""])

        # Drop the first and last row if they are empty
        if df.iloc[0].isnull().all():
            df = df.drop(index=0)
        if df.iloc[-1].isnull().all():
            df = df.drop(index=len(df)-1)

        # Reset the index after dropping rows
        df = df.reset_index(drop=True)

        return df
    else:
        print(f"Failed to fetch users repository. Status code: {response.status_code}")


# Function to find employee name (shortname) by github_username
def find_shortname_by_github_username(github_username, df):
    result = df[df['github_username'] == github_username]
    if not result.empty:
        shortname = result.iloc[0]['shortname']
        return shortname
    else:
        return None
    

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    owner = os.getenv("OWNER")
    repo = os.getenv("REPOSITORY_NAME")
    token = os.getenv("ACCESS_TOKEN")
    users = os.getenv("USERS_REPO")

    if owner and repo and token and users:
        username = get_max_contributor(owner, repo, token)
        users_df = get_users_list(owner, users, token)
        shortname = find_shortname_by_github_username(username, users_df)
        print(f"Possible repo owner: {shortname}")
    else:
        print("Environment variables OWNER, REPOSITORY_NAME, ACCESS_TOKEN, and USERS_REPO must be set.")
