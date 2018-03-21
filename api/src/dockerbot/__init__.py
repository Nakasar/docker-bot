# Initialisation of dockerbot package
import docker
import sys

client = docker.from_env()

__all__ = ["containers", "images", "logs"]

def log(string):
    print(string, file=sys.stderr)
