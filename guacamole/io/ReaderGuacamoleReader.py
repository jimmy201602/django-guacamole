
import select

from GuacamoleReader import GuacamoleReader
from guacamole.exceptions import GuacamoleServerException, GuacamoleUpstreamTimeoutException
from guacamole.protocol.GuacamoleInstruction import GuacamoleInstruction
import socket

# TODO cleanup
class ReaderGuacamoleReader(GuacamoleReader):
    def __init__(self, socket):
        self.socket = socket
        self.parseStart = 0
        self.buffer = bytearray(0)
        self.readPoller = select.poll()
        self.readPoller.register(socket, select.POLLIN)

    def available(self):
        ready = self.readPoller.poll(0)
        return len(ready) > 0 or len(self.buffer) > 0

    def read(self):
        try:
            while True:
                elementLength = 0
                i = self.parseStart
                while i < len(self.buffer):
                    readChar = chr(self.buffer[i])
                    i += 1
                    if '0' <= readChar and readChar <= '9':
                        elementLength = elementLength * 10 + ord(readChar) - ord('0')
                    elif readChar == '.':
                        if i + elementLength < len(self.buffer):
                            terminator = chr(self.buffer[i + elementLength])
                            i += elementLength + 1
                            elementLength = 0
                            self.parseStart = i
                            if terminator == ';':
                                instruction = bytearray(i)
                                instruction[:] = self.buffer[0:i]
                                self.buffer = self.buffer[i:]
                                self.parseStart = 0
                                return instruction
                            elif terminator != ',':
                                raise GuacamoleServerException("Element terminator of instruction was not ';' nor ','")
                        else:
                            break
                    else:
                        raise GuacamoleServerException("Non-numeric character in element length.")
                chunk = bytearray(4096)
                numRead = self.socket.recv_into(chunk)
                if numRead <= 0:
                    return None
                self.buffer.extend(chunk[:numRead])
        except socket.timeout as e:
            raise GuacamoleUpstreamTimeoutException(e)
        except socket.error as e:
            raise GuacamoleServerException(e)

    def readInstruction(self):
        chunk = self.read()
        if not chunk:
            return None

        elementStart = 0;
        elements = []

        while elementStart < len(chunk):
            lenghtEnd = -1
            for i in range(elementStart, len(chunk)):
                if chunk[i] == ord('.'):
                    lengthEnd = i
                    break

            if lengthEnd == -1:
                raise GuacamoleServerException("Read returned incomplete instruction.")

            length = int(chunk[elementStart:lengthEnd])

            elementStart = lengthEnd + 1
            element = chunk[elementStart:elementStart+length]

            elements.append(element)

            elementStart += length
            terminator = chunk[elementStart]

            elementStart += 1

            if terminator == ';':
                break

        # Optimize?
        opcode = elements.pop(0)
        instruction = GuacamoleInstruction(opcode, *elements)
        return instruction;

