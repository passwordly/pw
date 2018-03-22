import os
import configparser

from collections import OrderedDict
from passwordly import checkHash

class Config:
  def __init__(self, filename):
    self.parser = configparser.RawConfigParser()
    self.parser.add_section('config')
    self.filename = filename

  def read(self):
    self.parser.read(self.filename)

  def write(self):
    output_config = configparser.RawConfigParser()
    output_config.read_dict(OrderedDict({
      section: OrderedDict(sorted(values.items()))
      for section, values in sorted(self.parser.items())
    }))

    with open(self.filename+'.tmp', 'w') as configfile:
      output_config.write(configfile)

    os.rename(self.filename+'.tmp', self.filename)

  def getHashes(self):
    return self.parser.sections()

  def addHash(self, hash):
    self.parser.add_section(hash)

  def findHash(self, password):
    'Find a hash given the password'
    # Look for an existing hash
    for hash in self.getHashes():
      if hash[:4] == '$2a$' and checkHash(password, hash):
        return hash
    return None

  def get(self, hash, site):
    try:
      return self.parser.get(hash, site)
    except configparser.NoOptionError:
      return None

  def getSites(self, hash):
    return [site for (site, comment) in self.parser.items(hash)]

  def getAll(self, hash):
    return {site:comment for (site, comment) in self.parser.items(hash)}

  def set(self, hash, site, comment):
    self.parser.set(hash, site, comment)
