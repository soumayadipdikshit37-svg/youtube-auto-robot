# youtube-auto-robot
Automated YouTube video creation and upload.

## What this does
- Generates simple video ideas and stores them in `data/ideas.json`.
- Creates short placeholder videos with FFmpeg.
- Uploads videos to YouTube Studio (requires credentials in environment variables).
- Writes daily reports in `data/reports/`.

## Quick start
```bash
pip install -r requirements.txt
python auto_pipeline.py
```

## Environment variables
Set these for uploads:
- `YOUTUBE_EMAIL`
- `YOUTUBE_PASSWORD`

Use `DRY_RUN=1` to skip uploads and only generate videos/reports.

## Scheduling
To run daily (three videos per day by default), schedule `python auto_pipeline.py` with a cron job or a hosted runner. The automation only runs while the machine is on and connected.

## Notes
- This project does **not** guarantee monetization or revenue. YouTube monetization eligibility depends on YouTube policies and channel performance.
