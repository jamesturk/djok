# Django Starter Template

This is our opinionated template for starting new Django projects.

It adds a few libraries useful for every Django project, with reasonable starting configurations.
Additionally, the repository has linting/CI rules and a project layout that has worked well for our many Django projects.

## License

This project is placed into the public domain ([CC0](https://creativecommons.org/public-domain/cc0/)) so you may use it however you see fit.

You can clone this repository, use it as a template, or pick & choose what you like. Attribution is appreciated but not required.

Please note that the underlying libraries are under their own (MIT/BSD) licenses.

## Getting Started

If you are using this library as a baseline, there are a few steps you'll need to follow:

1. Replace all instances of "djeff" with your project name.
2. Add a LICENSE
3. run `uv run pre-commit install`
4. Read through the various sections below to familiarize yourself with the setup.
   A few of the libraries may require additional setup, documented under the **You:** steps below.

## File System Layout

- `config/` - This directory is the Django "project". It contains settings files as well as your root `urls.py`.
- `static/` - This directory is where you will place your static CSS, images, and JS. Those files will be served via `whitenoise`.
- `static/root/` - This directory will be served as-is at the root of your application. It is useful for files like `robots.txt` that need to be in a particular place.
- `static/root/robots.txt` - A default robots.txt is provided that excludes troublesome AI bots. (via https://github.com/ai-robots-txt/ai.robots.txt/blob/main/robots.txt)
)
- `templates/` - Django is configured to search this directory for your templates. You can also put templates within `<appdir>/templates/` for any given app, but this layout keeps them all together.

Additionally, there are two directories that you will see after running your application. These are `.gitignore`d.

- `_staticfiles` - Where Django will store the combined static files for serving. Do not modify files in this directory directly, instead modify the copies in `static`.
- `_logs` - The default destination of the log files, can be modified in `config/settings.py`.

## Tool Choices

- `ruff` - Ensure code quality.
- `uv` - Manage packages.
- `pre-commit` - Enforce repository standards.
- `just` - Run common tasks.

## Django Plugins/Apps

### django-environ

Configure Django projects using environment variables, per [The Twelve-Factor App](https://www.12factor.net).

**We:** Configured per typical instructions & used in `config/settings.py`.

**You:** Ensure any future configurable settings are added as environment variables as seen in that file.

<https://django-environ.readthedocs.io/en/latest/>

### whitenoise

Efficiently serve static files alongside your application.

**We:** Configured per typical instructions to be used in conjunction with Django's `staticfiles`.

**You:** Put your static files in `static/` & files that you need served at the root of your domain (like `robots.txt`) in `static/root`.

<https://whitenoise.readthedocs.io/en/latest/>

### django-typer

Allows writing Django management commands using `typer`.

**We:** Configured per typical instructions.

**You:** Write new management commands as needed using typer.

<https://django-typer.readthedocs.io/en/stable/>

### pytest-django

Allows writing Django tests using simplified `pytest`-style tests. Provides fixtures & other test helpers.

**We:** Configured per typical instructions.

**You:** Write `pytest`-style Django tests. Can run them with `pytest` (or `just test`).

<https://pytest-django.readthedocs.io/en/latest/>

### django-debug-toolbar

Provides an in-browser interface for inspecting Django views.

**We:** Configured per typical instructions, set up to automatically enable when `DEBUG` is true.

**You:** Enjoy increased visibility into database queries, template issues, etc.

<https://django-debug-toolbar.readthedocs.io/en/latest/>

### django-structlog

This library integrates [structured logging](https://www.structlog.org/en/stable/) with Django.

**We:** Provided default configuration that writes logs to the `logs/` directory.

**You:** Modify the `LOGGING` config to reflect your application's name and desired log levels/types.

<https://django-structlog.readthedocs.io/en/latest/>

### django-allauth

Augment's django's built in `auth` with commonly-needed views for signup, email confirmation, etc.

**We:** Configured for email login.

**You:** Review settings & ensure that they meet your application's login needs.

