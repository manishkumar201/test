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
if 'PR_NUMBER' in os.environ:
    try:
        pr_number = int(os.environ['PR_NUMBER'])
        pr = repo.get_pull(pr_number)
        print("pr_number:", pr_number)
        print("pr:", pr)
        files = pr.get_files()
        print(files)
        version_file_exist = False
        for file in files:
            if file.filename == 'VERSION':
                print("file -> " , file)
                version_file_exist = True
                break
        if not version_file_exist:
            pr.create_issue_comment('The VERSION file does not exist. Closing this pull request.')
            print('The VERSION file does not exist. Closing this pull request.')
            pr.edit(state='closed')  
        else:
            print('The VERSION file exists. All ohk')
        
    except Exception as e:
        print('PR_NUMBER :' , os.environ['PR_NUMBER'])
        print(f"Failed to check VERSION file : {str(e)}")
     
# 8. Check if version name from "VERSION" already exists as tag   
if 'PR_NUMBER' in os.environ:
    print("------------->" , os.environ['PR_NUMBER'])
    try:
        pr_number = int(os.environ['PR_NUMBER'])
        pr = repo.get_pull(pr_number)
        print("pr_number:", pr_number)
        print("pr:", pr)
        tags = repo.get_tags()
        tag_exist = False
        for tag in tags:
            if tag.name == VERSION_FILE:
                print("tag -> " , tag.name)
                tag_exist = True
                break
        if tag_exist:
            pr.create_issue_comment('The tag from VERSION file already exists. Closing this pull request.')
            print('The tag from VERSION file already exists. Closing this pull request.')
            pr.edit(state='closed') 
        else:
            print('The VERSION didnt matched with tag. All ohk')

    except Exception as e:
        print('PR_NUMBER :' , os.environ['PR_NUMBER'])
        print(f"Failed to compare version from VERSION  with tag: {str(e)}")
    