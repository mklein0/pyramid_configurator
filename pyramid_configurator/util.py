#
"""

"""

def dict_merge(dst, src):
    """
    recursively modifies in place the destination dict (dst) and its sub-dicts by merging the source dict into it.

    :param dict | None dst: Destination Dict to modifiy in place
    :param Any src: Source Dict to copy into the Destination Dict

    :return: destination dict, or source value if source value is not a dict
    :rtype: Any
    """
    if not isinstance(src, dict):
        return src

    if dst is None:
        dst = {}

    for k, v in src.items():
        if k in dst and isinstance(dst[k], dict):
            # Merge value into sub-dict
            dst[k] = dict_merge(dst[k], v)

        else:
            # Not merging into a dict, simply override existing value if any
            dst[k] = dict_merge(None, v)

    # Return merged dict
    return dst
