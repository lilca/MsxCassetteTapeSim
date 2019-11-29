##################################################
# MsxCassetteTape.py
# lilca reload
# ver 1.0 : 2019/10/03
##################################################
import WaveFile

class MsxCassetteTape:
    _CTRL_Z = 0x1a
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
    def playWord(self, wavefile, bytedata):
        low = (bytedata & 0x00ff)
        high = ((bytedata >> 8) & 0x00ff)
        self.playByte(wavefile, low)
        self.playByte(wavefile, high)
    def playByteRepeat(self, wavefile, bytedata, n):
        for idx in range(n):
            self.playByte(wavefile, bytedata)
    def playByteArray(self, wavefile, bytearray):
        for data in bytearray:
            self.playByte(wavefile, ord(data))
    def playByteArrayN(self, wavefile, bytearray, n):
        for data in bytearray:
            self.playByte(wavefile, ord(data))
    def playInterval(self, wavefile, msec):
        wavefile.extendSilence(msec)
    def csave(self, save_path):
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
        wave.writeWaveFile(save_path)

    def save(self, save_path):
        wave = WaveFile.WaveFile(self.samplerate)
        # File Header
        self.playLongHeader(wave)
        self.playByteRepeat(wave, 0xea, 10)
        for idx in range(6):
            self.playByte(wave, ord(self.filename[idx]))
        # Interval
        self.playInterval(wave, 1000)     # n[ms]
        # File Body
        length = len(self.tapedata)
        for idx in range(length):
            if idx % 256 == 0:
                self.playShortHeader(wave)
            self.playByte(wave, ord(self.tapedata[idx]))
        self.playByte(wave, self._CTRL_Z)
        self.playByteRepeat(wave, self._CTRL_Z, (256 - length % 256 - 1))
        wave.writeWaveFile(save_path)

    def bsave(self, save_path, begin_addr, end_addr, run_addr):
        wave = WaveFile.WaveFile(self.samplerate)
        # File Header
        self.playLongHeader(wave)
        self.playByteRepeat(wave, 0xd0, 10)
        for idx in range(6):
            self.playByte(wave, ord(self.filename[idx]))
        # Interval
        self.playInterval(wave, 1000)     # n[ms]
        # File Body
        self.playShortHeader(wave)
        self.playWord(wave, begin_addr)
        self.playWord(wave, end_addr)
        self.playWord(wave, run_addr)
        for idx in range(end_addr - begin_addr):
            self.playByte(wave, ord(self.tapedata[idx]))
        wave.writeWaveFile(save_path)

    def roundBaud(self, freq):
        return round(freqfr)

    def importWaveFile(self, load_path):
        wave = WaveFile.WaveFile()
        wave.readWaveFile(load_path)
        res = self.analysisWaveFile(wave, 0, 128)
        # round
        for idx in range(len(res)):
            res[idx] = round(res[idx], -2)
        #
        sum = 0
        for idx in range(10000):
            sum += res[idx]
        baud = int(round(sum / 10000, -2))
        hbaud = int(baud / 2)
        print("baud = "+str(baud))
        print("hbaud = "+str(hbaud))
        #
        for idx in range(1, len(res)):
            if res[idx-1] == hbaud:
                print("0")
                idx += 1
            elif res[idx-1] == baud and res[idx] == baud:
                print("1")
                idx += 2

    def analysisWaveFile(self, wave, channel, origin):
        res = []
        stream = wave.data.waveData
        slen = len(stream)
        blocksize = wave.fmt.blockalign
        blocks = int(slen / blocksize)
        samplesize = int(wave.fmt.bitswidth / 8)
        status = 0
        cnt = 0
        for idx in range(blocks):
            # get sample
            index = idx * blocksize + channel * samplesize
            sample = stream[index]
            if samplesize > 1:
                sample = sample * 256 + stream[index + 1]
            # 立ち上がり
            if sample > origin and status == 0:
                status = 1
                diff = idx - cnt
                cnt = idx
                res.extend([int(wave.fmt.samplerate/(diff+1e-10))])
            # 立ち下がり
            elif sample <= origin and status == 1:
                status = 0
        return res

if __name__ == "__main__":
    tape = MsxCassetteTape()
    tape.extendText("' Yomikometa?")
    path = "/Users/mise/Documents/github/repository/MsxCassetteTapeSim"
    #tape.csave(path + "/ctape.wav")
    #tape.save(path + "/tape.wav")
    #tape.bsave(path + "/btape.wav", 800, 810, 800)
    tape.importWaveFile(path + "/cas.wav")
