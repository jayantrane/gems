# ✦ Gems

Best reads curated by Jayant, collected over time.

Live at: [gems](https://gems.systemdesignprep.com)

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

The admin app lives in `admin/` and runs on your homelab. It provides a web UI to manage gems by directly editing `data/gems.json`.

### Setup with local virtual environment

```bash
cd /path/to/gems
python3 -m venv .venv
source .venv/bin/activate
pip install -r admin/requirements.txt
```

### Start

```bash
cd admin
python app.py
# Runs on http://localhost:5050
```

### Usage

- **View all gems**: Open `http://localhost:5050` — shows all gems sorted by date
- **Add a gem**: Fill in title, URL, and tags (comma-separated) at the top, click **Add**
- **Edit a gem**: Click **Edit** on any row, modify fields, click **Save**
- **Delete a gem**: Click **Del** on any row (confirmation prompt)
- **Save directly**: Add, edit, or delete operations are written to `data/gems.json` immediately

### Stop and exit

```bash
# In the terminal running Flask:
Ctrl+C

# Then deactivate the virtual environment:
deactivate
```

### How it works

The admin reads/writes `data/gems.json` directly and auto-detects the repo path from its own location. Git commit/push is handled outside the container.

## Local preview

```bash
python3 -m http.server 8888
# Open http://localhost:8888
```

## Run with Docker Compose

Use Docker Compose to run frontend and admin together with realtime edits from mounted files.

### Start both services

```bash
docker compose --env-file /mnt/media/projects/gems/.env.docker -f /mnt/media/projects/gems/docker-compose.yml up --build
```

### Access

- Frontend timeline: `http://localhost:8888`
- Admin editor: `http://localhost:5050`

Both services mount the repository folder, so updates to `data/gems.json`, `css/style.css`, `js/app.js`, and admin files are reflected immediately.

### Configure ports and project path

Edit `/mnt/media/projects/gems/.env.docker`:

- `COMPOSE_PROJECT_NAME`: compose project name (set to `gems` by default)
- `PROJECT_DIR`: absolute path of this repo on your machine
- `FRONTEND_PORT`: host port for timeline site
- `ADMIN_PORT`: host port for admin app

### Stop

```bash
docker compose --env-file /mnt/media/projects/gems/.env.docker -f /mnt/media/projects/gems/docker-compose.yml down
```