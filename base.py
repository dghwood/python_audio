import abc

class BaseAudioReadFile(abc.ABC):
  def __init__(self, file_name):
    self._file_name = file_name
    self._byte_order = 'little'
    self._read_file()
  
  def _read_file(self):
    with open(self._file_name, 'rb') as f:
      self._parse_file(f)

  @abc.abstractmethod
  def _parse_file(self, open_file):
    raise NotImplementedError(self, 'parse_file')
    
  def _parse_int(self, bytes_value):
    return int.from_bytes(bytes_value, 
                          self._byte_order)

  @property
  def file_name(self):
    return self._file_name

  @property
  @abc.abstractmethod
  def file_size(self):
    raise NotImplementedError(self, 'file_size')

  @property
  @abc.abstractmethod
  def num_channels(self):
    raise NotImplementedError(self, 'num_channels')

  @property
  @abc.abstractmethod
  def samples_per_sec(self):
    raise NotImplementedError(self, 'samples_per_sec')

  @property
  @abc.abstractmethod
  def numpy(self):
    raise NotImplementedError(self, 'numpy')