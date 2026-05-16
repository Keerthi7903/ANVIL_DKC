import httpx
from typing import Dict, Any

from config import settings


class DiscordNotificationError(Exception):
    pass


async def send_discord_alert(
    message: str
) -> bool:
    """
    Send alert to normal Discord webhook.
    """

    payload = {
        "content": message
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.DISCORD_WEBHOOK_URL,
            json=payload
        )

    return response.status_code in [200, 204]


async def send_manager_escalation(
    title: str,
    description: str
) -> bool:
    """
    Send escalation alert to manager Discord webhook.
    """

    embed = {
        "title": title,
        "description": description,
        "color": 16711680
    }

    payload = {
        "embeds": [embed]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.DISCORD_MANAGER_WEBHOOK_URL,
            json=payload
        )

    return response.status_code in [200, 204]