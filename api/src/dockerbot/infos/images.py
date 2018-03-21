import docker
client = docker.from_env()
import sys

def listImages():
    """
    Get list available images on current docker client.

    Parameters
    ----------

    Returns
    -------
    [String]
        List of image names ""**i.name**
    """
    try:
        images = client.images.list()
        response = []
        for image in images:
            for tag in image.tags:
                response.append("**{0}**".format(tag))
        return response
    except:
        return []

