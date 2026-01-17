# Render Deployment Guide for Volunteer Connect

## Pre-Deployment Checklist

✅ **Files Created/Modified:**

- `config.py` - Updated to use environment variables for PostgreSQL
- `app.py` - Uses Config class for all settings
- `requirements.txt` - Added `gunicorn` and `psycopg2-binary`
- `Procfile` - Tells Render how to run the app with Gunicorn
- `runtime.txt` - Specifies Python 3.9
- `.env.example` - Template for environment variables

## Deployment Steps on Render

### 1. Create a New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:

| Setting        | Value                                                                               |
| -------------- | ----------------------------------------------------------------------------------- |
| Name           | volunteer-connect-api                                                               |
| Root Directory | (leave empty)                                                                       |
| Build Command  | `pip install -r requirements.txt --no-cache-dir`                                    |
| Start Command  | `bash build_render.sh && python -m gunicorn app:app --preload --bind 0.0.0.0:$PORT` |
| Runtime        | Python 3                                                                            |

### 2. Set Environment Variables

In the Render dashboard, go to the "Environment" tab and add:

| Key            | Value                                                                             |
| -------------- | --------------------------------------------------------------------------------- |
| `DATABASE_URL` | (Render will provide this automatically for PostgreSQL)                           |
| `SECRET_KEY`   | Generate a secure key: `python -c "import secrets; print(secrets.token_hex(32))"` |

> **Note:** Render automatically creates a PostgreSQL database and sets `DATABASE_URL` when you enable it in the settings.

### 3. Enable PostgreSQL Database

1. In the web service settings, scroll to "Databases"
2. Click "Create Database"
3. Select "PostgreSQL" and your preferred plan (Free tier available)
4. Render will automatically set the `DATABASE_URL` environment variable

### 4. Deploy

1. Click "Create Web Service"
2. Render will build and deploy your app
3. Watch the logs for any errors

## First-Time Setup (After Deployment)

After the first deployment, you'll need to initialize the database:

1. Open a shell in Render (via the Dashboard or Render CLI)
2. Run migrations:
   ```bash
   flask db upgrade
   ```
3. Seed the database (optional):
   ```bash
   python seed.py
   ```

## Local Development

To run locally with SQLite (development):

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

To test with PostgreSQL locally:

```bash
# Create a .env file
cp .env.example .env

# Edit .env with your local PostgreSQL URL
# DATABASE_URL=postgresql://user:password@localhost:5432/volunteer_connect

# Run the app (will use PostgreSQL)
python app.py
```

## Troubleshooting

### Gunicorn Not Found (Exit Status 127)

If you see this error:

```
bash: line 1: gunicorn: command not found
==> Exited with status 127
```

**Solution:**

1. **Use Python module execution** (Recommended):

   ```
   # In Procfile, use:
   web: python -m gunicorn app:app --preload --bind 0.0.0.0:$PORT
   ```

   This ensures Python finds gunicorn even if it's not in the system PATH.

2. **Use build script** (Most reliable):

   ```
   # In Procfile, use:
   web: bash build_render.sh && python -m gunicorn app:app --preload --bind 0.0.0.0:$PORT
   ```

   The `build_render.sh` script ensures gunicorn is properly installed and verified before starting the app.

3. **Check Python version consistency**: Ensure `runtime.txt` specifies `python-3.9` (not a specific patch version like `python-3.9.20`)

4. **Verify requirements.txt contains gunicorn**:

   ```
   gunicorn==23.0.0
   ```

5. **Add --no-cache-dir to build command** to ensure clean installation:

   ```
   pip install -r requirements.txt --no-cache-dir
   ```

6. **Rebuild on Render**: Trigger a new deployment after making these changes

### Database Connection Errors

- Ensure `DATABASE_URL` is set correctly
- For PostgreSQL, the URL must start with `postgresql://` not `postgres://`
- The config.py handles this conversion automatically

### Migration Issues

If you need to create initial migrations:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### CORS Errors

The app is configured to allow all origins (`CORS(app)`). For production, consider restricting this to your frontend domain.

## Project Structure

```
volunteer-connect-backend/
├── app.py              # Main Flask application
├── config.py           # Configuration with env variable support
├── extensions.py       # SQLAlchemy extension
├── models.py           # Database models (User, Organization, etc.)
├── routes.py           # Additional route blueprints
├── seed.py             # Database seeding script
├── build_render.sh     # Build script for Render deployment
├── requirements.txt    # Python dependencies
├── Procfile            # Render deployment config
├── runtime.txt         # Python version
└── .env.example        # Environment variable template
```

## API Endpoints

| Method | Endpoint              | Description          |
| ------ | --------------------- | -------------------- |
| GET    | `/`                   | Health check         |
| POST   | `/register`           | Register new user    |
| POST   | `/login`              | User login           |
| GET    | `/organizations`      | List organizations   |
| POST   | `/organizations`      | Create organization  |
| GET    | `/opportunities`      | List opportunities   |
| POST   | `/opportunities`      | Create opportunity   |
| PATCH  | `/opportunities/<id>` | Update opportunity   |
| DELETE | `/opportunities/<id>` | Delete opportunity   |
| POST   | `/applications`       | Apply to opportunity |
| POST   | `/payments`           | Record payment       |
