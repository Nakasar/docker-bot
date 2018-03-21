from . import client, log


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
        containersList = client.containers.list()
        response = []
        for container in containersList:
            response.append("**{0}** ({1})".format(container.name, container.id))
        return response
    except:
        return []


def process(container_name):
    """
    Get the running process of the given container if found.

    Parameters
    ----------
    string
        container_name -> the name of the container.

    Returns
    -------
    set
        success: bool -> True if image is up and running, False otherwise.
        code: String -> Error code : INF- 00 = unkown error, 22 = no container with this name.
        message: String -> Message to display to user.
    """
    try:

        container = client.containers.get(container_name)
        try:
            processList = container.top()
            result = ""
            for process in processList["Processes"]:
                result += "\n> *{}* \n".format(process[7])
                result += "UID: {}\n".format(process[0])
                result += "PID: {}\n".format(process[1])
                result += "PPID: {}\n".format(process[2])
                result += "C: {}\n".format(process[3])
                result += "STIME: {}\n".format(process[4])
                result += "TTY: {}\n".format(process[5])
                result += "TIME: {}\n".format(process[6])
                result += "\n"
            return {"success": True, "message": result, "name": container_name}
        except:
            return {"success": False, "code": "INF-00", "message": "Could not get list of process for this container.", "name": container_name}
    except:
        return {"success": False, "code": "INF-22", "message": "No container running with this name.", "name": container_name}
    return {}


def kill(container_name):
    """
    Tries to stop the container with the given name.

    Parameters
    ----------
    string
        container_name -> the name of the container to stop.

    Returns
    -------
    set
        success: bool -> True if image is up and running, False otherwise.
        code: String -> Error code : ADM- 00 = unkown error, 02 = no container with this name, 06 = container not stoppable.
        message: String -> Message to display to user.
    """
    try:
        container = client.containers.get(container_name)
        try:
            container.remove(force=True)
            return {"success": True, "message": "Container `{0}` killed and **removed**.".format(container_name), "name": container_name}
        except:
            return {"success": False, "code": "ADM-06", "message": "Container not stoppable.", "name": container_name}
    except:
        return {"success": False, "code": "ADM-02", "message": "No container running with this name.", "name": container_name}
