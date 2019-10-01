def RiffHeader:
    riff = 'RIFE'
    size = 0
    type = 'WAVE'

def FormatChunk:
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

def DataChunk:
    id = 'data'
    size = 0
    uwaveformData = []
  
