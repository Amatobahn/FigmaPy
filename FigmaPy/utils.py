def get_file_key(node):
    if hasattr(node, 'file_key'):
        return node.file_key
    if hasattr(node, '_file_key'):
        return node._file_key
    if hasattr(node, 'mainFileKey'):
        return node.mainFileKey
    # return _parent.file_key  # todo property get setter
    return node._parent.get_file_key()
