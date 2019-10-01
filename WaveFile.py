import struct

class RiffHeader:
    def __init__(self): # 12
        self.riff = 'RIFF'
        self.size = 0
        self.type = 'WAVE'
    def update(self, chunksize):
        self.size = chunksize + len(self.type)
    def writeRiffHeader(self, fp):
        fp.write(self.riff.encode())
        fp.write(struct.pack("I", self.size))
        fp.write(self.type.encode())

class FormatChunk: # 24+alpha
    def __init__(self):
        self.id = 'fmt '
        self.size = 0
        self.format = 1    # WAVE_FORMAT_PCM
        self.channels = 1   # monoral=1, stereo=2
        self.samplerate = 44100
        self.bytepersec = -1
        self.blockalign = -1
        self.bitswidth = 8
        self.extended_size = 0
        self.extended = []
    def update(self):
        self.blockalign = int(self.bitswidth / 8 * self.channels)
        self.bytepersec = self.samplerate * self.blockalign
        self.size = 16
        if self.extended_size != 0:
            self.size += 2 + self.extended_size
    def setExtended(self, array):
        self.extended.extend(array)
        self.extended_size = len(self.extended)
    def clearExtended(self):
        self.extended = []
        self.extended_size = 0
    def writeFormatChunk(self, fp):
        fp.write(self.id.encode())
        fp.write(struct.pack("I", self.size))
        fp.write(struct.pack("H", self.format))
        fp.write(struct.pack("H", self.channels))
        fp.write(struct.pack("I", self.samplerate))
        fp.write(struct.pack("I", self.bytepersec))
        fp.write(struct.pack("H", self.blockalign))
        fp.write(struct.pack("H", self.bitswidth))
        if self.extended_size != 0:
            fp.write(struct.pack("H", self.extended_size))
            fp.write(bytes(self.extended))

class DataChunk:
    def __init__(self):
        self.id = 'data'
        self.size = 0
        self.waveData = []
    def extendWaveData(self, array):
        self.waveData.exptend(array)
        self.size = len(waveData)
    def clearWaveData(self):
        self.waveData = []
        self.size = 0
    def writeDataChunk(self, fp):
        fp.write(self.id.encode())
        fp.write(struct.pack("I", self.size))
        fp.write(bytes(self.waveData))

class WaveFile:
    def __init__(self):
        self.riff = RiffHeader()
        self.fmt = FormatChunk()
        self.data = DataChunk()
    def update(self):
        self.fmt.update()
        self.riff.update(self.fmt.size + self.data.size + 8 + 8)
    def writeWaveFile(self, path):
        self.update()
        with open(path, 'wb') as fp:
            self.riff.writeRiffHeader(fp)
            self.fmt.writeFormatChunk(fp)
            self.data.writeDataChunk(fp)
    def createWave(self, type, freq, second):
        waves = int(self.fmt.samplerate * second / freq)
        cycle = int(self.fmt.samplerate / waves)
        res = []
        val = 0
        if type != 0:
            val = 255
        for idx in range(waves):
            val = 255 - val
            for i in range(int(cycle / 2)):
                res.extend([val])
            val = 255 - val
            for i in range(int(cycle / 2)):
                res.extend([val])
        self.data.waveData = res
        self.data.size = self.fmt.samplerate * second


if __name__ == "__main__":
    wave = WaveFile()
    wave.createWave(0, 440, 1)
    wave.writeWaveFile("/Users/mise/Documents/github/repository/MsxCassetteTapeSim/test.wav")
