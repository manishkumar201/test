id=$(gh pr view $1 --json id -q '.id')

MUTATION='
  mutation($id: ID!) {
    convertPullRequestToDraft(input: { pullRequestId: $id }) {
      pullRequest {
        id
        number
        isDraft
      }
    }
  }
'
gh api graphql -F id="${id}" -f query="${MUTATION}" >/dev/null
