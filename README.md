# Backend

## Style guide

Below guides are used whenever possible. PS: they are useful for any django project, so feel free to explore them

-   https://github.com/HackSoftware/Django-Styleguide
-   https://danpalmer.me/2018-03-02-scaling-django-codebases/
-   https://www.youtube.com/@bugbytes3923 (Amazing channel for deep Django concepts)

## Setup environment

-   Run: `scripts/setup.sh --env <dev|prod> --python_alias <python_command>`
-   Example: `scripts/setup.sh --env dev --python_alias python`
-   To create a superuser: `python manage.py createsuperuser`

## Important Things

-   Python 3.11
-   Postgres is used (version 14.19 is used), but should be compatible with higher versions as well

## Folder Structure

Inside `backend-election-candidates/`

## User model

-   Inherits `django.contrib.auth.models.AbstractBaseUser` and `utils.core.base_models.BaseModel`
-   Its `CustomBaseUserManager` inherits `django.contrib.auth.models.BaseUserManager` and `safedelete.managers.SafeDeleteManager`

### apps/

-   `core`
-   `users`

### electionsys/

-   contains `settings/` folder

### requirements/

-   contains `base.txt`, `dev.txt` and `prod.txt` files
-   to install dependencies run `pip install -r requirements/dev.txt`

## Notes

### Creating a new app:

1. `cd apps`
2. `django-admin startapp <app_name>`
3. Go to `<app_name>/apps.py`
4. Change name `apps.<app_name>` in the `<app_name>Config` class
5. Add app to LOCAL_APPS in settings.py denoting by `apps.<app_name>`

### Abbreviations

-   IMP: Important (to be implemented before deployment)
-   CRITICAL: Critical (to be implemented before deployment, will break the system)
-   NOTE: Note (for general advice, clarifications, or guidance for future development.)
-   INFO: Info (for informational comments that provide context or references for future developers, but aren’t as urgent as notes or important tasks)
-   DEPRECATED: Deprecated (to be removed in the future)
-   HACK: Used to indicate a temporary or not-ideal solution that needs to be revisited and improved.
-   FIXME: Used to indicate a problem that needs to be fixed, but hasn’t been fixed yet.
-   TODO: Used to indicate a task that hasn’t been completed yet.

### Formatter

-   [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) is used for formatting (install the vscode extension and enable format on save)

### soft delete

-   [django-safedelete](https://pypi.org/project/django-safedelete/) is used for soft delete
-   See `utils/core/base_models.py`

### DJANGO_DEBUG

-   Set it using `export DJANGO_DEBUG="True"` (or False)
-   If it is True, .env file will be used, else .env.prod will be used.

### Commands

-   `python manage.py <command>`

### setup_server

-   see `apps/core/management/commands/setup_server.py`

### exception handler

-   see `utils/core/exception_handler.py`
-   handles most of the exceptions so you can directly raise exceptions anywhere and they'll be properly formatted and sent to FE

### Miscellaneous

#### Postman API Collection

-   https://www.postman.com/grey-water-468124/workspace/open-source-nepal-backend-django
