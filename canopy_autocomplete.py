import sublime
import sublime_plugin
import re

class CanopyAutocompleteCommand(sublime_plugin.TextCommand):
  topic_definition = re.compile('(?:\\A|\n\n)(^\\*\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(?=\\s+|$)', re.M)
  subtopic_definition = re.compile('(?:\\A|\n\n)(^\\*?\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(?=\\s+|$)', re.M)
  category_definition = re.compile('(?:\\A|\n\n)(^\\[)([^\\]]+)\\]$', re.M)

  def run(self, edit):
    fileText = self.view.substr(sublime.Region(0, self.view.size()))

    def create_dict(subtopic_match):
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

    self.subtopics = [ subtopic_dict for subtopic_dict in
      (create_dict(subtopic_match) for subtopic_match in self.subtopic_definition.finditer(fileText))
      if subtopic_dict['enclosing_topic_start'] > subtopic_dict['enclosing_category_start']
    ]

    if (len(self.subtopics) == 0):
      sublime.status_message('No Subtopics!')
      return

    if (len(re.findall(self.category_definition, fileText)) == 0):
      sublime.status_message('No Categories!')
      return

    sublime.active_window().show_quick_panel(
      [self.display_string(subtopic) for subtopic in self.subtopics], self.on_done
    )

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
      key=lambda m: (index_of_subtopic_definition - m.start())
    )

  def on_done(self, index):
    if (index > -1):
      self.view.sel().clear()
      self.view.sel().add(self.subtopics[index]['start'])
      self.view.show(self.view.sel())

  def display_string(self, subtopic):
    return '[{}] {}{}{}'.format(
      subtopic['enclosing_category_name'],
      subtopic['enclosing_topic_name'] if subtopic['enclosing_topic_name'] != subtopic['name'] else '',
      ': ' if (subtopic['enclosing_topic_name'] != subtopic['name'] and (not subtopic['enclosing_topic_name'].endswith('?'))) else '',
      subtopic['name']
    )

  def on_done(self, index):
    if (index > -1):
      self.view.run_command("insert", {"characters": self.subtopics[index]['name']})
