#!/usr/bin/env python3
import base64
import json
import mimetypes
import os
import shutil
import subprocess
import tempfile
import zipfile
from email.message import EmailMessage
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)


def require_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def google_access_token():
    client_id = require_env("GOOGLE_CLIENT_ID")
    client_secret = require_env("GOOGLE_CLIENT_SECRET")
    refresh_token = require_env("GOOGLE_DRIVE_REFRESH_TOKEN")
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def drive_headers(token):
    return {"Authorization": f"Bearer {token}"}


def create_drive_folder(token):
    name = "ADS Predictive Modeling Final Submission - Nikita Rogers"
    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    response = requests.post(
        "https://www.googleapis.com/drive/v3/files",
        headers={**drive_headers(token), "Content-Type": "application/json"},
        json=metadata,
        params={"fields": "id,name,webViewLink"},
        timeout=30,
    )
    response.raise_for_status()
    folder = response.json()

    perm = {
        "type": "anyone",
        "role": "reader",
    }
    requests.post(
        f"https://www.googleapis.com/drive/v3/files/{folder['id']}/permissions",
        headers={**drive_headers(token), "Content-Type": "application/json"},
        json=perm,
        params={"fields": "id"},
        timeout=30,
    ).raise_for_status()
    return folder


def upload_file(token, folder_id, path):
    path = Path(path)
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    metadata = {"name": path.name, "parents": [folder_id]}

    boundary = "===============nikita_ads_boundary=="
    body = []
    body.append(f"--{boundary}\r\n")
    body.append("Content-Type: application/json; charset=UTF-8\r\n\r\n")
    body.append(json.dumps(metadata))
    body.append("\r\n")
    body.append(f"--{boundary}\r\n")
    body.append(f"Content-Type: {mime_type}\r\n\r\n")
    prefix = "".join(body).encode("utf-8")
    suffix = f"\r\n--{boundary}--\r\n".encode("utf-8")

    response = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files",
        headers={
            **drive_headers(token),
            "Content-Type": f"multipart/related; boundary={boundary}",
        },
        params={"uploadType": "multipart", "fields": "id,name,webViewLink"},
        data=prefix + path.read_bytes() + suffix,
        timeout=300,
    )
    response.raise_for_status()
    return response.json()


def make_repo_zip():
    zip_path = DOCS / "ads-predictive-modeling-final-source.zip"
    if zip_path.exists():
        zip_path.unlink()
    skip_dirs = {".git", "__pycache__", "audio", "video", "slides"}
    skip_suffixes = {".mp4", ".mp3", ".pptx", ".html"}
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in ROOT.rglob("*"):
            if path == zip_path:
                continue
            rel = path.relative_to(ROOT)
            if any(part in skip_dirs for part in rel.parts):
                continue
            if path.is_dir():
                continue
            if path.suffix.lower() in skip_suffixes:
                continue
            zf.write(path, rel)
    return zip_path


