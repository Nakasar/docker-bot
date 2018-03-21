import docker
from datetime import datetime
import sys

client = docker.from_env()

def listLogs(container_name, limit, error, since, until):
    """
    Get the logs of a container given its name

    Parameters
    ----------
    [container_name]
        The name of the container
    [limit]
        The max count of log send
    [error]
        Tells if you want stderr logs
    [since]
        show logs since 'since'

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
                data = {
                    'title':'LOGS -- ' + container.name,
                    'message': "\n".join(str(container.logs(
                        stdout=True,
                        stderr=error,
                        since=datetime.strptime(since, '%m-%d/%H:%M:%S').replace(year=datetime.now().year),
                        until=datetime.strptime(until, '%m-%d/%H:%M:%S').replace(year=datetime.now().year)
                    ), 'utf-8').split('\n')[:limit])
                } if since != None else {
                    'title':'LOGS -- ' + container.name,
                    'message': "\n".join(str(container.logs(
                        stdout=True,
                        stderr=error
                    ), 'utf-8').split('\n')[:min(max(15, limit), 50)])
                }
                return { "success":True, "data": data }
        return { "success":False, "code":"LOG-01" }
    except:
        return { "success":False, "code":"LOG-00" }
