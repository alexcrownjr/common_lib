import json
from collections.abc import Iterable
from aiohttp.web import View, Request, HTTPMethodNotAllowed, Response


DEFAULT_METHODS = ('GET', 'POST', 'PUT', 'DELETE')


class ApiView(View):
    """
    Extended aiohttp.web.View class that supports serializing data returned by base http methods.

    get, post and other http methods should return model object or iterable of objects.
    Returned data is serialized and included in Response in json format.

    Usage example:
        class SomeView(ApiView):
            serializer_class = SomeModelSerializer

            async def get(self):
                model = SomeModel()
                return model
    """
    serializer_class = None
    results_key = "results"

    def __init__(self, request: Request) -> None:
        super().__init__(request)
        self.methods = {}
        self._get_class_methods()

        method_name = self.request.method.upper()
        if not method_name:
            raise HTTPMethodNotAllowed(method_name)

        setattr(self, method_name.lower(), self._serializer_wrapper(self.methods[method_name]))

    def _serializer_wrapper(self, method):
        """
        Returned metod data is serialized and returned in response
        """
        async def _wrap(*args, **kwargs):
            response = await method(*args, **kwargs)
            if isinstance(response, Iterable):
                serialized = self.get_serializer(response, many=True)
            else:
                serialized = self.get_serializer(response)
            return Response(text=json.dumps(serialized), content_type="application/json")
        return _wrap

    def _get_class_methods(self):
        """
        Prefill self.methods with actually implemented methods in class.
        """
        for method_name in DEFAULT_METHODS:
            method = getattr(self, method_name.lower(), None)
            if method:
                self.methods[method_name.upper()] = method

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        """
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.serializer_class

    def get_serializer(self, data=None, many=False):
        """
        Return serialized data depending on if data is iterable or single object.
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(many=many).dump(data)
        try:
            return {self.results_key: serializer.data} if many else serializer.data
        except AttributeError:
            return {self.results_key: serializer} if many else serializer
