

class GuacamoleInstruction(object):
    def __init__(self, opcode, *instructions):
        self._opcode = opcode
        if len(instructions) == 1 and hasattr(instructions[0], '__iter__'):
            self._instructions = instructions[0]
        else:
            self._instructions = instructions

    def __str__(self):
        return ','.join([str(len(self._opcode)) + '.' + self._opcode]
                      + [(str(len(i)) + '.' + str(i)) for i in self._instructions]
                ) + ';'

    @property
    def opcode(self):
        return self._opcode

    @property
    def instructions(self):
        return self._instructions

