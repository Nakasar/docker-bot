import docker

client = docker.from_env()

def listContainers():
    """
    Gets list of running containers in current docker client.

    Parameters
    ----------

    Returns
    -------
    [String]
        List of Container names and id "**c.name** c.id"
    """
    try:
        containers = client.containers.list()
        response = []
        for container in containers:
            response.append("**{0}** ({1})".format(container.name, container.id))
        return response
    except:
        return []


def detailContainer(containerId):
    return {}
