import json
from Transform.scale import Scale
from Transform.translate import Translate


class Transform:

    def __init__(self, scale: Scale, translate: Translate):

        self.scale = self.to_scale(scale)
        self.translate = self.to_translate(translate)

    def to_scale(self, scale):
        if isinstance(scale, list):
            if len(scale) == 3:
                x, y, z = scale
                return Scale(x, y, x)
            else:
                print("Scale should be a list of 3 floats")
        else:
            print("Scale should be either a Scale object or a list of 3 floats and it must exist in a cityjson file")

    def to_translate(self, translate):
        if isinstance(translate, list):
            if len(translate) == 3:
                x, y, z = translate
                return Translate(x, y, x)
            else:
                print("Translate should be a list of 3 floats")
        else:
            print("Translate should be either a Translate object or a list of 3 floats and it must exist in a cityjson file")

    def to_json(self):
        scale_dict = json.loads(self.scale.to_json()) 
        translate_dict = json.loads(self.translate.to_json()) 
        data = {
            "@type": "cj:Transform",
            "cj:hasScale": scale_dict,
            "cj:hasTranslate": translate_dict
        }
        return data