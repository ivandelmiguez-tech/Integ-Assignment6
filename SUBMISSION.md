# Assignment 6 — Submission Document

**Student:** Ivan Delmiguez  
**Course:** IT363  
**Project:** Production-Ready Django Photo Album Management System

---

## 1. Live Application URL

`https://________________.onrender.com`

*(Replace after deploying to Render.)*

---

## 2. Source Code Repository

https://github.com/ivandelmiguez-tech/Integ-Assignment6

---

## 3. Project Documentation

### Architecture Overview

The application is a Django 4.2 project (`photo_project`) with a single domain app (`albums`). All user-facing CRUD operations use **Class-Based Views**. Security is enforced through **Django authentication**, custom permission mixins, and the **`album_admin`** group for role-based access control.

### Technical Stack

| Component | Technology |
|-----------|------------|
| Framework | Django 4.2 (Python) |
| Database (production) | PostgreSQL on Render |
| Media storage | Cloudinary (`django-cloudinary-storage`) |
| Deployment | Render (Gunicorn + WhiteNoise) |
| Configuration | Environment variables via `python-decouple` |

### RBAC Design

- **Standard users:** Authenticated users who create and manage their own albums and photos. They can view albums marked public or owned by themselves.
- **Album administrators:** Members of the `album_admin` Django group (created by `python manage.py setup_rbac`). They can view, edit, and delete any album or photo and access the admin dashboard at `/admin-dashboard/`.
- **Superusers:** Full Django admin access plus album admin capabilities.

### CRUD Operations (CBVs)

| Resource | List | Detail | Create | Update | Delete |
|----------|------|--------|--------|--------|--------|
| Album | `AlbumListView` | `AlbumDetailView` | `AlbumCreateView` | `AlbumUpdateView` | `AlbumDeleteView` |
| Photo | (in album detail) | — | `PhotoCreateView` | `PhotoUpdateView` | `PhotoDeleteView` |

### Cloud Storage

In production (`DEBUG=false`, `USE_SQLITE=false`), `DEFAULT_FILE_STORAGE` is set to `MediaCloudinaryStorage`. Local `MEDIA_ROOT` is not used for serving uploads in production.

### Deployment Notes

Environment variables on Render: `SECRET_KEY`, `DEBUG=false`, `USE_SQLITE=false`, `ALLOWED_HOSTS`, `DATABASE_URL`, and all three `CLOUDINARY_*` variables. See **`DEPLOY_TUTORIAL.md`** for a beginner-friendly deploy guide.

---

## 4. Grading Checklist

- [x] Django CBVs for album and photo CRUD
- [x] RBAC with Django auth and `album_admin` group
- [x] Cloudinary integration (production)
- [x] PostgreSQL via Render `DATABASE_URL`
- [x] No hardcoded secrets in repository
- [x] `README.md` and `requirements.txt` included
- [ ] Live Render URL (complete after deploy)
- [x] GitHub repository published
