import docker

client = docker.from_env()

def listLogs(container_name, limit=-1):
    """
    Get the logs of a container given its name

    Parameters
    ----------
    [container_name]
        The name of the container
    [limit]
        The max count of log send

    Returns
    -------
    [logs]
        List of logs
    """

    try:
        for container client.containers.list():
            if (container.name == container_name):
                return str(container.logs(stdout=True, stderr=True)).split('\\n')[:limit]
    except:
        return []