def github_user(token):
    response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def ensure_github_repo(token, repo_name):
    user = github_user(token)
    owner = user["login"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    get_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    existing = requests.get(get_url, headers=headers, timeout=30)
    if existing.status_code == 200:
        return existing.json()["html_url"], owner
    if existing.status_code != 404:
        existing.raise_for_status()

    response = requests.post(
        "https://api.github.com/user/repos",
        headers=headers,
        json={
            "name": repo_name,
            "description": "Predictive modeling final project in R.",
            "private": False,
            "auto_init": False,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["html_url"], owner


def git_push(token, owner, repo_name):
    subprocess.run(["git", "add", "."], cwd=ROOT, check=True)
    status = subprocess.run(["git", "status", "--short"], cwd=ROOT, check=True, capture_output=True, text=True)
    if status.stdout.strip():
        subprocess.run(["git", "commit", "-m", "Complete predictive modeling submission package"], cwd=ROOT, check=True)

    remote_url = f"https://github.com/{owner}/{repo_name}.git"
    remotes = subprocess.run(["git", "remote"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()
    if "origin" in remotes:
        subprocess.run(["git", "remote", "set-url", "origin", remote_url], cwd=ROOT, check=True)
    else:
        subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=ROOT, check=True)

    env = os.environ.copy()
    askpass = tempfile.NamedTemporaryFile("w", delete=False)
    try:
        askpass.write(
            "#!/bin/sh\n"
            "case \"$1\" in\n"
            "  *Username*) echo x-access-token ;;\n"
            f"  *) echo '{token}' ;;\n"
            "esac\n"
        )
        askpass.close()
        os.chmod(askpass.name, 0o700)
        env.update({"GIT_ASKPASS": askpass.name, "GIT_TERMINAL_PROMPT": "0"})
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=ROOT, check=True, env=env)
    finally:
        try:
            os.unlink(askpass.name)
        except OSError:
            pass


def send_email(token, folder_link, github_link, uploaded):
    to_addr = os.environ.get("SUBMISSION_NOTIFY_EMAIL", "nikitarogers333@gmail.com")
    msg = EmailMessage()
    msg["To"] = to_addr
    msg["From"] = "me"
    msg["Subject"] = "ADS predictive modeling submission package"

    rows = "".join(
        f"<tr><td style='padding:8px;border:1px solid #ddd'>{item['name']}</td>"
        f"<td style='padding:8px;border:1px solid #ddd'><a href='{item.get('webViewLink', '')}'>Open</a></td></tr>"
        for item in uploaded
    )
    html = f"""
    <html>
      <body style="font-family:Arial,sans-serif;color:#20262e">
        <h2>ADS Predictive Modeling Submission Package</h2>
        <p>Drive folder: <a href="{folder_link}">{folder_link}</a></p>
        <p>GitHub repo: <a href="{github_link}">{github_link}</a></p>
        <h3>Uploaded files</h3>
        <table style="border-collapse:collapse">
          <tr><th style="padding:8px;border:1px solid #ddd;text-align:left">File</th><th style="padding:8px;border:1px solid #ddd;text-align:left">Link</th></tr>
          {rows}
        </table>
        <p>Review report and video before submission so methods and AI disclosure are understood.</p>
      </body>
    </html>
    """
    msg.set_content(f"Drive folder: {folder_link}\nGitHub repo: {github_link}\n")
    msg.add_alternative(html, subtype="html")

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8").rstrip("=")
    response = requests.post(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        headers={**drive_headers(token), "Content-Type": "application/json"},
        json={"raw": raw},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main():
    github_token = require_env("GITHUB_TOKEN")
    repo_name = "ads-predictive-modeling-final"

    zip_path = make_repo_zip()
    github_link, owner = ensure_github_repo(github_token, repo_name)
    git_push(github_token, owner, repo_name)

    google_token = google_access_token()
    folder = create_drive_folder(google_token)

    required_files = [
        ROOT / "Report-Team1.html",
        ROOT / "Executive_Summary-Team1.pptx",
        ROOT / "Video_Presentation-Team1.mp4",
        ROOT / "Video_Presentation_Slides-Team1.pptx",
        ROOT / "video_narration.mp3",
        ROOT / "video_script.md",
        ROOT / "README.md",
        ROOT / "report.Rmd",
        zip_path,
        DOCS / "model_test_results.csv",
        DOCS / "model_cv_results.csv",
        DOCS / "top_predictors.csv",
    ]
    optional_files = [
        ROOT / "submission_checklist.md",
        ROOT / "executive_summary_outline.md",
        ROOT / "video_presentation_outline.md",
    ]
    upload_targets = [p for p in required_files + optional_files if p.exists()]

    uploaded = [upload_file(google_token, folder["id"], path) for path in upload_targets]
    email_result = send_email(google_token, folder.get("webViewLink", ""), github_link, uploaded)

    manifest = {
        "drive_folder": folder,
        "github_link": github_link,
        "uploaded": uploaded,
        "email_id": email_result.get("id"),
    }
    (DOCS / "publish_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
