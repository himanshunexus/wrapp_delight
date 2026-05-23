# Admin Credentials & Bootstrap

## Current Admin Account

**Bootstrap credentials for the deployed admin account:**

- **Username**: set with `ADMIN_BOOTSTRAP_USERNAME` (defaults to `admin`)
- **Password**: set with `ADMIN_BOOTSTRAP_PASSWORD`
- **Email**: set with `ADMIN_BOOTSTRAP_EMAIL` (defaults to `admin@example.com`)

### What This Means

These credentials are read by:
- `delights_backend/core/store/management/commands/ensure_admin_user.py`

They are enforced at every application startup via the `ensure_admin_user` management command.

## Bootstrap Process

### On Render (Production)

The startup sequence in `render.yaml`:

1. Create media directory
2. Run database migrations
3. **Run `ensure_admin_user` command** — enforces the configured admin account
4. Start Gunicorn

**Result**: Admin account is created/updated with the credentials from environment variables.

### Locally (Development)

Same flow when you run:

```bash
cd delights_backend/core
python manage.py migrate
python manage.py ensure_admin_user
python manage.py runserver
```

Or if migrations/bootstrap fail to run:

```bash
python manage.py ensure_admin_user --verbosity 2
```

## Login URLs

### Custom Dashboard (Admin Interface)

- **URL**: `http://localhost:8000/login/?next=/dashboard/` (local)
- **URL**: `https://wrappdelights.onrender.com/login/?next=/dashboard/` (production)
- **Username**: configured with `ADMIN_BOOTSTRAP_USERNAME`
- **Password**: configured with `ADMIN_BOOTSTRAP_PASSWORD`

The login form accepts either case for the username because `CaseInsensitiveAuthenticationForm` is used.

### Django Admin (if needed)

- **URL**: `http://localhost:8000/control-room-admin/` (local, default)
- **URL**: `https://wrappdelights.onrender.com/control-room-admin/` (production, default)
- **Path can be customized** via env var: `ADMIN_PANEL_PATH=your-secret-path/`

Same configured credentials as above.

## Environment Variables Required

The admin account depends on `ADMIN_BOOTSTRAP_*` environment variables.

`ADMIN_BOOTSTRAP_PASSWORD` must be set before running `ensure_admin_user`.

If you need to change credentials, you must:

1. Update the `ADMIN_BOOTSTRAP_*` environment variables
2. Redeploy (Render will run the command at startup)

Or manually in the Django shell:

```bash
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> U = get_user_model()
>>> u = U.objects.get(username='admin')
>>> u.set_password('new-password-here')
>>> u.save()
```

## Summary

- **Single source of truth**: Environment variables read by `ensure_admin_user.py`
- **Enforced at startup**: Every boot, the command ensures the configured admin exists
- **Environment-driven**: No password is committed to source control
- **Case-insensitive login**: Username matching is flexible on the login form

If login fails, the most common reasons:

1. **Wrong password** — Double-check the literal string above, character for character
2. **Admin account not created** — Run `python manage.py ensure_admin_user` manually
3. **Stale session/cache** — Open a fresh incognito tab and try again
