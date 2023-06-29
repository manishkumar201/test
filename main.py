import os
from github import Github
from datetime import datetime, timedelta

# env values
g = Github(os.environ["GITHUB_TOKEN"])
repo = g.get_repo(os.environ['REPO_NAME'])
pulls = repo.get_pulls(state='open')
MERGE_PR = os.environ.get("MERGE_PR")
CLOSE_PR = os.environ.get("CLOSE_PR")

print("repo:",repo)
print("pulls:",pulls)

# 1.Check if there are any open pull requests
if pulls.totalCount == 0:
    print('No open pull requests, exiting...')
    exit()

# 5.Check if the pull request has a description
for pull in pulls:
    if not pull.body:
        try:
            pull.edit(state='closed')
            pull.create_issue_comment('No Description on PR body. Please add valid description.')
            print("Pull request", pull.number, "No Description on PR body. Please add valid description.")
        except Exception as e:
            print('Error occurred while processing pull request:', pull.number)
            print('Error:', e)

# 6.Check if the Approved or Close comments in the pull request comments
def merge():
    if 'PR_NUMBER' in os.environ:
        pr_number = int(os.environ['PR_NUMBER'])
        pr = repo.get_pull(pr_number)
        print("pr_number:", pr_number)
        print("pr:", pr)
        try:
            pr.merge(merge_method = 'merge', commit_message ='Pull Request Approved and Merged!')
            pr.create_issue_comment('This pull request was approved and merged because of a slash command.')
            print("Pull request:", pr, "was approved and merged because of a slash command.")
        except Exception as e:
            print(f"Failed to merge PR: {str(e)}")
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
    if MERGE_PR.__eq__('true'):
        merge()  
    if CLOSE_PR.__eq__('true'):
        close()   
    print('end')       