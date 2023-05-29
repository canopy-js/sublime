import sublime
import sublime_plugin
import re

class CanopyJumpToAllDefinitionCommand(sublime_plugin.TextCommand):
  topic_definition = re.compile('(?:\\A|\n\n)(^\\*\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(?=\\s+|$)', re.M)
  subtopic_definition = re.compile('(?:\\A|\n\n)(^\\*?\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(?=\\s+|$)', re.M)
  category_definition = re.compile('(?:\\A|\n\n)(^\\[)([^\\]]+)\\]$', re.M)
  reference = re.compile(r'\[\[((?:(?!(?<!\\)\]\]).)+)\]\]', re.S)

  def create_dict(self, subtopic_match, fileText):
    topic_match = self.enclosing_topic(subtopic_match.start(), fileText)
    category_match = self.enclosing_category(subtopic_match.start(), fileText)
    return {
      'start': subtopic_match.start(1),
      'name': subtopic_match.groups()[1],
      'enclosing_topic_name': topic_match.groups()[1],
      'enclosing_topic_start': topic_match.start(1),
      'enclosing_category_name': category_match.groups()[1],
      'enclosing_category_start': category_match.start(1)
    }
  def enclosing_topic(self, index_of_subtopic_definition, fileText):
    if (not re.search(self.topic_definition, fileText)):
      return None

    return min(
      (topic_match for topic_match in self.topic_definition.finditer(fileText) if (index_of_subtopic_definition - topic_match.start()) >= 0),
      key=lambda m: (index_of_subtopic_definition - m.start())
    )

  def enclosing_category(self, index_of_subtopic_definition, fileText):
    if (not re.search(self.category_definition, fileText)):
      return None

    return min(
      (category_match for category_match in self.category_definition.finditer(fileText) if (index_of_subtopic_definition - category_match.start()) >= 0),
      key=lambda m: (index_of_subtopic_definition - m.start())
    )

  def run(self, edit):
    current_selection = self.view.sel()[0]
    fileText = self.view.substr(sublime.Region(0, self.view.size()))
    current_reference_match = next((match for match in self.reference.finditer(fileText) if (match.start() - 1 < current_selection.begin() and match.end() > current_selection.end())), None)
    current_subtopic_match = next((match for match in self.subtopic_definition.finditer(fileText) if (match.start() - 1 < current_selection.begin() and match.end() > current_selection.end())), None)

    if (current_reference_match or current_subtopic_match): # We are hovering over a link
      target_string = self.render(current_reference_match.groups()[0] if current_reference_match else current_subtopic_match.groups()[1])

      self.matching_definitions = [self.create_dict(subtopic_match, fileText)
        for subtopic_match
        in re.finditer(self.subtopic_definition, fileText)
        if self.remove_markdown(subtopic_match.groups()[1]).upper() == self.remove_markdown(target_string).upper()]

      sublime.active_window().show_quick_panel(
        [self.display_string(def_dict) for def_dict in self.matching_definitions], self.on_done
      )

    else:
      sublime.status_message('Cursor needs to be on reference!')
      return

  def on_done(self, index):
    if (index > -1):
      self.view.sel().clear()
      self.view.sel().add(self.matching_definitions[index]['start'])
      self.view.show(self.view.sel())

  def remove_markdown(self, string):
    return string.replace('*', '')\
      .replace('_', '')\
      .replace('~', '')\
      .replace('`', '')\
      .replace('\n<', '')\
      .replace('\n>', '')\
      .replace('(', '')\
      .replace(')', '')\
      .replace('\'', '')\
      .replace('"', '')\
      .replace('‘', '')\
      .replace('’', '')\
      .replace('“', '')\
      .replace('”', '')

  def render(self, linkContents):
      target_string = '';
      exclusive_target_string = '';
      exclusive_display_syntax = False;

      segments = re.findall(r'(((?<!\\)\{\{?)((?:(?!(?<!\\)\}).)+)((?<!\\)\}\}?)|((?:(?!(?<!\\)[{}]).)+))', linkContents, re.S);
      for segment in segments:
        if (re.search(r'(?<!\\)\{', segment[0])): # if there are braces at all
          if (segment[4]): # plaintext segment
            target_string += segment[4];
          if (segment[1] == '{'):
            pipe_segments = re.split(r'(?<!\\)\|', segment[2])
            if (len(pipe_segments) == 2): # interpolation syntax
              target_string += pipe_segments[0]
              exclusive_target_string += pipe_segments[0]
            else: # exclusive display string syntax {{a}}
              target_string += pipe_segments[0]
          elif (segment[1] == '{{'): # exclusive target syntax
            exclusive_target_string += segment[2]
            exclusive_display_syntax = True
        elif(re.search(r'(?<!\\)\|', segment[0])):
          pipe_segments = re.split(r'(?<!\\)\|', segment[0])
          target_string = pipe_segments[0] # whether there is a pipe or isn't
        else: # plaintext link
          target_string += segment[0]

      target_string = exclusive_target_string if exclusive_display_syntax else target_string
      target_string = target_string[:1].upper() + target_string[1:]
      return target_string

  def display_string(self, subtopic):
    return '[{}] {}{}{}'.format(
      subtopic['enclosing_category_name'],
      subtopic['enclosing_topic_name'] if subtopic['enclosing_topic_name'] != subtopic['name'] else '',
      ': ' if (subtopic['enclosing_topic_name'] != subtopic['name'] and (not subtopic['enclosing_topic_name'].endswith('?'))) else '',
      subtopic['name']
    )
