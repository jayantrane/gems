# ✦ Gems

Best reads curated by Jayant, collected over time.

Live at: **gems.systemdesignprep.com**

## What

A single-page static website that displays curated articles in a vertical timeline. Each entry has a date, title (linking to the original article), and tags.

## How it's presented

- Reverse-chronological timeline — newest articles at the top
- CSS Grid layout: `date | timeline dot | article title | tags`
- Scroll-based fade effect — articles glow white when in viewport, fade out when scrolled away
- Dark mode by default, light mode toggle (persisted in localStorage)
- Tag filtering — click any tag to filter the timeline
- Designed for 1920×1080+ screens, responsive at ≤768px
- No framework — plain HTML, CSS, vanilla JS. No build step.

## JSON Schema (`data/gems.json`)

```json
{
  "gems": [
    {
      "seq": 1,
      "added": "2026-08-15T10:30:00Z",
      "updated": "2026-08-15T10:30:00Z",
      "title": "How Discord Stores Trillions of Messages",
      "url": "https://discord.com/blog/how-discord-stores-trillions-of-messages",
      "tags": ["database", "cassandra", "scale"]
    }
  ]
}
```

| Field     | Type     | Description                              |
|-----------|----------|------------------------------------------|
| `seq`     | int      | Auto-incrementing sequence number        |
| `added`   | string   | ISO 8601 timestamp when the gem was added |
| `updated` | string   | ISO 8601 timestamp of last edit          |
| `title`   | string   | Article title                            |
| `url`     | string   | Link to the original article             |
| `tags`    | string[] | List of topic tags                       |

## Admin (local only)

The admin app lives in `admin/` and runs on your homelab. It provides a web UI to manage gems and publish changes via git.

### Setup

```bash
cd admin
pip install -r requirements.txt
```

### Start

```bash
python app.py
# Runs on http://localhost:5050
```

### Usage

- **View all gems**: Open `http://localhost:5050` — shows all gems sorted by date
- **Add a gem**: Fill in title, URL, and tags (comma-separated) at the top, click **Add**
- **Edit a gem**: Click **Edit** on any row, modify fields, click **Save**
- **Delete a gem**: Click **Del** on any row (confirmation prompt)
- **Publish to git**: Enter an optional commit message at the bottom, click **Publish** — runs `git add`, `commit`, and `push`

### How it works

The admin reads/writes `data/gems.json` directly. It auto-detects the repo path from its own location. The "Publish" button commits and pushes the JSON file to git, which syncs to Hostinger.

## Local preview

```bash
python3 -m http.server 8888
# Open http://localhost:8888
```