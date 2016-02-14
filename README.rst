pyramid_configurator
====================

Rather than boil the ocean and force other modules to support some alternate configuration specification
format or force developers to translate those configuration examples into an alternate configuration
specification. This module follows the philosphy of let others be and let us use an alternate
configuration specification formats like TOML for pyramid application settings.

Installation
============

.. code-block: bash

    $ pip install pyramid_configurator


.. code-block: ini

    [app:main]

    # ...

    pyramid.settings.toml.location = /etc/pyramid/my_config.toml

.. code-block: none

    [application]

    property1 = 4
    property2 = "test"
    property3 = [
        "test", 4, 5
    ]


Inheritance
===========
