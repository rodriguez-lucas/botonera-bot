import os

ENVIRONMENT_VARIABLES = {}

REQUIRED_ENVIRONMENT_VARIABLES = [
    'DATABASE_URL',
    'DJANGO_SECRET_KEY',
    'GET_SOUND_URL',
    'BOT_TOKEN',
]


def check_and_load_required_environment_variables():
    unset_env_vars = []

    for env_var in REQUIRED_ENVIRONMENT_VARIABLES:
        if env_var not in os.environ:
            unset_env_vars.append(env_var)
        else:
            ENVIRONMENT_VARIABLES[env_var] = os.environ.get(env_var)

    if unset_env_vars:
        raise Exception('These env variables were not set: {}'.format(unset_env_vars))


check_and_load_required_environment_variables()
