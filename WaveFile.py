##################################################
# WaveFile.py
# lilca reload
# ver 1.0 : 2019/10/02
##################################################
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
    def readRiffHeader(self, data):
        self.riff = chr(data[0]) + chr(data[1]) + chr(data[2]) + chr(data[3])
        self.size = data[4] + data[5] * 256 + data[6] * 256 ** 2 + data[7] * 256 ** 3
        self.type = chr(data[8]) + chr(data[9]) + chr(data[10]) + chr(data[11])
        return 12
    def print(self):
        print("*** RIFF HEADER ***")
        print("RIFF識別子    ：" + self.riff)
        print("チャンクサイズ：" + str(self.size))
        print("フォーマット  ：" + self.type)

class FormatChunk: # 24+alpha
    def __init__(self, samplerate=44100 ,channels=1, bitswidth=8):
        self.id = 'fmt '
        self.size = 0
        self.format = 1    # WAVE_FORMAT_PCM
        self.channels = channels   # monoral=1, stereo=2
        self.samplerate = samplerate
        self.bytepersec = -1
        self.blockalign = -1
        self.bitswidth = bitswidth
        self.extended_size = 0
        self.extended = []
        self.update()
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
    def readFormatChunk(self, data):
        self.id = chr(data[0]) + chr(data[1]) + chr(data[2]) + chr(data[3])
        self.size = data[4] + data[5] * 256 + data[6] * 256 ** 2 + data[7] * 256 ** 3
        self.format = data[8] + data[9] * 256
        self.channels = data[10] + data[11] * 256
        self.samplerate = data[12] + data[13] * 256 + data[14] * 256 ** 2 + data[15] * 256 ** 3
        self.bytepersec = data[16] + data[17] * 256 + data[18] * 256 ** 2 + data[19] * 256 ** 3
        self.blockalign = data[20] + data[21] * 256
        self.bitswidth = data[22] + data[23] * 256
        if self.size > 16:
            self.extended_size = data[24] + data[25] * 256
            self.extended = data[26:]
        return self.size + 8
    def print(self):
        print("*** FORMAT CHUNCK ***")
        print("チャンク識別子      ：" + self.id)
        print("チャンクサイズ      ：" + str(self.size))
        print("音声フォーマット    ：" + str(self.format))
        print("チャンネル数        ：" + str(self.channels))
        print("サンプリング周波数  ：" + str(self.samplerate))
        print("byte/sec            ：" + str(self.bytepersec))
        print("byte/(channel*sample)：" + str(self.blockalign))
        print("bit/sample          ：" + str(self.bitswidth))
        print("拡張パラメータサイズ：" + str(self.extended_size))
        print("拡張パラメータ      ：")
        print(self.extended)

class DataChunk:
    def __init__(self):
        self.id = 'data'
        self.size = 0
        self.waveData = []
    def extendWaveData(self, array):
        self.waveData.extend(array)
        self.size = len(self.waveData)
    def clearWaveData(self):
        self.waveData = []
        self.size = 0
    def writeDataChunk(self, fp):
        fp.write(self.id.encode())
        fp.write(struct.pack("I", self.size))
        fp.write(bytes(self.waveData))
    def readDataChunk(self, data):
        self.id = chr(data[0]) + chr(data[1]) + chr(data[2]) + chr(data[3])
        self.size = data[4] + data[5] * 256 + data[6] * 256 ** 2 + data[7] * 256 ** 3
        self.waveData = data[8:]
        return 0
    def print(self):
        print("*** DATA CHUNCK ***")
        print("チャンク識別子      ：" + self.id)
        print("チャンクサイズ      ：" + str(self.size))
        print("波形データ          ：（省略）")
        #print(self.waveData)

class WaveFile:
    def __init__(self, samplerate=44100 ,channels=1, bitswidth=8):
        self.riff = RiffHeader()
        self.fmt = FormatChunk(samplerate, channels, bitswidth)
        self.data = DataChunk()
    def update(self):
        self.fmt.update()
        self.riff.update(self.fmt.size + self.data.size + 8 + 8)
    def extendWave(self, array):
        self.data.extendWaveData(array)
    def readWaveFile(self, path):
        with open(path, 'rb') as fp:
            data = fp.read()
        pos = self.riff.readRiffHeader(data)
        pos += self.fmt.readFormatChunk(data[pos:])
        pos += self.data.readDataChunk(data[pos:])
    def writeWaveFile(self, path):
        self.update()
        with open(path, 'wb') as fp:
            self.riff.writeRiffHeader(fp)
            self.fmt.writeFormatChunk(fp)
            self.data.writeDataChunk(fp)
    def extendSilence(self, msec):
        len = int(self.fmt.samplerate * msec / 1000)
        res = []
        for idx in range(len):
            res.extend([0])
        self.extendWave(res)
    def extendSquareWaveN(self, freq, dutyrate, waves):
        cycle = int(self.fmt.samplerate / freq)
        waves = int(waves)

        res = []
        for idx in range(waves):
            for i in range(cycle):
                if i <= cycle * dutyrate / 100:
                    res.extend([255])
                else:
                    res.extend([0])
        self.extendWave(res)
    def extendSquareWave(self, freq, dutyrate, msec):
        cycle = int(self.fmt.samplerate / freq)
        waves = int(self.fmt.samplerate * (msec / 1000) / cycle)
        self.extendSquareWaveN(freq, dutyrate, waves)
    def print(self):
        self.riff.print()
        self.fmt.print()
        self.data.print()
    def analysis(self, channel, origin):
        res = []
        stream = self.data.waveData
        slen = len(stream)
        blocksize = self.fmt.blockalign
        blocks = int(slen / blocksize)
        samplesize = int(self.fmt.bitswidth / 8)
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
                res.extend([int(self.fmt.samplerate/(diff+1e-10))])
            # 立ち下がり
            elif sample <= origin and status == 1:
                status = 0
        return res

if __name__ == "__main__":
    wave = WaveFile()
#    wave.extendSquareWave(2400, 50, 1000)
#    wave.extendSquareWave(4800, 50, 1500)
#    wave.writeWaveFile("/Users/mise/Documents/github/repository/MsxCassetteTapeSim/test.wav")
    wave.readWaveFile("/Users/mise/Documents/github/repository/MsxCassetteTapeSim/cas.wav")
    wave.print()
    max = 0
    min = 255
    count = 0
    sum = 0
    for val in wave.data.waveData:
        count +=1
        sum += val
        if max < val:
            max = val
        if min > val:
            min = val
    print(max, min)
    print(count, sum/count)

