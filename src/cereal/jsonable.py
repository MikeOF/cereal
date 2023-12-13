import inspect
import json
from abc import ABCMeta
from typing import Optional


class JSONAble(metaclass=ABCMeta):

    _SERIALIZATION_MODULE = json
    _CONSTRUCTOR_PARAMETER_SET: Optional[set[str]] = None

    @classmethod
    def _ensure_constructor_parameter_set(cls) -> None:

        if cls._CONSTRUCTOR_PARAMETER_SET is None:

            cls._CONSTRUCTOR_PARAMETER_SET = {
                name for name in inspect.signature(cls.__init__).parameters if name != 'self'
            }

    @classmethod
    def from_json_str(cls, json_str):
        return cls.from_json(json_obj=json.loads(json_str))

    @classmethod
    def from_json(cls, json_obj: dict):

        cls._ensure_constructor_parameter_set()
        construction_kwarg_by_name = {k: v for k, v in json_obj.items() if k in cls._CONSTRUCTOR_PARAMETER_SET}

        return  cls(**construction_kwarg_by_name)

    def to_json_str(self, indent: int = None):
        return json.dumps(self.to_json(), indent=indent)

    def to_json(self):
        self._ensure_constructor_parameter_set()
        return {k: getattr(self, k) for k in self._CONSTRUCTOR_PARAMETER_SET}
