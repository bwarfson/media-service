import getpass
import os
from pathlib import Path

from git import Repo

import cdk.media_service.constants as constants


def get_username() -> str:
    try:
        return getpass.getuser().replace('.', '-')
    except Exception:
        return 'github'


def get_stack_name() -> str:
    repo = Repo(Path.cwd())
    username = get_username().lower()
    cicd_environment = os.getenv('ENVIRONMENT', 'dev').lower()
    try:
        branch_name = f'{repo.active_branch}'.replace('/', '-').replace('_', '-').lower()
        return f'{username}-{branch_name}-{constants.SERVICE_NAME}-{cicd_environment}'
    except TypeError:
        # we're running in detached mode (HEAD)
        # see https://github.com/gitpython-developers/GitPython/issues/633
        return f'{username}-{constants.SERVICE_NAME}-{cicd_environment}'


def get_construct_name(stack_prefix: str, construct_name: str) -> str:
    return f'{stack_prefix}-{construct_name}'[0:64]
