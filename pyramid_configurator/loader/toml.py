#
"""
An extension to the Pyramid Configurator library which loads TOML configurations into the settings file.
"""
import os
import collections

from pytoml import load as pytoml_load

from pyramid_configurator.util import dict_merge


CurrentTomlFile = collections.namedtuple(
    'CurrentTomlFile', ['filename', 'inherit_file_iter', 'base_dir', 'toml_dict', 'result_dict'])


def load_toml_with_inherit(filename, base_dir='/', inherit_key='inherit'):
    """
    Load TOML file with special mangement for file based inheritance.

    func load_file
        1. create an empty resulting dict.
        1. Read current TOML File into a separate dict.
        2. Extract inheritance list of parent TOML files to derive from.
        3. For each parent TOML file in list order.
            1. Call this func load_file on that file.
            2. Take resulting configuration dict and merge it into resulting dict.
               Last Write wins.
        5. Merge separate TOML dict from current TOML File read into resulting dict.
        6. Return resulting dict.

    :param str filename: location of TOML file
    :param str base_dir: staring directory to look for TOML file from
    :param str inherit_key: Key Name for inherit configuration.

    :rtype: dict
    """
    result_dict = {}

    # File processing stack for TOML File Inheritance.
    file_processing_stack = [
        CurrentTomlFile(
            filename='<root>', inherit_file_iter=iter((filename,)), base_dir=base_dir,
            toml_dict={}, result_dict=result_dict
        )
    ]

    # Detect loops in inheritance file and cache results to speed loading of files.
    cached_result_dicts = {}
    processed_files = set()

    while len(file_processing_stack) > 0:
        # Look at head of file processing stack
        current_toml = file_processing_stack[-1]

        try:
            # Get next filename to process
            pathname = current_toml.inherit_file_iter.next()

        except StopIteration:
            # Current file list iterator is finished, remove it from processing stack
            file_processing_stack.pop()

            # Finished processing files we are inheriting from. Apply current TOML file configuration
            # to inheritance results
            cached_result_dicts[current_toml.filename] = \
                dict_merge(current_toml.result_dict, current_toml.toml_dict)

            # If current file is a child of another file in the stack, merge current file results into
            # parent file results.
            if len(file_processing_stack) > 0:
                parent_toml = file_processing_stack[-1]

                # Add the current toml results to parent file which is inheriting
                dict_merge(parent_toml.result_dict, current_toml.result_dict)

            # Next iteration of loop
            continue

        # Need to load next file in processing queue
        filename, base_dir, optional = decode_inherit_filename(pathname, base_dir=current_toml.base_dir)

        cached_result = cached_result_dicts.get(filename)
        if cached_result:
            # There is a cached result for desired file, use that.
            dict_merge(current_toml.result_dict, cached_result)

        elif filename in processed_files:
            # We are already processing file in question, but have not determined a result.
            # must be a circular reference in inheritance chain.
            # TODO: Improve this message.
            raise ValueError('Cycle detected in inheritance chain')

        else:
            # Mark new child toml as being processed, and begin processing.
            processed_files.add(filename)
            child_toml = load_toml_file(filename, base_dir, optional, inherit_key=inherit_key)
            if child_toml is None:
                continue

            # Else, Add new file entry to process stack so values are merged next iteration
            file_processing_stack.append(child_toml)

    # Finished processing TOML file and its parent files, return result
    return result_dict


def load_toml_file(filename, base_dir, optional, inherit_key='inherit'):
    """
    load TOML file and return a description of its value and inheritance requirements.

    :param str filename: location of TOML file
    :param str base_dir: Directory to look for TOML file in
    :param bool optional: If file existance is required, set to False
    :param str inherit_key: Key Name for inherit configuration.

    :return: Description of TOML file being read in.
    :rtype: CurrentTomlFile | None
    """
    try:
        with file(filename, 'rb') as fobj:
            toml_dict = pytoml_load(fobj)

        # Determine if new file has additional files to inherit
        # iterate out those configuration dicts first
        inherit_filenames = toml_dict.pop(inherit_key, ())

    except IOError:
        # Assume file does not exist error, skip if file is optional
        if optional:
            return None

        # Else, file is required
        raise

    # Add entry to process queue so values are merged next iteration, or more files processed
    return CurrentTomlFile(
        filename=filename, inherit_file_iter=iter(inherit_filenames),
        base_dir=base_dir, toml_dict=toml_dict, result_dict={}
    )


def decode_inherit_filename(pathname, base_dir='/'):
    """
    Decode path for TOML file to absolute path and its characteristics.

    :param str pathname: location of TOML file
    :param str base_dir: staring directory to look for TOML file from

    :return: absolute pathname, directory path of pathname, if file existance is optional
    :rtype: str, str, bool
    """
    # Check if current file is optional
    optional = False
    if pathname.startswith('?'):
        optional = True
        pathname = pathname[1:]

    # Determine location of file
    pathname = os.path.abspath(os.path.join(base_dir, pathname))

    # Determine the new base location for the inheritance configs being read.
    base_dir = os.path.dirname(pathname)

    return pathname, base_dir, optional
