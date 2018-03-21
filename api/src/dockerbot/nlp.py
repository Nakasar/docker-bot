from . import recast

def analyse(string):
    response = recast.requet.analyse_text(string)
    intent = response.intent.slug
    entities = {}
    for entity in response.entities:
        entities[entity.name] = entity.value
    return (string, intent, entities)
