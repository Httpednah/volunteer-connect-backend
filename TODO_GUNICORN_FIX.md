# TODO - Fix Gunicorn Deployment Issue

## Fix runtime.txt - Use Python 3.9 (without patch version)

- [x] Update runtime.txt from `python-3.9.20` to `python-3.9`

## Fix Pipfile - Match Python version

- [x] Update Pipfile python_version from `3.8` to `3.9`

## Update RENDER_DEPLOYMENT.md - Add troubleshooting

- [x] Add "Gunicorn Not Found" troubleshooting section
- [x] Document the fix for build issues

## Fix Procfile - Use Python module execution

- [x] Change Procfile from `gunicorn app:app --preload` to `python -m gunicorn app:app --preload --bind 0.0.0.0:$PORT`
- [x] Update RENDER_DEPLOYMENT.md with new Start Command

## Fix Import Issues

- [x] Fix routes.py imports (import db from extensions, not models)
- [x] Register payments_bp blueprint in app.py

## Create Build Script

- [x] Create build_render.sh to verify gunicorn installation
- [x] Update Procfile to use build script

## Re-deploy to Render

- [ ] Push changes to GitHub
- [ ] Trigger new deployment on Render
- [ ] Verify gunicorn starts correctly
