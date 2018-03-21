from datetime import datetime

from . import client

def listLogs(container_name, limit=-1, error=False, since='01-01/00:00:00', until='12-31/00:00:00'):
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
        container = client.containers.get(container_name)
        data = {
            'title':'LOGS : ' + container.name,
            'message': "\n".join(str(container.logs(
                stdout=True,
                stderr=True,
                since=datetime.strptime(since, '%m-%d/%H:%M:%S').replace(year=datetime.now().year),
                until=datetime.strptime(until, '%m-%d/%H:%M:%S').replace(year=datetime.now().year)
            ), 'utf-8').split('\n')[:limit])
        } if since != None else {
            'title':'LOGS -- ' + container.name,
            'message': "\n".join(str(container.logs(
                stdout=True,
                stderr=True
            ), 'utf-8').split('\n')[:limit])
        }
        return { "success":True, "data": data } if not(error) else { "success":True, "data": {
            'title':data.title,
            'message': [ e for e in data.message if 'error' in e.lower() ]
            } }
    except:
        return { "success":False, "code":"LOG-01" }
