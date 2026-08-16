import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

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


def git_run(*args):
    result = subprocess.run(
        ["git"] + list(args),
        cwd=REPO_PATH,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.returncode == 0, result.stdout + result.stderr


@app.route("/")
def index():
    gems = load_gems()
    gems.sort(key=lambda g: g.get("added", ""), reverse=True)
    return render_template("index.html", gems=gems)


@app.route("/add", methods=["POST"])
def add():
    gems = load_gems()
    gem = {
        "seq": next_seq(gems),
        "added": now_iso(),
        "updated": now_iso(),
        "title": request.form["title"].strip(),
        "url": request.form["url"].strip(),
        "tags": [t.strip() for t in request.form["tags"].split(",") if t.strip()],
    }
    gems.append(gem)
    save_gems(gems)
    flash(f"Added: {gem['title']}")
    return redirect(url_for("index"))


@app.route("/edit/<int:seq>", methods=["POST"])
def edit(seq):
    gems = load_gems()
    for gem in gems:
        if gem["seq"] == seq:
            gem["title"] = request.form["title"].strip()
            gem["url"] = request.form["url"].strip()
            gem["tags"] = [t.strip() for t in request.form["tags"].split(",") if t.strip()]
            gem["updated"] = now_iso()
            break
    save_gems(gems)
    flash("Updated.")
    return redirect(url_for("index"))


@app.route("/delete/<int:seq>", methods=["POST"])
def delete(seq):
    gems = load_gems()
    gems = [g for g in gems if g["seq"] != seq]
    save_gems(gems)
    flash("Deleted.")
    return redirect(url_for("index"))


@app.route("/publish", methods=["POST"])
def publish():
    ok, out = git_run("add", "data/gems.json")
    if not ok:
        flash(f"git add failed: {out}")
        return redirect(url_for("index"))

    msg = request.form.get("commit_msg", "Update gems").strip() or "Update gems"
    ok, out = git_run("commit", "-m", msg)
    if not ok and "nothing to commit" not in out:
        flash(f"git commit failed: {out}")
        return redirect(url_for("index"))

    ok, out = git_run("push")
    if ok:
        flash("Published successfully.")
    else:
        flash(f"git push failed: {out}")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
