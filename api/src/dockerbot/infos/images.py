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
        print(images, file=sys.stderr)
        response = []
        for image in images:
            print(image, file=sys.stderr)
            print(image.tags, file=sys.stderr)
            for tag in image.tags:
                print(tag, file=sys.stderr)
                response.append("**{0}**".format(tag))
        print(response, file=sys.stderr)
        return response
    except:
        return []
