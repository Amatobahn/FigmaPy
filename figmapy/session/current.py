# to avoid import loops, this is a separate module
#
# a helper to allow for easy access to the active session from figma nodes.
# do not rely on this session when using multiple active sessions.
figma_session = None
