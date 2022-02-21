import environs
import os


def create_env():
    dotenv = environs.Env()
    return dotenv


def load_env(envs):
    """Load enviroment from given file or dict."""
    if isinstance(envs, dict):
        os.environ.update(envs)
    elif isinstance(env, str) and os.path.isfile(envs):
        env.read_env(envs)


def config_class(environment):
    """Link given environment to a config class."""
    return f"{__package__}.config.{environment.capitalize()}Config"


# the application environment
env = create_env()
