class Result:
    def __init__(self) -> None:
        self._errors = []
        self._object = None

    def has_errors(self):
        return len(self.errors()) > 0

    def errors(self):
        return self._errors

    def add_error(self, error):
        self._errors.append(error)

    def set_object(self, obj):
        self._object = obj

    def get_object(self):
        return self._object

    def errors_as_str(self):
        return ', '.join(self.errors())


class Command:
    def execute(self):
        raise NotImplementedError('Subclass responsibility')
