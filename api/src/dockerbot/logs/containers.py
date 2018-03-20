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
        status : success or error
        List of logs if success else error code
    """

    try:
        containers = client.containers.list()
        for container in containers:
            if (container.name == container_name):
                data = { 'title':'LOGS -- ' + name, 'message': str(container.logs(stdout=True, stderr=True)).split('\\n')[:limit] }
                return { "success":True, "data": data }
        return { "success":False, "code":"LOG-01" }
    except:
        return { "success":False, "code":"LOG-00" }
