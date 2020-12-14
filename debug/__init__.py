import sys

QUIET = 0
NORMAL = 1
VERBOSE = 2


class DebugObj:
    def __init__(self, debug_mode=NORMAL):
        self.debug_mode = debug_mode
        self._history = []

    def _get_debug_string(self, args, sep, end):
        args = (str(item) for item in args)
        output = sep.join(args)
        output = output + end
        return output

    def debug(self, *args, sep=' ', end='\n'):
        debug_string = self._get_debug_string(args, sep, end)
        self._history.append(debug_string)
        if self.debug_mode == 0:
            return

        msg = f"Debug: {debug_string}"
        sys.stdout.write(msg)

    def set_debug_mode(self, mode):
        if mode not in [0, 1, 2]:
            raise ValueError("Invalid mode provided")
        self.debug_mode = mode

    def __call__(self, *args, **kwargs):
        self.debug(*args, **kwargs)


debug = DebugObj()


def set_debug_mode(mode):
    debug.set_debug_mode(mode)
