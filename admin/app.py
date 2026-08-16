import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, redirect, render_template, request, url_for, flash

app = Flask(__name__)
app.secret_key = "gems-admin-local-only"

REPO_PATH = Path(__file__).resolve().parent.parent
JSON_PATH = REPO_PATH / "data" / "gems.json"


def load_gems():
    if not JSON_PATH.exists():
        return []
    with open(JSON_PATH) as f:
        return json.load(f).get("gems", [])


def save_gems(gems):
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(JSON_PATH, "w") as f:
        json.dump({"gems": gems}, f, indent=2)
        f.write("\n")


def next_seq(gems):
    return max((g["seq"] for g in gems), default=0) + 1


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def is_valid_http_url(value):
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


@app.route("/")
def index():
    gems = load_gems()
    gems.sort(key=lambda g: g.get("added", ""), reverse=True)
    return render_template("index.html", gems=gems)


@app.route("/add", methods=["POST"])
def add():
    gems = load_gems()
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()
    tags = [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()]

    if not title:
        flash("Title is required.")
        return redirect(url_for("index"))

    if not is_valid_http_url(url):
        flash("URL must start with http:// or https://")
        return redirect(url_for("index"))

    gem = {
        "seq": next_seq(gems),
        "added": now_iso(),
        "updated": now_iso(),
        "title": title,
        "url": url,
        "tags": tags,
    }
    gems.append(gem)
    save_gems(gems)
    flash(f"Added: {gem['title']}")
    return redirect(url_for("index"))


@app.route("/edit/<int:seq>", methods=["POST"])
def edit(seq):
    gems = load_gems()
    title = request.form.get("title", "").strip()
    url = request.form.get("url", "").strip()
    tags = [t.strip() for t in request.form.get("tags", "").split(",") if t.strip()]

    if not title:
        flash("Title is required.")
        return redirect(url_for("index"))

    if not is_valid_http_url(url):
        flash("URL must start with http:// or https://")
        return redirect(url_for("index"))

    updated = False
    for gem in gems:
        if gem["seq"] == seq:
            gem["title"] = title
            gem["url"] = url
            gem["tags"] = tags
            gem["updated"] = now_iso()
            updated = True
            break

    if not updated:
        flash("Gem not found.")
        return redirect(url_for("index"))

    save_gems(gems)
    flash("Updated.")
    return redirect(url_for("index"))


@app.route("/delete/<int:seq>", methods=["POST"])
def delete(seq):
    gems = load_gems()
    initial_count = len(gems)
    gems = [g for g in gems if g["seq"] != seq]
    if len(gems) == initial_count:
        flash("Gem not found.")
        return redirect(url_for("index"))

    save_gems(gems)
    flash("Deleted.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
