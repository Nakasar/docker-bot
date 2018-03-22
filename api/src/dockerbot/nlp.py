from . import recast

def analyse(string):
    response = recast.request.analyse_text(string)
    try:
        intent = response.intent.slug
        try:
            entities = response.entities
            return {"string": string, "intent": intent, "entities": entities}
        except:
            return {"string": string, "intent": intent, "entities": None}
    except:
        return {"string": string, "intent": None, "entities": None}
