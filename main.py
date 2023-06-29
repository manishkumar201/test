import os
from github import Github
from datetime import datetime, timedelta

# env values
g = Github(os.environ["GITHUB_TOKEN"])
repo = g.get_repo(os.environ['REPO_NAME'])
pulls = repo.get_pulls(state='open')
CLOSE_PR = os.environ.get("VERSION_EXIST")

print("repo:",repo)
print("pulls:",pulls)

# 1.Check if there are any open pull requests
if pulls.totalCount == 0:
    print('No open pull requests, exiting...')
    exit()


def close():
    if 'PR_NUMBER' in os.environ:
        pr_number = int(os.environ['PR_NUMBER'])
        pr = repo.get_pull(pr_number)
        print("pr_number:", pr_number)
        print("pr:", pr)
        try:
            pr.edit(state="closed")
            pr.create_issue_comment('This pull request was closed because of a slash command.')
            print("Pull request:", pr, "was closed because of a slash command.")
        except Exception as e:
            print(f"Failed to close PR: {str(e)}")

if __name__ == '__main__':
    print('start')  
    if CLOSE_PR.__eq__('false'):
        close()   
    print('end')       