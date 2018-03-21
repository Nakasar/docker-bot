import docker
client = docker.from_env()


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