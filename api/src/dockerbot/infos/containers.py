def listContainers():
    """
    Gets list of running containers in current docker client.

    Parameters
    ----------

    Returns
    -------
    [Container]
        List of Container objects
    """
    global client
    try:
        containers = client.containers.list()
        response = []
        for container in containers:
            response.append("**{0}** ({1})".format(container.name, container.id))
        return response
    except:
        return []


def detailContainer(containerId):
    global client
    return {}
