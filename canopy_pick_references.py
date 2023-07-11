import sublime
import sublime_plugin
import re

class CanopyPickReferencesCommand(sublime_plugin.TextCommand):
  topic_definition = re.compile('(?:\\A|\n\n)(^\\*\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(?=\\s+|$)', re.M)
  subtopic_definition = re.compile('(?:\\A|\n\n)(^\\*?\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(?=\\s+|$)', re.M)
  category_definition = re.compile('(?:\\A|\n\n)(^\\[)([^\\]]+)\\]$', re.M)
  reference = re.compile(r'\[\[((?:(?!(?<!\\)\]\]).)+)\]\]', re.S)

  def run(self, edit):
    current_selection = self.view.sel()[0]
    fileText = self.view.substr(sublime.Region(0, self.view.size()))

    if (len(re.findall(self.category_definition, fileText)) == 0):
      sublime.status_message('No Categories!')
      return

    if (len(re.findall(self.topic_definition, fileText)) == 0):
      sublime.status_message('No Topics!')
      return

    if (len(re.findall(self.topic_definition, fileText)) == 0):
      sublime.status_message('No Subtopics!')
      return

    current_reference_match = next((match for match in self.reference.finditer(fileText) if (match.start() <= current_selection.begin() and match.end() > current_selection.end())), None)
    current_subtopic_match = next((match for match in self.subtopic_definition.finditer(fileText) if (match.start() <= current_selection.begin() and match.end() > current_selection.end())), None)
    def create_dict(reference_match):
      topic_match = self.enclosing_topic(reference_match.start(), fileText)
      subtopic_match = self.enclosing_subtopic(reference_match.start(), fileText)
      category_match = self.enclosing_category(reference_match.start(), fileText)
      return {
        'start': reference_match.start(),
        'text': reference_match.groups()[0].replace('\n<', '').replace('\n>', '').replace('\n', ' '),
        'enclosing_topic_name': topic_match.groups()[1],
        'enclosing_topic_start': topic_match.start(1),
        'enclosing_subtopic_name': subtopic_match.groups()[1],
        'enclosing_subtopic_start': subtopic_match.start(1),
        'enclosing_category_name': category_match.groups()[1],
        'enclosing_category_start': category_match.start(1)
      }

    if (current_reference_match or current_subtopic_match): # We are hovering over a link or definition
      target_string = self.render(current_reference_match.groups()[0] if current_reference_match else current_subtopic_match.groups()[1])

      self.matching_references = [reference_dict for reference_dict in
        (create_dict(reference_match) for reference_match in self.reference.finditer(fileText))
        if reference_dict['enclosing_topic_start'] > reference_dict['enclosing_category_start'] and self.render(reference_dict['text']).upper() == target_string.upper()
      ]

      if (len(self.matching_references) == 0):
        sublime.status_message('No matching references!')
        return

      if (len(self.matching_references) == 1):
        self.view.sel().clear()
        self.view.sel().add(self.matching_references[0]['start'])
        self.view.show(self.view.sel())
        return

      sublime.active_window().show_quick_panel(
        [self.display_string(matching_reference) for matching_reference in self.matching_references], self.on_done
      )

    else:
      sublime.status_message('Cursor needs to be on definition or reference!')
      return

  def enclosing_category(self, index_of_subtopic_definition, fileText):
    if (not re.search(self.category_definition, fileText)):
      return None

    return min(
      (category_match for category_match in self.category_definition.finditer(fileText) if (index_of_subtopic_definition - category_match.start()) >= 0),
      key=lambda m: (index_of_subtopic_definition - m.start())
    )

  def enclosing_topic(self, index_of_subtopic_definition, fileText):
    if (not re.search(self.topic_definition, fileText)):
      return None

    return min(
      (topic_match for topic_match in self.topic_definition.finditer(fileText) if (index_of_subtopic_definition - topic_match.start()) >= 0),
      key=lambda m: (index_of_subtopic_definition - m.start(1))
    )

  def enclosing_subtopic(self, index_of_subtopic_definition, fileText):
    if (not re.search(self.subtopic_definition, fileText)):
      return None

    return min(
      (subtopic_definition for subtopic_definition in self.subtopic_definition.finditer(fileText) if (index_of_subtopic_definition - subtopic_definition.start()) >= 0),
      key=lambda m: (index_of_subtopic_definition - m.start(1))
    )

  def on_done(self, index):
    if (index > -1):
      self.view.sel().clear()
      self.view.sel().add(self.matching_references[index]['start'])
      self.view.show(self.view.sel())

  def display_string(self, matching_reference):
    return '[{}] {}{}{}'.format(
      matching_reference['enclosing_category_name'],
      matching_reference['enclosing_topic_name'] if matching_reference['enclosing_topic_name'] != matching_reference['text'] else '',
      ': ' if (matching_reference['enclosing_topic_name'] != matching_reference['text'] and (not matching_reference['enclosing_topic_name'].endswith('?'))) else '',
      matching_reference['enclosing_subtopic_name']
    )

  def render(self, linkContents):
      target_string = '';
      exclusive_target_string = '';
      exclusive_display_syntax = False;

      segments = re.findall(r'(((?<!\\)\{\{?)((?:(?!(?<!\\)\}).)+)((?<!\\)\}\}?)|((?:(?!(?<!\\)[{}]).)+))', linkContents);
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
