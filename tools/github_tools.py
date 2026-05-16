import httpx
from typing import List, Dict, Any

from config import settings


BASE_URL = "https://api.github.com"


headers = {
    "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


class GitHubAPIError(Exception):
    pass


async def get_pr_details(
    owner: str,
    repo: str,
    pr_number: int
) -> Dict[str, Any]:
    """
    Fetch pull request details from GitHub.
    """

    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=headers
        )

    if response.status_code != 200:
        raise GitHubAPIError(
            f"Failed to fetch PR details: {response.text}"
        )

    return response.json()


async def list_pr_reviewers(
    owner: str,
    repo: str,
    pr_number: int
) -> List[str]:
    """
    Get list of reviewers assigned to a PR.
    """

    pr_data = await get_pr_details(
        owner,
        repo,
        pr_number
    )

    reviewers = [
        reviewer["login"]
        for reviewer in pr_data.get(
            "requested_reviewers",
            []
        )
    ]

    return reviewers


async def request_reviewer(
    owner: str,
    repo: str,
    pr_number: int,
    reviewer_login: str
) -> bool:
    """
    Assign reviewer to pull request.
    """

    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers"

    payload = {
        "reviewers": [reviewer_login]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            json=payload
        )

    return response.status_code in [201, 200]


async def post_pr_comment(
    owner: str,
    repo: str,
    pr_number: int,
    body: str
) -> str:
    """
    Post a comment on a PR.
    """

    url = f"{BASE_URL}/repos/{owner}/{repo}/issues/{pr_number}/comments"

    payload = {
        "body": body
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers=headers,
            json=payload
        )

    if response.status_code not in [200, 201]:
        raise GitHubAPIError(
            f"Failed to post comment: {response.text}"
        )

    data = response.json()

    return data["html_url"]