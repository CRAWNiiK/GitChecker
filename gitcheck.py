import os
import platform
import requests
import argparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def clear_console():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print(Fore.CYAN + """
╔═══╗╔══╗╔════╗   ╔═══╗╔╗ ╔╗╔═══╗╔═══╗╔╗╔═╗╔═══╗╔═══╗
║╔═╗║╚╣╠╝║╔╗╔╗║   ║╔═╗║║║ ║║║╔══╝║╔═╗║║║║╔╝║╔══╝║╔═╗║
║║ ╚╝ ║║ ╚╝║║╚╝   ║║ ╚╝║╚═╝║║╚══╗║║ ╚╝║╚╝╝ ║╚══╗║╚═╝║
║║╔═╗ ║║   ║║     ║║ ╔╗║╔═╗║║╔══╝║║ ╔╗║╔╗║ ║╔══╝║╔╗╔╝
║╚╩═║╔╣╠╗ ╔╝╚╗    ║╚═╝║║║ ║║║╚══╗║╚═╝║║║║╚╗║╚══╗║║║╚╗
╚═══╝╚══╝ ╚══╝    ╚═══╝╚╝ ╚╝╚═══╝╚═══╝╚╝╚═╝╚═══╝╚╝╚═╝

_____________________________________________________
                by CRAWNiiK
_____________________________________________________
    """)

def set_console_title(title):
    os.system(f'title {title}' if platform.system() == 'Windows' else f'\033]0;{title}\007')

def get_github_user(username, include_repos=False):
    api_url_user = f'https://api.github.com/users/{username}'
    api_url_repos = f'https://api.github.com/users/{username}/repos'
    status_user, status_repos = 200, 200
    user_data, repos_data = {}, []

    try:
        response_user = requests.get(api_url_user)
        status_user, user_data = response_user.status_code, response_user.json()

        if include_repos:
            response_repos = requests.get(api_url_repos)
            status_repos, repos_data = response_repos.status_code, response_repos.json()

            # Sort repositories by stars in descending order
            repos_data.sort(key=lambda x: x['stargazers_count'], reverse=True)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error: {e}")

    if status_user == 200:
        print(Fore.GREEN + f"\nGitHub User Information for '{username}':")
        print(f"Name: {user_data.get('name', 'N/A')}")
        print(f"Bio: {user_data.get('bio', 'N/A')}")
        print(f"Public Repositories: {user_data.get('public_repos', 0)}")
        print(f"Followers: {user_data.get('followers', 0)}")
        print(f"Following: {user_data.get('following', 0)}")

        if include_repos and status_repos == 200:
            print(Fore.GREEN + "\nPublic Repositories (sorted by stars):")
            for repo in repos_data:
                print(Fore.YELLOW + f"\nRepository: {repo['name']}")
                print(f"Description: {repo['description']}")
                print(f"Stars: {repo['stargazers_count']}")
                print(Fore.RED + f"Link: {repo['html_url']}")
                print(Fore.MAGENTA + f"Git Clone Command: git clone {repo['clone_url']}")
    else:
        print(Fore.RED + f"Error: Unable to fetch GitHub user information. Status Code: {status_user}")
        if include_repos:
            print(Fore.RED + f"Error: Unable to fetch repository information. Status Code: {status_repos}")

def main():
    clear_console()
    set_console_title("GitHub User Info Script")
    parser = argparse.ArgumentParser(description='Fetch and display information about a GitHub user.')
    parser.add_argument('username', type=str, help='GitHub username')
    parser.add_argument('--repos', '-r', action='store_true', help='Include public repositories information')
    args = parser.parse_args()

    if not args.repos:
        print(Fore.YELLOW + f"Note: Use '--repos' if you want to see all of {args.username}'s repositories.")

    get_github_user(args.username, args.repos)

if __name__ == "__main__":
    main()
