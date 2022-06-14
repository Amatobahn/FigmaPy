def get_file_key(node):
    if hasattr(node, 'file_key'):
        return node.file_key
    # return pythonParent.file_key  # todo property get setter
    return node.pythonParent.get_file_key()
