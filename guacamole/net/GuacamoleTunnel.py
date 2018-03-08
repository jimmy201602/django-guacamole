#!/usr/bin/env python


class GuacamoleTunnel(object):
    INTERNAL_DATA_OPCODE = ''

    def acquireReader(self):
        raise Exception("Not Implemented")

    def releaseReader(self):
        raise Exception("Not Implemented")

    def hasQueuedReaderThreads(self):
        raise Exception("Not Implemented")

    def acquireWriter(self):
        raise Exception("Not Implemented")

    def releaseWriter(self):
        raise Exception("Not Implemented")

    def getUUID(self):
        raise Exception("Not Implemented")

    def getSocket(self):
        raise Exception("Not Implemented")

    def close(self):
        raise Exception("Not Implemented")

    def isOpen(self):
        raise Exception("Not Implemented")

