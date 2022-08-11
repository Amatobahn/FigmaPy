def get_file_key(node):
    """
    Retrieve file key of a node

    comments use file_key
    files use mainFileKey
    get file key / fileMeta use key
    """
    if hasattr(node, "file_key"):
        return node.file_key
    if hasattr(node, "_file_key"):
        return node._file_key
    if hasattr(node, "mainFileKey"):
        return node.mainFileKey
    # return _parent.file_key  # TODO: property get setter
    return node._parent.get_file_key()
