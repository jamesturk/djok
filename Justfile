
lint:
    uv run pre-commit run --all-files

test *ARGS:
    uv run pytest {{ARGS}}

reset:
    rm -rf _logs/*
    rm -rf _staticfiles
    rm -rf db.sqlite3
    uv run python manage.py migrate
    uv run python manage.py createsuperuser

runserver *ARGS:
    uv run python manage.py runserver {{ARGS}}

# run arbitrary django commands
dj *ARGS:
    uv run python manage.py {{ARGS}}
