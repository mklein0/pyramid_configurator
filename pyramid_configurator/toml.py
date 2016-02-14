#
"""
An extension to the Pyramid Configurator library which loads TOML configurations into the settings file.
"""
import os
import collections

import pytoml

from pyramid.config import Configurator
from pyramid.config.settings import Settings

from pyramid_configurator.loader.toml import load_toml_with_inherit


PYRAMID_TOML_SETTINGS_LOCATION_KEY = 'pyramid.settings.toml.location'


class TomlSettings(Settings):

    def __init__(self, d=None, _environ_=os.environ, **kw):
        # Derived toml location based on priority of where value is defined.
        # Locations in growing priority order.
        #
        #   1. Settings from INI configuration
        #   2. Overriden function parameter
        #   3. Environment Variable
        toml_location = None
        if d is not None:
            toml_location = d.get(PYRAMID_TOML_SETTINGS_LOCATION_KEY)

        toml_location = kw.get(PYRAMID_TOML_SETTINGS_LOCATION_KEY.replace('.', '_'), toml_location)
        toml_location = _environ_.get(PYRAMID_TOML_SETTINGS_LOCATION_KEY.replace('.', '_').upper(), toml_location)

        if toml_location is not None:
            # TOML Location present, load it using special file inheritance rules.
            toml_dict = load_toml_with_inherit(toml_location)

            # Update the dict read from the INI file, if present
            if d is not None:
                d.update(toml_dict)

            else:
                # No settings from INI file.
                d = toml_dict

        super(TomlSettings, self).__init__(d=d, _environ_=_environ_, **kw)


class TomlConfigurator(Configurator):

    def _set_settings(self, mapping):
        if not mapping:
            mapping = {}
        settings = TomlSettings(mapping)
        self.registry.settings = settings
        return settings
