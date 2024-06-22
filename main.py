import os
import requests
from dotenv import load_dotenv


def get_repo_details(owner, repo):
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


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    owner = os.getenv("OWNER")
    repo = os.getenv("REPOSITORY_NAME")
    token = os.getenv("ACCESS_TOKEN")

    if owner and repo and token:
        result = get_repo_details(owner, repo)
        max_contributor = max(result, key=lambda x: x['Contributions'])
        print(f"Possible Repo Owner (GitHub Username): {max_contributor['User']}")
    else:
        print("Environment variables OWNER, REPOSITORY_NAME, and ACCESS_TOKEN must be set.")
