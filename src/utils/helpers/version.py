import subprocess

def subprocess_run(args, **kwargs) -> str:
    kwargs["encoding"] = kwargs.get("encoding", "utf-8")
    kwargs["stdout"] = subprocess.PIPE
    kwargs["stderr"] = subprocess.PIPE
    # raise CalledProcessError if returncode is non-zero
    kwargs["check"] = True
    proc = subprocess.run(args, **kwargs)
    return proc.stdout.strip()


def get_git_url_and_branch() -> dict[str, str]:
    try:
        ref = subprocess_run(["git", "rev-parse", "--abbrev-ref", "@{upstream}"])
    except subprocess.CalledProcessError:
        ref = subprocess_run(["git", "rev-parse", "--abbrev-ref", "master@{upstream}"])
    origin, git_branch = ref.split("/", 1)
    git_url = subprocess_run(["git", "remote", "get-url", origin])

    # get https:// url from git@ url
    if git_url.startswith("git@"):
        git_url = git_url.replace(":", "/", 2).replace("git@", "https://", 1)
    if git_url.endswith(".git"):
        git_url = git_url.replace(".git", "", 1)

    return {"url": git_url, "branch": git_branch}


def get_git_version() -> str:
    git_commit_date_hash = subprocess_run(
        ["git", "show", "-s", "--date=format:%Y.%m.%d", "--format=%cd+%h"]
    ).replace(".0", ".")
    return git_commit_date_hash
