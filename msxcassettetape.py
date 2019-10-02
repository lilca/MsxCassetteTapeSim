import WaveFile

class MsxCassetteTape:
    def __init__(self):
        self.baudrate = 1200     # 1200bps or 2400bps
        self.samplerate = 44100
        self.filename = ""
        self.tapedata = []

    def setArray(self, array):
        for idx in range(len(array)):
            self.tapedata[idx] = array[idx]*4+3
    def playShortHeader(self, wavefile):
        wavefile.extendSquareWave(self.baudrate * 2, 50, 1700)
    def playLongHeader(self, wavefile):
        wavefile.extendSquareWave(self.baudrate * 2, 50, 6700)
    def csave(self):
        wave = WaveFile(self.samplerate)
        # File Header
        self.playLongHeader(wave)
        self.playByteRepeat(0xd3, 10)
        for idx in range(6):
            self.playByte(filename[idx])
        # Interval
        self.playInterval(1000)     // n[ms]
        # File Body
        self.playShortHeader()
        self.playByteArray(pointer, n)
        self.playByteRepeat(0x00, 7)

    def save(self):
        # File Header
        self.playLongHeader()
        self.playByteRepeat(0xea, 10)
        for idx in range(6):
            self.playByte(filename[idx])
        # Interval
        self.playInterval(1000)     // n[ms]
        # File Body
        while:
            self.playShortHeader()
            self.playByteArray(pointer, 256)

    def bsave(self, startaddr, endaddr,runaddr):
        # File Header
        self.playLongHeader()
        self.playByteRepeat(0xd0, 10)
        for idx in range(6):
            self.playByte(filename[idx])
        # Interval
        self.playInterval(1000)     // n[ms]
        # File Body
        self.playShortHeader()
        self.playInt(off_address)
        self.playInt(last_address)
        self.playInt(start_address)
        self.playByteArray(pointer, last_address-off_address)

if __name__ == "__main__":
    tape = MsxCassetteTape()
    self.csave("file  ")
