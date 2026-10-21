#!/usr/bin/env just --justfile
export PATH := join(justfile_directory(), ".venv", "bin") + ":" + env_var('PATH')
export DJANGO_SETTINGS_MODULE := "config.settings.dev"

default:
    just --list

# upgrade lock file and sync changes
upgrade:
  uv lock --upgrade && uv sync

# make migrations
makemigrations:
    python manage.py makemigrations

# migrate
migrate:
    python manage.py migrate

check:
    python manage.py check


# runserver
run:
    python manage.py runserver


# generate admin.py for app
gen_admin app_name:
    python manage.py admin_generator  {{app_name}} 

# run check
test:
    python manage.py test

# squash migrations
squashmigrations app_label migration_name:
    python manage.py squashmigrations  {{app_label}} {{migration_name}}

shell:
    python manage.py shell

format:
    ruff format .

new_app app_name:
    genesis new backend apps/{{app_name}}

install_self:
    uv tool install --editable .

post-copy:
    [ -d .git ] || (git init && git add . && git commit -m 'chore: initial project setup' && git tag 0.0.1)
    [ -f .env ] || cp config/envs/.env.example.dev .env
    uv sync
    uv run python -m core.scripts.post_copy
    just makemigrations
    just migrate
    just format
    just test
    git rev-parse -q --verify refs/tags/setup-complete >/dev/null \
    || (git add -A && git commit -m "feat: Post Project Setup Commit" --allow-empty \
    && git tag setup-complete && git tag 0.1.0)

post-update:
    [ -f .env ] || cp config/envs/.env.example.dev .env
    uv sync
    uv run python -m core.scripts.post_update
    just makemigrations
    just migrate
    just format
    just test
