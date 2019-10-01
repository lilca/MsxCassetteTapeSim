class MsxCassetteTape:
    baudrate = 1200     // 1200bps or 2400bps
    filename = ""
    tapedata = []

    def csave(self):
        // File Header
        self.playLongHeader()
        self.playByteRepeat(0xd3, 10)
        for idx in range(6):
            self.playByte(filename[idx])
        // Interval
        self.playInterval(1000)     // n[ms]
        // File Body
        self.playShortHeader()
        self.playByteArray(pointer, n)
        self.playByteRepeat(0x00, 7)

    def save(self):
        // File Header
        self.playLongHeader()
        self.playByteRepeat(0xea, 10)
        for idx in range(6):
            self.playByte(filename[idx])
        // Interval
        self.playInterval(1000)     // n[ms]
        // File Body
        while:
            self.playShortHeader()
            self.playByteArray(pointer, 256)

    def bsave(self):
        // File Header
        self.playLongHeader()
        self.playByteRepeat(0xd0, 10)
        for idx in range(6):
            self.playByte(filename[idx])
        // Interval
        self.playInterval(1000)     // n[ms]
        // File Body
        self.playShortHeader()
        self.playInt(off_address)
        self.playInt(last_address)
        self.playInt(start_address)
        self.playByteArray(pointer, last_address-off_address)
