import os
from github import Github
from datetime import datetime, timedelta

# env values
g = Github(os.environ["GITHUB_TOKEN"])
repo = g.get_repo(os.environ['REPO_NAME'])
pulls = repo.get_pulls(state='open')
CLOSE_PR = os.environ.get("CLOSE_PR")
VERSION_FILE = os.environ.get("VERSION_FILE")

print("repo:",repo)
print("pulls:",pulls)

# 0 testing secrets
print("-------------testing secrets-------------")
SECRETS = os.environ.get("SECRETS");
print(SECRETS)


# 1.Check if there are any open pull requests
if pulls.totalCount == 0:
    print('No open pull requests, exiting...')
    exit()

# 2.Check if the pull request targets the master branch directly
for pull in pulls:
    if pull.base.ref == 'master' and not pull.head.ref.startswith('release/'):
        try:
            pull.edit(state='closed')
            pull.create_issue_comment('Do not accept PR target from feature branch to master branch.')
            print("Pull request", pull.number, "Do not accept PR target from feature branch to master branch.")
        except Exception as e:
            print('Error occurred while processing pull request:', pull.number)
            print('Error:', e)

# 3. Check All the files and see if there is a file named "VERSION"
for pull in pulls:
    # get_files() will fetch all the file names and store it in the files
    files = pull.get_files()
    version_file_exist = False
    for file in files:
        if file.filename == 'VERSION':
            print("file -> " , file)
            version_file_exist = True
            break
    
    # If the VERSION file is not modified, close the pull request
    if not version_file_exist:
        pull.create_issue_comment('The VERSION file does not exist. Closing this pull request.')
        pull.edit(state='closed')     

for pull in pulls:
    tags = repo.get_tags()
    tag_exist = False
    for tag in tags:
        if tag.name == VERSION_FILE:
            print("tag -> " , tag.name)
            tag_exist = True
            break

    if tag_exist:
        pull.create_issue_comment('The tag from VERSION file already exists. Closing this pull request.')
        pull.edit(state='closed') 
        
