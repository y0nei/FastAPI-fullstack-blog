import time
from git import Repo

repo = Repo(search_parent_directories=True)
sha = repo.head.object.hexsha

if repo.head.is_detached is True:
    current_branch = repo.head
else:
    current_branch = repo.active_branch

def get_git_url_and_branch(repository: Repo = repo) -> dict[str, str]:
    remote_url = repository.remotes.origin.url

    if remote_url.startswith("git@"):
        remote_url = remote_url.replace(":", "/", 2).replace("git@", "https://", 1)
    if remote_url.endswith(".git"):
        remote_url = remote_url.replace(".git", "", 1)

    # Get current active branch or display `detached(commit_sha)`
    if repo.head.is_detached is True:
        branch = f"detached({str(repo.head.commit)[:7]})"
    else:
        branch = str(repo.active_branch)

    return {"url": remote_url, "branch": branch}

def get_git_version() -> str:
    commit_date = time.strftime("%Y.%m.%d", time.gmtime(current_branch.commit.committed_date))
    git_commit_date_hash = f"{commit_date}+{sha[:7]}".replace(".0", ".")
    if repo.is_dirty():
        git_commit_date_hash += "+dirty"

    return git_commit_date_hash
