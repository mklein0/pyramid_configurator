#
"""
An extension to the Pyramid Configurator library which loads TOML configurations into the settings file.
"""
import os
import collections

from pytoml import load as pytoml_load

from pyramid_configurator.util import dict_merge


PendingTomlFile = collections.namedtuple(
    'PendingTomlFile', ['filename', 'filename_iter', 'base_dir', 'toml_dict'])


def load_toml_with_inherit(filename, base_dir='/', inherit_key='inherit'):
    """
    Load TOML file with special mangement for file based inheritance.

    :param str filename: location of TOML file
    :param str base_dir: staring directory to look for TOML file from
    :param str inherit_key: Key Name for inherit configuration.

    :rtype: dict
    """
    result = None

    pending_file_q = [
        PendingTomlFile(
            filename='<root>', filename_iter=iter((filename,)), base_dir=base_dir, toml_dict={}
        )
    ]

    while len(pending_file_q) > 0:
        # Look at head of processing q
        pending_toml = pending_file_q[-1]

        try:
            # Get next filename to process
            pathname = pending_toml.filename_iter.next()

        except StopIteration:
            # Current iterator is finished, remove it from processing q
            pending_file_q.pop()

            # Add the pending toml dict to results, children have been processed.
            result = dict_merge(result, pending_toml.toml_dict)

            # Next iteration of loop
            continue

        # Need to load next file in processing queue
        # Check if current file is optional
        optional = False
        if pathname.startswith('?'):
            optional = True
            pathname = pathname[1:]

        try:
            filename, toml_dict, new_filenames, base_dir = load_toml_file(
                pathname, base_dir=pending_toml.base_dir,
                inherit_key=inherit_key)

        except IOError:
            # Assume file does not exist error, skip if file is optional
            if optional:
                continue

            # Else, file is required
            raise

        # Add entry to process queue so values are merged next iteration, or more files processed
        pending_file_q.append(
            PendingTomlFile(
                filename=filename, filename_iter=iter(new_filenames),
                base_dir=base_dir, toml_dict=toml_dict
            )
        )

    # If no results due to optional file existance, return an empty dict
    if result is None:
        return {}

    # Else return merged dict
    return result


def load_toml_file(pathname, base_dir='/', inherit_key='inherit'):
    """
    :param str pathname: location of TOML file
    :param str base_dir: staring directory to look for TOML file from
    :param str inherit_key: Key Name for inherit configuration.

    :return: pathname of TOML file, TOML configuration, list of files to inherit, base directory of TOML file
    :rtype: str, dict, list[str], str
    """
    # Determine location of file
    pathname = os.path.abspath(os.path.join(base_dir, pathname))

    # Determine the new base location for the inheritance configs being read.
    base_dir = os.path.dirname(pathname)

    with file(pathname, 'rb') as fobj:
        toml_dict = pytoml_load(fobj)

    # Determine if new file has additional files to inherit
    # iterate out those configuration dicts first
    filenames = toml_dict.pop(inherit_key, ())

    return pathname, toml_dict, filenames, base_dir
