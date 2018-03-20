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
            client.containers.run(foundImage, detach=True)
        except:
            # Unable to run image, or an error occured in some process
            return {"success": False, "code": "ADM-05"}
    except:
        try:
            # Search for image on docker repos
            pulledImage = client.images.pull("{}:latest".format(image))
            return {"success": False, "code": "ADM-02", "message": "Image found and pulled, run it with `!docker admin run {}`".format(pulledImage.tags[0])}
        except:
            # No image found on docker repos
            return {"success": False, "code": "ADM-01", "message": "No image found on docker repos."}
