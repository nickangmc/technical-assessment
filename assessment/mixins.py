# This mixin class must be used alongside a rest_framework ViewSet


class SerializerMixin:

    # Attribute for setting serializers on per-action levels
    # Each action must be in the list of actions in a view set
    # e.g. List, Retrieve, Create, Update, Partial Update, Destroy
    #
    #   Format:
    #       {
    #           <action>: <serializer>,
    #           <action>: <function_name_in_string>,
    #           ...
    #       }
    #
    #   Example:
    #       {
    #           "list": Serializer,
    #           "retrieve": Serializer,
    #           "update": "get_update_serializer"
    #       }
    #
    serializer_class_per_action = None

    def get_serializer_class(self, *args, **kwargs):

        if isinstance(self.serializer_class_per_action, dict):

            # Gets the default serializer from the class
            default_serializer = self.serializer_class

            # Gets serializer at per-action level if exists
            # otherwise fallbacks to use the default serializer
            self.serializer_class = self.serializer_class_per_action.get(
                self.action,
                default_serializer,
            )

            # Checks if serializer selected is a function (represented by the
            # function name in string format)
            # If so, runs the function and selects the serializer returned
            if isinstance(self.serializer_class, str):
                func = getattr(self, self.serializer_class)

                if callable(func):
                    self.serializer_class = func()

        # Parent method: rest_framework.generics.GenericAPIView.get_serializer_class
        return super().get_serializer_class(*args, **kwargs)
