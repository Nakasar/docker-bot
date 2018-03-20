import docker
client = docker.from_env()

def run(image):
    """
    Tries to recover the given image in cache, otherwise looks into docker repos.

    Parameters
    ----------
    string
        image -> the name of the image to run.
    """
    try:
        # Search for image in local cache
        foundImage = client.images.get(image)
        try:
            # Run image
            container = client.containers.run(foundImage, detach=True)
            message = "Image `{}` up and running into `{}`.".format(foundImage.tags[0], container.name)
            return {"success": True, "message": message}
        except:
            # Unable to run image, or an error occured in some process
            return {"success": False, "code": "ADM-05", "message": "Unable to run image pulled `{}`.".format(foundImage.tags[0])}
    except:
        try:
            # Search for image on docker repos
            pulledImage = client.images.pull("{}:latest".format(image))
            return {"success": False, "code": "ADM-11", "message": "Image found and pulled, run it with `!docker admin run {}`".format(pulledImage.tags[0])}
        except:
            # No image found on docker repos
            return {"success": False, "code": "ADM-01", "message": "No image found on docker repos."}