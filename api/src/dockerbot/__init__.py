# Initialisation of dockerbot package
import docker
import recastai
import sys

client = docker.from_env()
recast = recastai.Client('ffde2e6e88745852df01e71e55e60e81', 'en')

__all__ = ["containers", "images", "logs", "nlp"]

def log(string):
    print(string, file=sys.stderr)
