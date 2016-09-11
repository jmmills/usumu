import os

DEFAULTS = {}

# precedence
# {NAME}_USUMU_{KEY} if name is defined
# USUMU_{KEY}
# DEAFULTS[KEY]

APP_KEY_FORMAT = 'USUMU_{}'
NAME_KEY_FORMAT = '{}_' + APP_KEY_FORMAT


class Config(object):
    def __init__(self, name=None):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def _name_key(self, key):
        return NAME_KEY_FORMAT.format(self.name, key)

    def _app_key(self, key):
        return APP_KEY_FORMAT.format(key)

    def _has_name_key(self, key):
        return self.name is not None and os.getenv(self._name_key(key)) is not None

    def _has_app_key(self, key):
        return os.getenv(self._app_key(key)) is not None

    def _has_default_key(self, key):
        return key in DEFAULTS

    def _get_name_value(self, key):
        return os.getenv(self._name_key(key))

    def _get_app_value(self, key):
        return os.getenv(self._app_key(key))

    @staticmethod
    def _get_default_value(self, key):
        return DEFAULTS[key]

    def _has_key_with_precedence(self, key):
        return self._has_name_key(key) or self._has_app_key(key) or self._has_default_key(key)

    def _get_key_with_precedence(self, key):
        if self._has_name_key(key):
            return self._get_name_value(key)

        if self._has_app_key(key):
            return self._get_name_value(key)

        if self._has_default_key(key):
            return self._get_name_value(key)

    def _raise_for_invalid_key(self, key):
        assert(self._has_key_with_precedence(key),
               'Configuration key "{}" not found in DEFAULTS or {}, {}'.format(self._name_key(), self._app_key()))


    # TODO: write __getattr__ method
