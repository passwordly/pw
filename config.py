import os
import ConfigParser

from passwordly import checkHash

class Config:
  def __init__(self, filename):
    self.parser = ConfigParser.RawConfigParser()
    self.filename = filename

  def read(self):
    self.parser.read(self.filename)

  def write(self):
    with open(self.filename+'.tmp', 'w') as configfile:
      self.parser.write(configfile)

    os.rename(self.filename+'.tmp', self.filename)

  def getHashes(self):
    return self.parser.sections()

  def addHash(self, hash):
    self.parser.add_section(hash)

  def findHash(self, password):
    'Find a hash given the password'
    # Look for an existing hash
    for hash in self.getHashes():
      if checkHash(password, hash):
        return hash
    return None

  def get(self, hash, site):
    try:
      return self.parser.get(hash, site)
    except ConfigParser.NoOptionError:
      return None

  def getAll(self, hash):
    return {site:comment for (site, comment) in self.parser.items(hash)}

  def set(self, hash, site, comment):
    self.parser.set(hash, site, comment)
