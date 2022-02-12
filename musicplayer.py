"""
A lot of this stuff is super early prototype stage and undocumented because i dont care, and nobody should not use this code with the current state that it is in.

non standard documentation patterns? ✔
variables and functions that arent used? ✔
variables and functions missing explinations for what i am attemtping to do for the future? ✔
python just looks... slightly offputting? ✔
hardcoded variables? ✔
only works on windows os? ✔
dosent even work for all music file types - or idk why i get  errors yet? ✔
uncertain for why my pc gets "The specified device is not open or is not recognized by MCI." errors? ✔
forgot to properly credit where i took parts of my code from? ✔ (https://github.com/TaylorSMarks/playsound/blob/master/playsound.py)
missing full documentation for how to use it? ✔

v Feb 12, 2022
"""

class Music_Player():
  """
  """
  __is_playing = False
  __controls_pressed = []
  __volume = 0.3

  do_shuffle = True
  
  def __init__(self):
    self.mood = None
    self.library = {}
    self.playlists = {}
    self.do_shuffle = True
  
  def update_mood(self):
    """
    Updates mood/playlist
    """
    valid_keys = {}
    for n in self.playlists:
      keys = set()
      for k in self.playlists[n]['keys']:
        if k not in valid_keys:
          valid_keys[k] = n
          keys.add(k)
      print(f"{n}\t{', '.join(keys)}")
    if valid_keys == {}:
      print("ERROR: Library hasnt been loaded in yet!")
      return
    
    inp = None
    while inp not in valid_keys:
      inp = input("Enter mood code here:").strip().lower()
    self.mood = valid_keys[inp]
    
    inp = None
    t=['y','yes','t','true']
    f=['n','no','f','false']
    while not (inp in t or inp in f):
      inp = input("Do shuffle? ")
    if inp in t:
      self.do_shuffle = True
    elif inp in f:
      self.do_shuffle = False
  
  def update_music_library(self):
    """
    sets self.library to the following:
      {
        '<artist>':
          {
            '<song name>':
              {
                'file': '<file path>'
                'playlists' : [<playlist/mood names>]
              }
          }
      }
    sets the self.playlists too.
    """
    from os import walk
    from os.path import join as pathjoin
    self.library = {}
    for subdir, dirs, files in walk("<PATH TO PARENT DIRECTORY WITH MUSIC FILES/SUBDIRECTORIES>"):
      if subdir not in self.library and subdir not in ['','__PLAYLISTS']:
        self.library[subdir] = {}
      for file in files:
        self.library[subdir][file]={'file':pathjoin(subdir, file)}
    
    self.playlists = {}
    for subdir, dirs, files in walk("<PATH TO __PLAYLIST FILE DIRECTORY>"):
      for file in files:
        if file.lower().endswith(".pyplayerplaylist"):
          playlist_name = file.lower().replace(".pyplayerplaylist","")
          self.playlists[playlist_name] = {'keys':[],'songs':[]}
          with open(subdir + "\\" + file, "r", encoding='utf-8') as f:
            data = f.read().split("\n")
            if data[0].startswith("#"):
              self.playlists[playlist_name]['keys'] = [v.lower() for v in data[0].split("#") if v]
              del data[0]
            self.playlists[playlist_name]['songs'] = [l for l in data if l]
    
    del walk
    del pathjoin
  
  def winCommand(self, *command):
    """
    helper func to run windows commands
    """
    bufLen = 600
    buf = create_unicode_buffer(bufLen)
    command = ' '.join(command)
    errorCode = int(windll.winmm.mciSendStringW(command, buf, bufLen - 1, 0))  # use widestring version of the function
    if errorCode:
      errorBuffer = create_unicode_buffer(bufLen)
      windll.winmm.mciGetErrorStringW(errorCode, errorBuffer, bufLen - 1)  # use widestring version of the function
      exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:\n        ' + command + '\n    ' + errorBuffer.value)
      print(exceptionMessage)
      raise Exception(exceptionMessage)
    return buf.value
  
  def play_file(self, filepath, block = True):
    """
    Plays the sound
    """
    try:
      self.winCommand(u'open {}'.format(filepath))
      self.winCommand(u'play {}{}'.format(filepath, ' wait' if block else ''))
    finally:
      try:
        self.winCommand(u'close {}'.format(filepath))
      except Exception:
        # If it fails, there's nothing more that can be done...
        print(u'Failed to close the file: {}'.format(filepath))
  
  def start(self):
    """
    starts playing the currently selected playlist/mood
    """
    if self.mood not in self.playlists:
      print("NEED TO SET THE MOOD")
      self.update_mood()
    print("Playing... ")
    ordered_playlist = self.playlists[self.mood]['songs']
    if self.do_shuffle:
      shuffle(self.playlists[self.mood]['songs'])
    
    for song in ordered_playlist:
      print(f"Playing song: {song}")
      try:
        self.play_file(song)
      except:
        print(f"error?! {song}")
      
if __name__ == "__main__":
  from ctypes import create_unicode_buffer
  from ctypes.wintypes import LPCWSTR, LPWSTR, UINT, HANDLE, DWORD
  from ctypes import windll
  from turtle import update
  from random import shuffle
  windll.winmm.mciSendStringW.argtypes = [LPCWSTR, LPWSTR, UINT, HANDLE]  # error prob coming from something that has to do with whatever this is
  windll.winmm.mciGetErrorStringW.argtypes = [DWORD, LPWSTR, UINT]
  player = Music_Player()
  player.update_music_library()
  player.update_mood()
  player.start()


