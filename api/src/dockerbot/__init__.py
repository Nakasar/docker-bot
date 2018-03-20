# Initialisation of dockerbot package
import docker

# Load all subpackages
__all__ = ["admin", "infos", "logs"]

client = docker.from_env()
