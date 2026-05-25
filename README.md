# Photo Album Management System

Production-ready Django application for managing photo albums with **Class-Based Views (CBVs)**, **Role-Based Access Control (RBAC)**, **Cloudinary** media storage, and **Render** deployment with **PostgreSQL**.

**Course:** IT363 — Assignment 6  
**Author:** Ivan Delmiguez

---

## Features

| Requirement | Implementation |
|-------------|----------------|
| CBVs for CRUD | `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView` for albums and photos |
| RBAC | Django auth + `album_admin` group; owners manage their albums; admins moderate all |
| Cloudinary | `django-cloudinary-storage` — no local `MEDIA_ROOT` in production |
| PostgreSQL | Via `DATABASE_URL` on Render (`dj-database-url`) |
| Secrets | `python-decouple` reads env vars — nothing sensitive in repo |

---

## Roles (RBAC)

| Role | Capabilities |
|------|----------------|
| **Standard user** | Register/login; create albums; upload/edit/delete own albums and photos; view public albums |
| **Album admin** (`album_admin` group) | All of the above plus manage **any** album/photo; access admin dashboard |
| **Superuser** | Django admin + same privileges as album admin |

Run once after deploy:

```bash
python manage.py setup_rbac
```

Assign a user to the admin group:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import Group, User
user = User.objects.get(username="admin_username")
user.groups.add(Group.objects.get(name="album_admin"))
```

---

## Local Development

### Prerequisites

- Python 3.11+
- (Optional) [Cloudinary](https://cloudinary.com) account for image uploads

### Setup

```bash
cd photo_album
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
copy .env.example .env         # Windows — edit values
python manage.py migrate
python manage.py setup_rbac
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

Without Cloudinary credentials, images save to `media/` locally (development only). In production (`DEBUG=false` + Cloudinary env vars), all uploads go to Cloudinary.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `true` locally, `false` on Render |
| `ALLOWED_HOSTS` | Comma-separated hosts, e.g. `your-app.onrender.com` |
| `DATABASE_URL` | PostgreSQL connection string (auto on Render) |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |

---

## Deploy to Render

**Beginner-friendly guide:** see **[DEPLOY_TUTORIAL.md](DEPLOY_TUTORIAL.md)** (step-by-step with screenshots-style instructions and every environment variable explained).

Quick summary:

1. Push this `photo_album` folder to a **public GitHub repository** (root = folder containing `manage.py`).
2. Create a [Cloudinary](https://cloudinary.com) account and note credentials.
3. On [Render](https://render.com):
   - **New → Blueprint** and connect the repo (uses `render.yaml`), **or**
   - **New → Web Service** → Python, root directory = repo root.
4. Set environment variables:
   - `DEBUG` = `false`
   - `ALLOWED_HOSTS` = `your-service-name.onrender.com`
   - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`
   - `DATABASE_URL` — link PostgreSQL database (Blueprint does this automatically).
5. **Build command:** `./build.sh`  
   **Start command:** `gunicorn photo_project.wsgi:application`
6. After first deploy, open the Render shell and run:
   ```bash
   python manage.py createsuperuser
   python manage.py setup_rbac
   ```
   Add your superuser to the `album_admin` group via shell (see above).

---

## Project Structure

```
photo_album/
├── albums/                 # Main app
│   ├── models.py           # Album, Photo
│   ├── views.py            # CBVs (CRUD + auth)
│   ├── permissions.py      # RBAC mixins
│   ├── forms.py
│   └── management/commands/setup_rbac.py
├── photo_project/          # Settings, URLs, WSGI
├── templates/
├── static/
├── requirements.txt
├── render.yaml
├── build.sh
└── README.md
```

---

## Submission Checklist

- [ ] Live Render URL
- [ ] GitHub repository link (with this README and `requirements.txt`)
- [ ] Single PDF/document: repo URL + live URL + brief documentation
- [ ] Render instance stays active during grading

---

## License

Educational project for course submission.
