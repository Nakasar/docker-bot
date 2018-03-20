def listContainers():
    global client
    try:
        containers = client.containers.list()
        return containers
    except:
        return []
