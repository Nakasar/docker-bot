from datetime import datetime

from . import client

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
    [until]
        show logs until 'until'

    Returns
    -------
    [logs]
        status : success or error
        List of logs if success else error code
    """
    try:
        container = client.containers.get(container_name)
        data = {
            'title':'LOGS : ' + container.name,
            'message': "\n".join([ e for e in str(container.logs(
                stdout=True,
                stderr=True,
                since=datetime.strptime(since, '%m-%d/%H:%M:%S').replace(year=datetime.now().year),
                until=datetime.strptime(until, '%m-%d/%H:%M:%S').replace(year=datetime.now().year)
            ), 'utf-8').split('\n')[:limit] if 'error' in e.lower() or not(error) ])
        }
        return { "success":True, "data": data }
    except:
        return { "success":False, "code":"LOG-01" }
