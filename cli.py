import readline

def ask(question, answers={"yes":True,"y":True,"no":False,"n":False}):
  'Ask a yes/no (or similar) question on the command line'
  while True:
    answer = raw_input(question).lower().strip()

    if answer in answers:
      return answers[answer]
    else:
      print 'Your answer was not recognised'

def read_autocomplete(prefix, options):
  def completer(text, state):
    completions = [i for i in options if i.startswith(text)]
    if state < len(completions):
      return completions[state]
    else:
      return None

  readline.parse_and_bind("tab: complete")
  readline.set_completer(completer)

  result = raw_input(prefix)

  readline.set_completer(lambda text, state: None)

  return result

