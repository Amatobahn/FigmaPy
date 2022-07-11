def get_file_key(node):
    if hasattr(node, 'file_key'):
        return node.file_key
    # return _parent.file_key  # todo property get setter
    return node._parent.get_file_key()
