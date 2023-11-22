import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime



def github_repo_score(projects):
    net_score = 0
    repo_data_export = pd.DataFrame(columns=['repo_name', 'latest_commit', 'contributer_count', 'star_count', 'fork_count', 'languages_used', 'active_score', 'contributer_score', 'star_score', 'fork_score', 'language_score', 'net_score'])
    if len(projects) > 0:
        for project in projects:
            repo = requests.get(project)
            soup = BeautifulSoup(repo.text, 'html.parser')
            repo_name = soup.select_one('strong[itemprop="name"] a').getText()
            relative_time_html_element = soup.select_one('relative-time')
            if relative_time_html_element is not None:
                # latest_commit = datetime.datetime.strptime(relative_time_html_element['datetime'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
                latest_commit = datetime.datetime.strptime(relative_time_html_element['datetime'], "%Y-%m-%dT%H:%M:%S%z")
            else:
                # latest_commit = datetime.datetime.strptime('1970-01-01T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
                latest_commit = datetime.datetime.strptime('1970-01-01T00:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')

            current_date = datetime.datetime.now(datetime.timezone.utc)
            print(current_date, latest_commit, sep='\n')
            if latest_commit >= current_date - datetime.timedelta(days=30):
                active_score = 1
            elif latest_commit >= current_date - datetime.timedelta(days=90):
                active_score = 0.8
            elif latest_commit >= current_date - datetime.timedelta(days=180):
                active_score = 0.6
            elif latest_commit >= current_date - datetime.timedelta(days=365):
                active_score = 0.4
            else:
                active_score = 0.2

            contributer_count_element = soup.select_one('a[href*="/graphs/contributors"] span.Counter')
            if contributer_count_element is not None:
                contributer_count = contributer_count_element.text
                if 'k' in contributer_count_element.text:
                    contributer_count = int(contributer_count_element.text.replace('k', '')) * 1000
                contributer_count = int(contributer_count)
            else:
                contributer_count = 0

            if contributer_count == 1:
                contributer_score = 0.2
            elif contributer_count == 2:
                contributer_score = 0.4
            elif contributer_count == 3:
                contributer_score = 0.6
            elif contributer_count == 4:
                contributer_score = 0.8
            else:
                contributer_score = 1

            star_count_element = soup.select_one('a[href*="/stargazers"] strong')
            if star_count_element is not None:
                star_count = star_count_element.text.replace(',', '')
                if 'k' in star_count_element.text:
                    star_count = int(float(star_count_element.text.replace('k', '')) * 1000)
                star_count = int(star_count)
            else:
                star_count = 0

            if star_count == 0:
                star_score = 0.2
            elif star_count <= 10:
                star_score = 0.4
            elif star_count <= 50:
                star_score = 0.6
            elif star_count <= 100:
                star_score = 0.8
            else:
                star_score = 1

            fork_count_element = soup.select_one('a[href*="/forks"] strong')
            if fork_count_element is not None:
                fork_count = fork_count_element.text.replace(',', '')
                if 'k' in fork_count_element.text:
                    fork_count = int(float(fork_count_element.text.replace('k', '')) * 1000)
                fork_count = int(fork_count)
            else:
                fork_count = 0

            if fork_count == 0:
                fork_score = 0.2
            elif fork_count <= 10:
                fork_score = 0.4
            elif fork_count <= 50:
                fork_score = 0.6
            elif fork_count <= 100:
                fork_score = 0.8
            else:
                fork_score = 1

            languages_used = {}
            language_elements = soup.select('.BorderGrid-row .list-style-none li')
            for lang_element in language_elements:
                lang_name_element = lang_element.select_one('span.color-fg-default.text-bold')
                lang_percentage_element = lang_element.select_one('span:last-child')
                
                if lang_name_element is None or lang_percentage_element is None:
                    continue
                
                lang_name = lang_name_element.get_text(strip=True)
                lang_percentage = lang_percentage_element.get_text(strip=True)

                if lang_name.lower() == 'other':
                    continue
                
                languages_used[lang_name] = lang_percentage

            if len(languages_used) == 1:
                language_score = 0.3
            elif len(languages_used) == 2:
                language_score = 0.6
            elif len(languages_used) >= 3:
                language_score = 1
            else:
                language_score = 0


            repodata=[repo_name, latest_commit, contributer_count, star_count, fork_count, languages_used]
            reposcores = [active_score, contributer_score, star_score, fork_score, language_score]
            curr_net_score = sum(reposcores)/len(reposcores)
            # print(repodata, sep='\n')
            # print(reposcores, sep='\n')
            # print(curr_net_score, sep='\n')
            net_score += curr_net_score
            # add to dataframe 
            repo_data_export = pd.concat([repo_data_export, pd.DataFrame([repo_name, latest_commit, contributer_count, star_count, fork_count, languages_used, active_score, contributer_score, star_score, fork_score, language_score, curr_net_score], index=repo_data_export.columns).T])
        net_score = net_score/len(projects)
    return net_score, repo_data_export
            
                
