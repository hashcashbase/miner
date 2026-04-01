import os


def set_env_variable(key, value):
    """Update or add a key=value pair in the .env.local file."""
    lines = []
    updated = False
    if os.path.exists('.env.local'):
        with open('.env.local', 'r') as f:
            lines = f.readlines()

    with open('.env.local', 'w') as f:
        for line in lines:
            if line.startswith(f'{key}='):
                f.write(f'{key}={value}\n')
                updated = True
            else:
                f.write(line)
        if not updated:
            f.write(f'{key}={value}\n')


def get_env_variable(key, default=None):
    """Get environment variable from the system or return default."""
    return os.getenv(key, default)