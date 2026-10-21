import os
import django


def setup_django(settings_module="base", is_notebook=False):
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", f"config.settings.{settings_module}"
    )
    if is_notebook:
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    django.setup()
