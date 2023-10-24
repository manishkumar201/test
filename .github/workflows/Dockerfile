# Use the official GitHub CLI Docker image as the base image
FROM ghcr.io/github/gh:latest

# Install the gh-pr-draft extension
RUN gh extension install kyanny/gh-pr-draft

# Set the entry point to the GitHub CLI
ENTRYPOINT ["gh"]