projects = ["https://github.com/luminati-io/luminati-proxy", "https://github.com/realKarthikNair/realKarthikNair"]
github_repo_score(projects)

# todo : custom criteria values


# class GithubRepoScore:

#     def __init__(self, projects):
#         self.projects = projects
    
#     def repo_scrape(self, projects):
#         net_score = 0
#         if len(projects) > 0:
#             for project in projects:
#                 repo = requests.get(project)
#                 soup = BeautifulSoup(repo.text, 'html.parser')
#                 repo_name = soup.select_one('strong[itemprop="name"] a').getText()
#                 relative_time_html_element = soup.select_one('relative-time')
#                 if relative_time_html_element is not None:
#                     # latest_commit = datetime.datetime.strptime(relative_time_html_element['datetime'], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
#                     latest_commit = datetime.datetime.strptime(relative_time_html_element['datetime'], "%Y-%m-%dT%H:%M:%S%z")
#                 else:
#                     # latest_commit = datetime.datetime.strptime('1970-01-01T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
#                     latest_commit = datetime.datetime.strptime('1970-01-01T00:00:00+00:00', '%Y-%m-%dT%H:%M:%S%z')

#                 contributer_count_element = soup.select_one('a[href*="/graphs/contributors"] span.Counter')
#                 if contributer_count_element is not None:
#                     contributer_count = int(contributer_count_element.text)
#                 else:
#                     contributer_count = 0

#                 star_count_element = soup.select_one('a[href*="/stargazers"] strong')
#                 if star_count_element is not None:
#                     star_count = int(star_count_element.text.replace(',', ''))
#                 else:
#                     star_count = 0

#                 fork_count_element = soup.select_one('a[href*="/forks"] strong')
#                 if fork_count_element is not None:
#                     fork_count = int(fork_count_element.text.replace(',', ''))
#                 else:
#                     fork_count = 0

#                 languages_used = {}
#                 language_elements = soup.select('.BorderGrid-row .list-style-none li')
#                 for lang_element in language_elements:
#                     lang_name_element = lang_element.select_one('span.color-fg-default.text-bold')
#                     lang_percentage_element = lang_element.select_one('span:last-child')
                    
#                     if lang_name_element is None or lang_percentage_element is None:
#                         continue
                    
#                     lang_name = lang_name_element.get_text(strip=True)
#                     lang_percentage = lang_percentage_element.get_text(strip=True)

#                     if lang_name.lower() == 'other':
#                         continue
                    
#                     languages_used[lang_name] = lang_percentage


#         self.repodata=[repo_name, latest_commit, contributer_count, star_count, fork_count, languages_used]
    
    # def repo_score(self, repodata):

    #     active_score, contributer_score, star_score, fork_score, language_score = 0, 0, 0, 0, 0

    #     current_date = datetime.datetime.now(datetime.timezone.utc)
    #     latest_commit = repodata[1]
    #     if latest_commit >= current_date - datetime.timedelta(days=30):
    #         active_score = 1
    #     elif latest_commit >= current_date - datetime.timedelta(days=90):
    #         active_score = 0.8
    #     elif latest_commit >= current_date - datetime.timedelta(days=180):
    #         active_score = 0.6
    #     elif latest_commit >= current_date - datetime.timedelta(days=365):
    #         active_score = 0.4
    #     else:
    #         active_score = 0.2

    #     contributer_count = repodata[2]

    #     if contributer_count == 1:
    #         contributer_score = 0.2
    #     elif contributer_count == 2:
    #         contributer_score = 0.4
    #     elif contributer_count == 3:
    #         contributer_score = 0.6
    #     elif contributer_count == 4:
    #         contributer_score = 0.8
    #     else:
    #         contributer_score = 1

    #     star_count = repodata[3]

    #     if star_count == 0:
    #         star_score = 0.2
    #     elif star_count <= 10:
    #         star_score = 0.4
    #     elif star_count <= 50:
    #         star_score = 0.6
    #     elif star_count <= 100:
    #         star_score = 0.8
    #     else:
    #         star_score = 1

    #     fork_count = repodata[4]

    #     if fork_count == 0:
    #         fork_score = 0.2
    #     elif fork_count <= 10:
    #         fork_score = 0.4
    #     elif fork_count <= 50:
    #         fork_score = 0.6
    #     elif fork_count <= 100:
    #         fork_score = 0.8
    #     else:
    #         fork_score = 1

    #     languages_used = repodata[5]

    #     if len(languages_used) == 1:
    #         language_score = 0.3
    #     elif len(languages_used) == 2:
    #         language_score = 0.6
    #     elif len(languages_used) >= 3:
    #         language_score = 1
    #     else:
    #         language_score = 0

    #     self.reposcores = [active_score, contributer_score, star_score, fork_score, language_score]

            
