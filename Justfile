
lint:
    uv run pre-commit run --all-files

test *ARGS:
    uv run pytest {{ARGS}}

runserver *ARGS:
    uv run python manage.py runserver {{ARGS}}

# run arbitrary django commands
dj *ARGS:
    uv run python manage.py {{ARGS}}
