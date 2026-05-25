# Photo Album Assignment — Simple Step-by-Step Tutorial

**Student:** Jessie Paragas  
**GitHub:** https://github.com/ivandelmiguez-tech/Integ-Assignment6  

This guide explains everything in plain language. Do the steps **in order**.

---

## What you already finished

- Built the Django photo album app
- Tested it on your computer (`python manage.py runserver`)
- Connected Cloudinary (for photos in the cloud)
- Pushed code to GitHub

**What is left:** Put the app on the internet (Render) and submit the assignment.

---

## Part A — Words you need to know

| Word | Meaning |
|------|---------|
| **Environment variable** | A secret setting stored on Render (not in your code). Like a password drawer the app reads at startup. |
| **Key** | The *name* of the setting (example: `SECRET_KEY`) |
| **Value** | The *actual text* that goes with that name |
| **DATABASE_URL** | A long link that tells Django how to connect to PostgreSQL on Render |
| **ALLOWED_HOSTS** | The website address Render gives you — Django only accepts visitors from that address |

---

## Part B — Deploy on Render (put app online)

### Step 1 — Log in to Render

1. Open https://render.com  
2. Sign up or log in (you can use your GitHub account).

---

### Step 2 — Create the database (PostgreSQL)

The assignment requires PostgreSQL, not SQLite.

1. Click the blue **New +** button (top right).  
2. Click **PostgreSQL**.  
3. Fill in:
   - **Name:** `photo-album-db` (any name is fine)
   - **Plan:** Free  
4. Click **Create Database**.  
5. Wait until status says **Available**.  
6. On that page, find **Connections** → copy **Internal Database URL**  
   - It looks like: `postgresql://photo_album_user:xxxxx@dpg-xxxxx-a/photo_album`  
   - Save it in Notepad — you will use it as `DATABASE_URL`.

---

### Step 3 — Create the website (Web Service)

1. Click **New +** again → **Web Service**.  
2. Connect **GitHub** if asked.  
3. Find and select your repo: **ivandelmiguez-tech / Integ-Assignment6**.  
4. Fill in the form:

| Field | What to type |
|-------|----------------|
| **Name** | `integ-assignment6` (or any short name — this becomes part of your URL) |
| **Region** | Same region as your database |
| **Branch** | `main` |
| **Root Directory** | Leave **empty** |
| **Runtime** | Python 3 |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn photo_project.wsgi:application` |
| **Plan** | Free |

5. **Do not click Create yet** — add environment variables first (Step 4).

---

### Step 4 — Add environment variables (the “name of variable” part)

Scroll down to **Environment Variables** → **Add Environment Variable**.

Add **one row for each line** below.  
- Left box = **Key** (the variable name)  
- Right box = **Value** (what goes inside)

| Key (copy exactly) | Value (what you put) |
|--------------------|----------------------|
| `SECRET_KEY` | Open PowerShell on your PC and run: `python -c "import secrets; print(secrets.token_urlsafe(50))"` — copy the long text it prints |
| `DEBUG` | `false` |
| `USE_SQLITE` | `false` |
| `ALLOWED_HOSTS` | Your Render URL **without** `https://` — example: `integ-assignment6.onrender.com` (you see the real name after you create the service; you can edit this later) |
| `DATABASE_URL` | Paste the **Internal Database URL** from Step 2 |
| `CLOUDINARY_CLOUD_NAME` | `dv6evsj2n` |
| `CLOUDINARY_API_KEY` | Your key from Cloudinary dashboard |
| `CLOUDINARY_API_SECRET` | Your secret from Cloudinary dashboard |

**Tip:** If Render lets you **Link Database**, you can link `photo-album-db` instead of pasting `DATABASE_URL` manually — Render fills it in for you.

6. Now click **Create Web Service**.  
7. Wait 5–10 minutes. Watch the **Logs** tab until it says the deploy succeeded.

---

### Step 5 — Fix ALLOWED_HOSTS if the site shows “DisallowedHost”

1. After deploy, Render shows your live URL at the top, e.g. `https://integ-assignment6.onrender.com`  
2. Go to **Environment** → edit `ALLOWED_HOSTS`  
3. Value should be **only the hostname**: `integ-assignment6.onrender.com` (no `https://`, no `/` at the end)  
4. Save → Render will redeploy automatically.

---

### Step 6 — Create admin user on Render (after first deploy works)

1. Open your web service on Render.  
2. Click **Shell** tab (on the left).  
3. Type these commands one at a time:

```bash
python manage.py createsuperuser
```
(Follow prompts: username, email, password)

```bash
python manage.py setup_rbac
```

```bash
python manage.py shell
```

In the Python shell, type (change `yourusername` to the username you just created):

```python
from django.contrib.auth.models import Group, User
user = User.objects.get(username="yourusername")
user.groups.add(Group.objects.get(name="album_admin"))
exit()
```

Now that user can open **Admin** in the navbar.

---

### Step 7 — Test the live site

Open your Render URL in Chrome.

Checklist:

- [ ] Home page loads  
- [ ] Sign up works  
- [ ] Create album works  
- [ ] Upload photo works (proves Cloudinary works)  
- [ ] Photo shows in the album  

If upload fails → double-check all three `CLOUDINARY_*` variables on Render.

---

## Part C — Submit to your class portal

### Step 8 — Fill in SUBMISSION.md

Open `SUBMISSION.md` in the project and replace:

1. **Live URL:** `https://YOUR-APP-NAME.onrender.com`  
2. **GitHub:** `https://github.com/ivandelmiguez-tech/Integ-Assignment6`

### Step 9 — Make one document for the teacher

Copy into Word or Google Docs:

- Your name: Jessie Paragas  
- Course / Assignment 6  
- Live application URL  
- GitHub repository URL  
- Short explanation (copy from SUBMISSION.md):
  - App uses Django CBVs for albums and photos  
  - RBAC: normal users vs `album_admin` group  
  - Photos stored on Cloudinary  
  - Database is PostgreSQL on Render  

Export as **PDF** and upload to the course portal before the deadline.

### Step 10 — Before grading day

Free Render apps **sleep** when nobody visits them. Open your live URL once so it wakes up before your teacher grades it.

---

## Quick troubleshooting

| Problem | Fix |
|---------|-----|
| `DisallowedHost` | Fix `ALLOWED_HOSTS` to match your `.onrender.com` address exactly |
| `Must supply api_key` | Add all 3 Cloudinary variables on Render |
| Build failed on `build.sh` | In Build Command use: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate --no-input && python manage.py setup_rbac` |
| Page very slow first load | Normal on free plan — wait 30 seconds |
| CSS looks broken | Build must run `collectstatic`; redeploy |

---

## Your links (fill in after deploy)

| Item | Link |
|------|------|
| GitHub | https://github.com/ivandelmiguez-tech/Integ-Assignment6 |
| Live site | https://________________.onrender.com |

---

## Assignment requirements — how this project meets them

| Requirement | Where it is in the project |
|-------------|----------------------------|
| Django CBVs | `albums/views.py` |
| RBAC | `albums/permissions.py` + `album_admin` group |
| Cloudinary | `settings.py` + env vars on Render |
| PostgreSQL | `DATABASE_URL` on Render |
| No hardcoded secrets | `.env` local only; Render env vars in production |
| README + requirements.txt | In repo root |

You are done when the live URL works and the submission document is uploaded.
