from __future__ import annotations

import os
from pathlib import Path

import requests
import yaml
from dotenv import load_dotenv


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DISCORD_ROLES_PATH = PROJECT_ROOT / "config" / "notifications" / "discord_roles_manga.yaml"


def load_discord_roles() -> dict:
    if not DISCORD_ROLES_PATH.exists():
        print(f"[WARN] Fichier rôles introuvable: {DISCORD_ROLES_PATH}")
        return {}

    with DISCORD_ROLES_PATH.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    return data.get("roles", {})


def get_role_for_title(title: str) -> str | None:
    roles = load_discord_roles()
    return roles.get(title)


def send_discord_notification(
    title: str,
    chapters: list[str] | str,
    url: str,
    site: str,
) -> None:
    print(f"[DEBUG] Appel send_discord_notification pour {title}")

    webhook_url = os.getenv("DISCORD_MANGA_WEBHOOK_URL")
    if not webhook_url:
        print("[WARN] DISCORD_MANGA_WEBHOOK_URL absent")
        return

    role = get_role_for_title(title)

    if isinstance(chapters, list):
        chapters_text = ", ".join(str(chapter) for chapter in chapters)
        chapter_count = len(chapters)
    else:
        chapters_text = str(chapters)
        chapter_count = 1

    role_mention = f"<@&{role}> " if role else ""

    message = (
        f"{role_mention}{chapter_count} nouveau(x) chapitre(s) pour **{title}** : {chapters_text}\n"
        f"{site} → {url}"
    )

    payload = {
        "content": message,
        "allowed_mentions": {
            "parse": [],
            "roles": [str(role)] if role else [],
        },
    }

    print("[DEBUG] Payload Discord:", payload)

    response = requests.post(webhook_url, json=payload, timeout=15)

    print("[DEBUG] Discord status:", response.status_code)
    print("[DEBUG] Discord response:", response.text)
    print(f"[DEBUG] title={title} role={role!r}")

    response.raise_for_status()