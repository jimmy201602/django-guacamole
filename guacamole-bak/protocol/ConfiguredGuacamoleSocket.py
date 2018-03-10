from guacamole.exceptions import GuacamoleServerException
from guacamole.net.GuacamoleSocket import GuacamoleSocket
from GuacamoleClientInformation import GuacamoleClientInformation
from GuacamoleInstruction import GuacamoleInstruction

class ConfiguredGuacamoleSocket(GuacamoleSocket):
    def __init__(self, socket, config, info=None):
        if not info:
            info = GuacamoleClientInformation()

        self._socket = socket
        self._config = config
        self._info = info
        self._id = None

        reader = self._socket.getReader()
        writer = self._socket.getWriter()

        select_arg = config.connectionID
        if not select_arg:
            select_arg = config.protocol

        writer.writeInstruction(GuacamoleInstruction('select', select_arg))

        args = self.expect(reader, "args")
        arg_names = args.instructions
        arg_values = []
        for name in arg_names:
            arg_values.append(config.getParameter(str(name)) or '')

        writer.writeInstruction(GuacamoleInstruction('size',
            str(info.optimalScreenWidth),
            str(info.optimalScreenHeight),
            str(info.optimalScreenResolution)))
        writer.writeInstruction(GuacamoleInstruction('audio', info.audioMimetypes))
        writer.writeInstruction(GuacamoleInstruction('video', info.videoMimetypes))
        writer.writeInstruction(GuacamoleInstruction('image', info.imageMimetypes))
        writer.writeInstruction(GuacamoleInstruction('connect', arg_values))

        ready = self.expect(reader, "ready")
        ready_args = ready.instructions
        if len(ready_args) == 0:
            raise GuacamoleServerException("No connection ID received")

        self._id = ready_args[0]

    def expect(self, reader, opcode):
        instruction = reader.readInstruction()
        if not instruction:
            raise GuacamoleServerException('End of stream while waiting for ' + opcode)
        
        if instruction.opcode != opcode:
            raise GuacamoleServerException('Received "{}" instruction while expecting "{}"'.format(instruction.opcode, opcode))

        return instruction

    @property
    def config(self):
        return self._config

    @property
    def connectionID(self):
        return self._id

    def getReader(self):
        return self._socket.getReader()

    def getWriter(self):
        return self._socket.getWriter()

    def close(self):
        self._socket.close()

    def isOpen(self):
        return self._socket.isOpen()