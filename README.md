# Guess Repo Owner

## Description
This script will quickly guess the repository based on the amount of contributions. The most number of contributions is assumed the owner of the repository.

I'm using the amount of contributions because the topic tags are not often used in an organization for repo identification and other info.

## Sample Use-Case (Cybersecurity)
This can be integrated to an incident management tool so that SOC and IR can quickly identify the contact for repositories with exposed secrets/credentials.

## Running in your Local Machine

1. create a `.env` file and put the necessary info, i.e., OWNER, REPOSITORY_NAME, ACCESS_TOKEN.

    ```
    OWNER=githubuser
    REPOSITORY_NAME=githubrepo
    ACCESS_TOKEN=myaccesstoken_1234567890
    ```

2. setup the Python environment (run the following commands)

    ```shell
    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ python main.py
    ```
