from __future__ import annotations

import getpass
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import requests


OWNER = "Tom6661"
REPOSITORY = "esp32-arduino-2023112450"
ROOT = Path(__file__).resolve().parents[1]
CA_BUNDLE = ROOT / ".github-ca-bundle.pem"


def run_git(*args: str, env: dict[str, str] | None = None) -> None:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        env=env,
        text=True,
    )
    if completed.returncode:
        raise SystemExit(completed.returncode)


def main() -> None:
    if not CA_BUNDLE.exists():
        raise SystemExit(
            f"Missing CA bundle: {CA_BUNDLE}\n"
            "Run this script from the prepared workspace."
        )

    token = getpass.getpass("GitHub Token (input is hidden): ")
    if not token:
        raise SystemExit("No token entered.")

    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }
    )

    user_response = session.get(
        "https://api.github.com/user",
        verify=str(CA_BUNDLE),
        timeout=30,
    )
    if user_response.status_code != 200:
        raise SystemExit(
            f"GitHub authentication failed: {user_response.status_code}\n"
            f"{user_response.text}"
        )

    login = user_response.json().get("login")
    if login != OWNER:
        raise SystemExit(f"Token belongs to {login!r}, expected {OWNER!r}.")
    print(f"Authenticated as {login}.")

    repo_url = f"https://github.com/{OWNER}/{REPOSITORY}.git"
    check = session.get(
        f"https://api.github.com/repos/{OWNER}/{REPOSITORY}",
        verify=str(CA_BUNDLE),
        timeout=30,
    )
    if check.status_code == 404:
        created = session.post(
            "https://api.github.com/user/repos",
            json={
                "name": REPOSITORY,
                "description": "ESP32 Arduino course project for 2023112450",
                "private": False,
                "has_issues": False,
                "has_projects": False,
                "has_wiki": False,
            },
            verify=str(CA_BUNDLE),
            timeout=30,
        )
        if created.status_code not in (201,):
            raise SystemExit(
                f"Repository creation failed: {created.status_code}\n"
                f"{created.text}"
            )
        print(f"Created {repo_url}.")
    elif check.status_code == 200:
        print(f"Repository already exists: {repo_url}.")
    else:
        raise SystemExit(f"Repository lookup failed: {check.status_code}\n{check.text}")

    run_git("add", ".gitignore", "README.md", "docs", "src", "scripts")
    status = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=ROOT,
    )
    if status.returncode:
        run_git("commit", "-m", "完善 GitHub 发布配置")

    remotes = subprocess.run(
        ["git", "remote"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.split()
    if "origin" in remotes:
        run_git("remote", "set-url", "origin", repo_url)
    else:
        run_git("remote", "add", "origin", repo_url)

    with tempfile.TemporaryDirectory() as temp_dir:
        askpass = Path(temp_dir) / "askpass.py"
        askpass.write_text(
            "import os, sys\n"
            "prompt = sys.argv[1].lower() if len(sys.argv) > 1 else ''\n"
            "print(os.environ['GITHUB_USERNAME'] if 'username' in prompt "
            "else os.environ['GITHUB_TOKEN'])\n",
            encoding="utf-8",
        )
        git_env = os.environ.copy()
        git_env.update(
            {
                "GIT_ASKPASS": str(askpass),
                "GIT_TERMINAL_PROMPT": "0",
                "GITHUB_USERNAME": OWNER,
                "GITHUB_TOKEN": token,
            }
        )
        run_git("push", "-u", "origin", "HEAD:main", env=git_env)

    print(f"Published successfully: https://github.com/{OWNER}/{REPOSITORY}")


if __name__ == "__main__":
    main()
