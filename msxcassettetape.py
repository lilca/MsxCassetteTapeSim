##################################################
# MsxCassetteTape.py
# lilca reload
# ver 1.0 : 2019/10/03
##################################################
import WaveFile

class MsxCassetteTape:
    def __init__(self, filename="tapdat"):
        self.baudrate = 1200     # 1200bps or 2400bps
        self.samplerate = 44100
        self.filename = filename
        self.tapedata = []

    def extendText(self, text):
        self.tapedata = text
    def setArray(self, array):
        for idx in range(len(array)):
            self.tapedata[idx] = array[idx]*4+3
    def playShortHeader(self, wavefile):
        wavefile.extendSquareWave(self.baudrate * 2, 50, 1700)
    def playLongHeader(self, wavefile):
        wavefile.extendSquareWave(self.baudrate * 2, 50, 6700)
    def playBit0(self, wavefile):
        wavefile.extendSquareWaveN(self.baudrate, 50, 1)
    def playBit1(self, wavefile):
        wavefile.extendSquareWaveN(self.baudrate * 2, 50, 2)
    def playByte(self, wavefile, bytedata):
        # Start bit
        self.playBit0(wavefile)
        # Byte data
        for shift in range(8):
            tmp = (bytedata >> shift) & 0x01
            if tmp == 0:
                self.playBit0(wavefile)
            else:
                self.playBit1(wavefile)
        # Stop bit
        self.playBit1(wavefile)
        self.playBit1(wavefile)
    def playByteRepeat(self, wavefile, bytedata, n):
        for idx in range(n):
            self.playByte(wavefile, bytedata)
    def playByteArray(self, wavefile, bytearray):
        for data in bytearray:
            self.playByte(wavefile, ord(data))
    def playInterval(self, wavefile, msec):
        wavefile.extendSilence(msec)
    def csave(self):
        wave = WaveFile.WaveFile(self.samplerate)
        # File Header
        self.playLongHeader(wave)
        self.playByteRepeat(wave, 0xd3, 10)
        for idx in range(6):
            self.playByte(wave, ord(self.filename[idx]))
        # Interval
        self.playInterval(wave, 1000)     # n[ms]
        # File Body
        self.playShortHeader(wave)
        self.playByteArray(wave, self.tapedata)
        self.playByteRepeat(wave, 0x00, 7)
        wave.writeWaveFile("/Users/mise/Documents/github/repository/MsxCassetteTapeSim/tape.wav")

    def save(self):
        # File Header
        self.playLongHeader()
        self.playByteRepeat(0xea, 10)
        for idx in range(6):
            self.playByte(filename[idx])
        # Interval
        self.playInterval(1000)     // n[ms]
        # File Body
        for idx in len(self.tapedata)/256:
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
    tape.extendText("' Yomikometa?")
    tape.csave()
