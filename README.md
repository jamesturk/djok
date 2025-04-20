# DJOK: Django Starter Template

<https://git.unnamed.computer/jpt/djok>

This is our opinionated template for starting new Django projects.

It adds a few libraries useful for every Django project, with reasonable starting configurations.
Additionally, the repository has linting/CI rules and a project layout that has worked well for our many Django projects.

## License & Usage

This project is placed into the public domain ([CC0](https://creativecommons.org/public-domain/cc0/)) so you may use it however you see fit.

You can clone this repository and use it as a template, or pick & choose what you like and copy files as needed.

Attribution is appreciated but not required.

Please note that the underlying libraries are under their own (MIT/BSD) licenses.

## Getting Started

To make full usage of this you will need to install

- `uv` - <https://docs.astral.sh/uv/getting-started/installation/>
- `just`
   - You can run `just` using `uv` if you wish:
      - `uvx --from rust-just just` for a one-off run
      - `uv tool install just` for a permanent installation


If you are using this library as a baseline, there are a few steps you'll need to follow:

1. Read through the various sections below to familiarize yourself with the setup.
   A few of the libraries may require additional setup, documented under the **You:** steps below.
2. Before starting, you will need to choose which kind of user account you want. See `DJOK_USER_TYPE` below.
3. Replace this README & the LICENSE file with those appropriate to your project.
   (**Caution**: Since this repository is licensed CC-0, failure to do so would mean licensing your code in the same way, likely not what you want.)
4. Open pyproject.toml & replace "djok" with your project name.
5. **Recommended:** run `uv run pre-commit install`

## File System Layout

- `apps/` - Create your app(s) in this directory.
- `apps/accounts/` - An app that defines our custom user model, compatible with `allauth` and `django.contrib.admin`.
- `config/` - This directory is the Django "project". It contains settings files as well as your root `urls.py`.
- `static/` - This directory is where you will place your static CSS, images, and JS. Those files will be served via `whitenoise`.
- `static/root/` - This directory will be served as-is at the root of your application. It is useful for files like `robots.txt` that need to be in a particular place.
- `static/root/robots.txt` - A default robots.txt is provided that excludes troublesome AI bots. (via https://github.com/ai-robots-txt/ai.robots.txt/blob/main/robots.txt)
)
- `templates/` - Django is configured to search this directory for your templates. You can also put templates within `<appdir>/templates/` for any given app, but this layout keeps them all together.
- `templates/account/` - For your convinience, the default auth templates provided by `django-allauth`. Replace or modify these.

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

**We:** Provide several configurations.

**You:** Select one by setting `DJOK_USER_TYPE`.

#### DJOK_USER_TYPE

Should be set to either:

- `username` - Standard username/password login w/ optional email.
- `email` - Standard email/password login, username is set to email.
            Comes with allauth-powered token-based login as well.
- `email+username` - Email-based with optional username field for display
                     purposes.

This must be set **before** running initial DB migrations.

Once set, you can run:

```shell
just dj makemigrations accounts
just dj migrate
```

Changing once the application is live will require careful planning and custom data migration.

#### DJOK_PASSWORD_PROMPTS

Determines how many password inputs are shown.

- 0 - Email/Token based login.
- 1 - Single password input.
- 2 - Password input with confirmation.

#### Webauthn

See the comments in `config/settings.py` to enable signup & login via Webauthn.

