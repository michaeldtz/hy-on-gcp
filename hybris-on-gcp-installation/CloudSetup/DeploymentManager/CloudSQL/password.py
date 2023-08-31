
import random
import yaml

PROPERTY_LENGTH = 'length'
PROPERTY_INCLUDE_SYMBOLS = 'includeSymbols'

# Note the omission of some hard to distinguish characters like I, l, 0, and O.
UPPERS = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
LOWERS = 'abcdefghijkmnopqrstuvwxyz'
ALPHABET = UPPERS + LOWERS
DIGITS = '123456789'
ALPHANUMS = ALPHABET + DIGITS
# Including only symbols that can be passed around easily in shell scripts.
SYMBOLS = '*-+.'

CANDIDATES_WITH_SYMBOLS = ALPHANUMS + SYMBOLS
CANDIDATES_WITHOUT_SYMBOLS = ALPHANUMS

CATEGORIES_WITH_SYMBOLS = [UPPERS, LOWERS, DIGITS, SYMBOLS]
CATEGORIES_WITHOUT_SYMBOLS = [UPPERS, LOWERS, DIGITS]

MIN_LENGTH = 8


class InputError(Exception):
  """Raised when input properties are unexpected."""


def GenerateConfig(context):
  """Entry function to generate the DM config."""
  props = context.properties
  length = props.setdefault(PROPERTY_LENGTH, MIN_LENGTH)
  include_symbols = props.setdefault(PROPERTY_INCLUDE_SYMBOLS, False)

  if not isinstance(include_symbols, bool):
    raise InputError('%s must be a boolean' % PROPERTY_INCLUDE_SYMBOLS)

  content = {
      'resources': [],
      'outputs': [{
          'name': 'password',
          'value': GeneratePassword(length, include_symbols)
      }]
  }
  return yaml.dump(content)


def GeneratePassword(length=8, include_symbols=False):
  """Generates a random password."""
  if length < MIN_LENGTH:
    raise InputError('Password length must be at least %d' % MIN_LENGTH)

  candidates = (CANDIDATES_WITH_SYMBOLS if include_symbols
                else CANDIDATES_WITHOUT_SYMBOLS)
  categories = (CATEGORIES_WITH_SYMBOLS if include_symbols
                else CATEGORIES_WITHOUT_SYMBOLS)

  # Generates up to the specified length minus the number of categories.
  # Then inserts one character for each category, ensuring that the character
  # satisfy the category if the generated string hasn't already.
  generated = ([random.choice(ALPHABET)] +
               [random.choice(candidates)
                for _ in range(length - 1 - len(categories))])
  for category in categories:
    _InsertAndEnsureSatisfaction(generated, category, candidates)
  return ''.join(generated)


def _InsertAndEnsureSatisfaction(generated, required, all_candidates):
  """Inserts 1 char into generated, satisfying required if not already.

  If the required characters are not already in the generated string, one will
  be inserted. If any required character is already in the generated string, a
  random character from all_candidates will be inserted. The insertion happens
  at a random location but not at the beginning.

  Args:
    generated: the string to be modified.
    required: list of required characters to check for.
    all_candidates: list of characters to choose from if the required characters
        are already satisfied.
  """
  if set(generated).isdisjoint(required):
    # Not yet satisfied. Insert a required candidate.
    _InsertInto(generated, required)
  else:
    # Already satisfied. Insert any candidate.
    _InsertInto(generated, all_candidates)


def _InsertInto(generated, candidates):
  """Inserts a random candidate into a random non-zero index of generated."""
  # Avoids inserting at index 0, since the first character follows its own rule.
  generated.insert(random.randint(1, len(generated) - 1),
                   random.choice(candidates))