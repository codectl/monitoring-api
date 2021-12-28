import environs


def create_env():
    """Create an env from local .env."""
    dotenv = environs.Env()
    dotenv.read_env()
    return dotenv


# the env
env = create_env()
