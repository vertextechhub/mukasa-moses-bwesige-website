# Mukasa Moses Bwesige — professional website

A Django website for professional information, documented work, publications, media and contact. The frontend uses Django templates, semantic HTML, custom responsive CSS and a small amount of vanilla JavaScript.

## Content integrity

Research documents and the source register are stored locally in the ignored `private_research/` directory. They are editorial source material, not public website content, and must not be committed or copied into served directories. Migrations populate the public profile, six source-linked work themes, bibliographic research records, institutional features, media entries and a dated reflection from the supplied sources. Contextual institutional resources may be listed with publisher attribution and explicit metadata limits when personal authorship is unverified; unresolved personal posts or appearances remain unpublished drafts. See the local `private_research/editorial_review.md` before publishing additional material.

Public content uses the requested name, links to original publishers, and distinguishes authored work from publisher features and acknowledged contributions. Dates are included only where a year or exact date is supported. The site does not assert unconfirmed qualifications, current roles, contact details or impact. Media placeholders are labelled, non-photographic spaces. No third-party media is downloaded or reproduced.

## Run locally or in GitHub Codespaces

Python 3.12 or later is recommended. In Codespaces, the included `.devcontainer/devcontainer.json` installs dependencies and applies migrations when the container is created.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Open the forwarded port 8000. The admin is at `/admin/`. The local default is SQLite and development mode; no `.env` file is committed. `DJANGO_SECRET_KEY` should be set to a unique random secret outside local development.

## Add and publish content

Use Django Admin to manage the professional profile, areas of work, publications and resources, media and speaking, insights, organisations, source references and contact messages. Relate each research, media or reflection record to its supporting themes and source references. Draft items are not visible publicly until **Is published** is enabled. Keep source URLs and attribution with each item. Use the year-only field when only a year is known rather than inventing a day or month. Scholarly records have separate journal, volume, issue and page-range fields; leave unavailable metadata blank. Admin image fields require descriptive alternative text.

The publications archive supports search and filters for record type, year, theme and publisher. The media archive supports search and filters for format, year, language, theme and publisher/organiser. Both use paginated results. Individual area pages collect their related publications, appearances and reflections. Public pages only query published content; records awaiting source or authorship checks remain drafts.

For recordings, choose English or Ukrainian where applicable. YouTube URLs may be configured as privacy-enhanced embeds; the visitor must explicitly load the video before a third-party request is made. Other media should link to its authorised original location. Images are stored under the untracked `media/` directory in local development.

The contact form has CSRF protection, server-side validation, a honeypot and a brief submission cooldown. Messages are stored in Django Admin and are not forwarded by email. Configure an email workflow separately if one is needed; no private contact details are embedded in the source.

## Configuration

Copy `.env.example` to `.env` and set environment variables in your shell/Codespaces secrets or deployment platform. Django does not automatically load `.env`; export the values in your environment or use your platform’s environment configuration.

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Secret key; set a unique, high-entropy value in deployment. |
| `DJANGO_DEBUG` | `True` for local development; set `False` in production. |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Comma-separated trusted origins including scheme, if required. |
| `DATABASE_URL` | Optional database URL. Omit it to use local SQLite; PostgreSQL is supported. |
| `SITE_URL` | Public canonical site origin, without a trailing slash. |
| `DJANGO_LOG_LEVEL` | Python logging level, default `INFO`. |

## Checks and tests

```bash
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
```

The automated tests cover the required pages, published-content visibility, generated slugs, media embed URL handling, contact validation, CSRF, the sitemap and robots endpoint.

## Production preparation

1. Set `DJANGO_DEBUG=False`, a private `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `SITE_URL`, and `DATABASE_URL` in the hosting environment.
2. Use PostgreSQL and run `python manage.py migrate`.
3. Run `python manage.py collectstatic`; WhiteNoise serves fingerprinted static assets.
4. Configure persistent/media object storage for uploaded portrait and media images. The default filesystem media storage is suitable for local development, not ephemeral application instances.
5. Run `python manage.py check --deploy` and resolve deployment-specific findings, including HTTPS, hostnames and trusted origins.
6. Back up the database and protect contact submissions as personal information.

No deployment has been performed as part of this implementation.
