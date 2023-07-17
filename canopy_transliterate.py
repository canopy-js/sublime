def transliterate(string):
  """"Transliterates Hebrew sections in a string, including final letters.

  Args:
    string: The string to transliterate.

  Returns:
    A list of the transliterated sections.
  """

  transliteration_table = {
    "א": "a",
    "ב": "b",
    "ג": "g",
    "ד": "d",
    "ה": "h",
    "ו": "vou",
    "ז": "z",
    "ח": "ch",
    "ט": "t",
    "י": "y",
    "כ": "ch",
    "ל": "l",
    "מ": "m",
    "נ": "n",
    "ס": "s",
    "ע": "e",
    "פ": "p",
    "צ": "tz",
    "ק": "k",
    "ר": "r",
    "ש": "sh",
    "ת": "st",
    "ם": "m",
    "ן": "n",
    "ץ": "tz",
    "ף": "p",
    "ך": "ch",
  }

  result = ""
  current_transliteration = ""

  for character in string:
    if (character in transliteration_table) or (character == ' ' and current_transliteration):
      result += character
      if character == ' ':
        current_transliteration += ' '
      else:
        current_transliteration += transliteration_table[character]
    else:
      if current_transliteration:
        result += current_transliteration
        current_transliteration = ""
      result += character

  if current_transliteration:
      result += ' ' + current_transliteration

  return result
