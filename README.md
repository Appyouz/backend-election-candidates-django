# Backend

## Style guide

Below guides are used whenever possible. PS: they are useful for any django project, so feel free to explore them

-   https://github.com/HackSoftware/Django-Styleguide
-   https://danpalmer.me/2018-03-02-scaling-django-codebases/
-   https://www.youtube.com/@bugbytes3923 (Amazing channel for deep Django concepts)

## Important Things

-   Python 3.11
-   Postgres is used (version 14.19 is used), but should be compatible with higher versions as well

## Folder Structure

Inside `backend-election-candidates/`

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

-   Black is used for formatting (install the vscode extension and enable format on save)

### soft delete

-   [django-safedelete](https://pypi.org/project/django-safedelete/) is used for soft delete
-   See `utils/core/base_models.py`

### DJANGO_DEBUG

-   Set it using `export DJANGO_DEBUG="True"` (or False)
-   If it is True, .env file will be used, else .env.prod will be used.

### Commands

-   `python manage.py <command>`

#### seed_data

-   see `apps/core/management/commands/seed_data.py`
-   NOTE: `created_by` and `updated_by` will be set to null

#### create_stock_item_if_not_exists

-   see `apps/core/management/commands/create_stock_item_if_not_exists.py`

#### setup_server

-   see `apps/core/management/commands/setup_server.py`

### Miscellaneous
