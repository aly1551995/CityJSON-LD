import json
from typing import Union, List, Dict, Any, Optional
from Transform.scale import Scale
from Transform.translate import Translate

class Transform:
    def __init__(self, scale: Union[Scale, List[float]], translate: Union[Translate, List[float]]):
        """
        Initialize the Transform object with scale and translate values.

        :param scale: Scale object or list of 3 floats representing scale factors.
        :param translate: Translate object or list of 3 floats representing translation values.
        """
        self.scale = self.to_scale(scale)
        self.translate = self.to_translate(translate)

    @staticmethod
    def to_scale(scale: Union[Scale, List[float]]) -> Scale:
        """
        Convert a list of scale factors to a Scale object.

        :param scale: List of 3 floats or a Scale object.
        :return: Scale object.
        """
        if isinstance(scale, list):
            if len(scale) == 3:
                x, y, z = scale
                return Scale(x, y, z)
            else:
                raise ValueError("Scale should be a list of 3 floats")
        elif isinstance(scale, Scale):
            return scale
        else:
            raise TypeError("Scale should be either a Scale object or a list of 3 floats")

    @staticmethod
    def to_translate(translate: Union[Translate, List[float]]) -> Translate:
        """
        Convert a list of translation values to a Translate object.

        :param translate: List of 3 floats or a Translate object.
        :return: Translate object.
        """
        if isinstance(translate, list):
            if len(translate) == 3:
                x, y, z = translate
                return Translate(x, y, z)
            else:
                raise ValueError("Translate should be a list of 3 floats")
        elif isinstance(translate, Translate):
            return translate
        else:
            raise TypeError("Translate should be either a Translate object or a list of 3 floats")

    def to_json(self) -> Dict[str, Any]:
        """
        Convert the Transform object to a JSON-LD representation.

        :return: JSON-LD representation of the Transform object.
        """
        scale_dict = json.loads(self.scale.to_json())
        translate_dict = json.loads(self.translate.to_json())
        data = {
            "@type": "cj:Transform",
            "cj:hasScale": scale_dict,
            "cj:hasTranslate": translate_dict,
        }
        return data
