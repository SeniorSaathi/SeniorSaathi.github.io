import requests
import json
import os

def github_repo_finder(query, n, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    params = {
        'q': query,
        'sort': 'stars',
        'order': 'desc',
    }

    response = requests.get('https://api.github.com/search/repositories', headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        repos = []
        for item in data.get('items', [])[:n]:
            repo_name = item.get('full_name')
            repo_url = item.get('html_url')
            repos.append([repo_name, repo_url])
        return repos
    else:
        print(f"Error: Unable to fetch data from GitHub API. Status code {response.status_code}")
        return None

def generate_query(domain):
    return f"learn+{domain.lower()} stars:>100"

if __name__ == '__main__':
    with open('github_pa.txt', 'r') as f:
        github_token = f.read().strip()

    for line in open('domains.txt'):
        line = line.rstrip('\n')
        line = line.replace(' ', '+')
        line = line.replace('/', '+')
        line = line.replace(':', '+')
        query = generate_query(line)
        file_name = os.path.join("DB", "proj_repos", f"{line}.json")
        n = 10

        try:
            repos = github_repo_finder(query, n, github_token)
            if repos:
                with open(file_name, 'w') as f:
                    json.dump(repos, f, indent=2)
                print(f"Data saved to {file_name}")
            else:
                print("No data was scraped.")
        except Exception as e:
            print(f"Error: {str(e)}")
