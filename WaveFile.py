class RiffHeader:
    def __init__(self):
        riff = 'RIFF'
        size = 0
        type = 'WAVE'

class FormatChunk:
    def __init__(self):
        id = 'fmt '
        size = 24
        format = 0    # WAVE_FORMAT_UNKNOWN
        channels = 1   # monoral=1, stereo=2
        samplerate = 44100
        bytepersec = self.samplerate * self.blockalign
        blockalign = self.bitswidth / 8 * self.channels
        bitswidth = 8
        extended_size = 0
        extended = []

class DataChunk:
    def __init__(self):
        id = 'data'
        size = 0
        uwaveformData = []
  
class WaveFile:
    def __init__(self):
        riff = RiffHeader()
        fmt = FormatChunk()
        data = DataChunk()
