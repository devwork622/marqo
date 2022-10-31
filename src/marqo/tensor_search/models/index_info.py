import pprint
from typing import NamedTuple, Any
from marqo.tensor_search import enums


class IndexInfo(NamedTuple):
    """
    model_name: name of the ML model used to encode the data
    properties: keys are different index field names, values
        provide info about the properties
    """
    model_name: str
    properties: dict
    index_settings: dict

    def get_index_settings(self) -> dict:
        return self.index_settings.copy()

    def get_vector_properties(self) -> dict:
        """returns a dict containing only names and properties of vector fields
        Perhaps a better approach is to check if the field's props is actually a vector type,
        plus checks over fieldnames
        """
        return {
            vector_name: vector_props
            for vector_name, vector_props in self.properties[enums.TensorField.chunks]["properties"].items()
            if vector_name.startswith(enums.TensorField.vector_prefix)
        }

    def get_text_properties(self) -> dict:
        """returns a dict containing only names and properties of non
        vector fields.

        This returns more than just pure text fields. For example: ints
        bool fields.

        """
        return {
            text_field: text_props
            for text_field, text_props in self.properties.items()
            if not text_field.startswith(enums.TensorField.vector_prefix)
                and not text_field in enums.TensorField.__dict__.values()
        }

    def get_true_text_properties(self) -> dict:
        """returns a dict containing only names and properties of fields that
        are true text fields
        """
        simple_props = self.get_text_properties()

        true_text_props = dict()
        for text_field, text_props in simple_props.items():
            try:
                if text_props["type"] == enums.OpenSearchDataType.text:
                    true_text_props[text_field] = text_props
            except KeyError:
                continue
        return true_text_props