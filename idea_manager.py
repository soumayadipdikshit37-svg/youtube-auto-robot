import json
import os
import random
from datetime import datetime

DEFAULT_STORE_PATH = "data/ideas.json"

IDEA_TEMPLATES = [
    {
        "title": "3 productivity tips for busy creators",
        "description": "Share three practical productivity habits creators can apply today.",
        "tags": ["productivity", "creator tips", "workflow"],
    },
    {
        "title": "Beginner guide to creating YouTube shorts",
        "description": "Explain the basic steps for making shorts with simple examples.",
        "tags": ["youtube shorts", "beginner", "content creation"],
    },
    {
        "title": "Top 5 free tools for video editing",
        "description": "Highlight free editing tools and a quick use case for each.",
        "tags": ["video editing", "tools", "free"],
    },
    {
        "title": "How to pick a niche for a new channel",
        "description": "Walk through a simple niche selection framework.",
        "tags": ["youtube", "niche", "strategy"],
    },
    {
        "title": "Weekly content planning checklist",
        "description": "Provide a checklist for planning a week's worth of content.",
        "tags": ["planning", "checklist", "content"],
    },
]


def ensure_store(path=DEFAULT_STORE_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as handle:
            json.dump({"ideas": []}, handle, indent=2)


def load_store(path=DEFAULT_STORE_PATH):
    ensure_store(path)
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_store(store, path=DEFAULT_STORE_PATH):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(store, handle, indent=2)


def generate_ideas(count):
    ideas = []
    for _ in range(count):
        template = random.choice(IDEA_TEMPLATES)
        idea = {
            "id": f"idea_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
            "title": template["title"],
            "description": template["description"],
            "tags": template["tags"],
            "status": "new",
            "created_at": datetime.utcnow().isoformat() + "Z",
        }
        ideas.append(idea)
    return ideas


def add_ideas(new_ideas, path=DEFAULT_STORE_PATH):
    store = load_store(path)
    store["ideas"].extend(new_ideas)
    save_store(store, path)
    return store


def get_next_ideas(count, path=DEFAULT_STORE_PATH):
    store = load_store(path)
    pending = [idea for idea in store["ideas"] if idea.get("status") == "new"]
    return pending[:count]


def mark_used(idea_ids, path=DEFAULT_STORE_PATH):
    store = load_store(path)
    for idea in store["ideas"]:
        if idea.get("id") in idea_ids:
            idea["status"] = "used"
            idea["used_at"] = datetime.utcnow().isoformat() + "Z"
    save_store(store, path)
    return store
