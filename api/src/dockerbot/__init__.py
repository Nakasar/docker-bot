# Initialisation of dockerbot package
import docker

client = docker.from_env()

__all__ = ["containers", "images", "logs"]
