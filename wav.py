from python_audio import base 
import numpy as np

class WavReadFile(base.BaseAudioReadFile):
  """ Sample Usage 


    wav_file = WavReadFile('samples/easy.wav')
    print(wav_file.numpy.shape, wav_file.numpy.dtype)
  """
  @property 
  def file_size(self):
    return self._file_size
  @property 
  def samples_per_sec(self):
    return self._samples_per_sec
  @property 
  def numpy(self):
    return self._data 
  @property 
  def num_channels(self):
    return self._num_channels

  def _parse_file(self, open_file):
    """ Based on  http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/WAVE.html 
    """
    if open_file.read(4) != b'RIFF':
      raise Exception('No RIFF chunk at', open_file.tell())

    self._file_size = self._parse_int(open_file.read(4))
    
    if open_file.read(4) != b'WAVE':
      raise Exception('No WAVE chunk at', open_file.tell())
    
    if open_file.read(4) != b'fmt ':
      raise Exception('No fmt chunk at', open_file.tell())

    fmt_cksize = self._parse_int(open_file.read(4))

    """
    0x0001	WAVE_FORMAT_PCM	PCM
    0x0003	WAVE_FORMAT_IEEE_FLOAT	IEEE float
    0x0006	WAVE_FORMAT_ALAW	      8-bit ITU-T G.711 A-law
    0x0007	WAVE_FORMAT_MULAW	      8-bit ITU-T G.711 µ-law
    0xFFFE	WAVE_FORMAT_EXTENSIBLE	Determined by SubFormat
    """ 
    wFormatTag = self._parse_int(open_file.read(2))
    if wFormatTag != 0x0001:
      raise Exception('Support only implemented for PCM files, this file is ', wFormatTag)
    
    self._num_channels = self._parse_int(open_file.read(2))
    self._samples_per_sec = self._parse_int(open_file.read(4))
    
    nAvgBytesPerSec = self._parse_int(open_file.read(4))
    nBlockAlign = self._parse_int(open_file.read(2))
    wBitsPerSample = self._parse_int(open_file.read(2))

    if open_file.read(4) != b'data':
      raise Exception('No data chunk at', open_file.tell())
    
    data_cksize = self._parse_int(open_file.read(4))
    channel_bits = int(nBlockAlign / self._num_channels)

    dtype = [np.uint8, np.uint16, np.uint32, np.uint64][channel_bits - 1] 

    self._data = np.array([
      [self._parse_int(open_file.read(channel_bits)) for j in range(self._num_channels)]
      for i in range(0, data_cksize, channel_bits)
    ], dtype = dtype)

def numpy_from_file(file_name):
  return WavReadFile(file_name).numpy 
