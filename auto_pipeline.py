#!/usr/bin/env python3
import json
import os
from datetime import datetime

from idea_manager import add_ideas, generate_ideas, get_next_ideas, mark_used
from video_creator import create_video
from youtube_uploader import upload_video

DEFAULT_DAILY_COUNT = 3
REPORTS_DIR = "data/reports"


def write_report(report):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    filename = datetime.utcnow().strftime("%Y-%m-%d") + ".json"
    path = os.path.join(REPORTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    return path


def daily_run(target_count=DEFAULT_DAILY_COUNT, dry_run=False):
    print("🗓️  Starting daily automation run")

    pending = get_next_ideas(target_count)
    if len(pending) < target_count:
        needed = target_count - len(pending)
        print(f"Generating {needed} new ideas...")
        add_ideas(generate_ideas(needed))
        pending = get_next_ideas(target_count)

    report = {
        "date": datetime.utcnow().isoformat() + "Z",
        "target_count": target_count,
        "videos": [],
    }

    used_ids = []
    for idea in pending:
        print(f"Creating video for idea: {idea['title']}")
        video_path = create_video(idea=idea)
        upload_result = False
        if video_path:
            if dry_run or os.getenv("DRY_RUN") == "1":
                print("DRY_RUN enabled: skipping upload")
                upload_result = True
            else:
                upload_result = upload_video(
                    video_path,
                    title=idea["title"],
                    description=idea["description"],
                    tags=idea.get("tags", []),
                )
        else:
            print("Video creation failed; skipping upload")

        report["videos"].append(
            {
                "idea_id": idea["id"],
                "title": idea["title"],
                "video_path": video_path,
                "uploaded": upload_result,
            }
        )

        if video_path:
            used_ids.append(idea["id"])

    if used_ids:
        mark_used(used_ids)

    report_path = write_report(report)
    print(f"📄 Daily report saved to {report_path}")
    return report


if __name__ == "__main__":
    daily_run()
