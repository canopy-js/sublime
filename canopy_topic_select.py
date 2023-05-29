import sublime
import sublime_plugin
import re

class CanopyTopicSelectCommand(sublime_plugin.TextCommand):
  topic_definition = re.compile('(?:\\A|\n\n)(^\\*\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(?=\\s+|$)', re.M)
  category_definition = re.compile('(?:\\A|\n\n)(^\\[)([^\\]]+)\\]$', re.M)

  def run(self, edit):
    fileText = self.view.substr(sublime.Region(0, self.view.size()))

    def create_dict(topic_match):
      category_match = self.enclosing_category(topic_match.start(), fileText)
      return {
        'start': topic_match.start(1),
        'name': topic_match.groups()[1],
        'enclosing_category_name': category_match.groups()[1],
        'enclosing_category_start': category_match.start(1)
      }

    self.topics = [ topic_dict for topic_dict in
      (create_dict(topic_match) for topic_match in self.topic_definition.finditer(fileText))
    ]

    if (len(self.topics) == 0):
      sublime.status_message('No Subtopics!')
      return

    if (len(re.findall(self.category_definition, fileText)) == 0):
      sublime.status_message('No Categories!')
      return

    sublime.active_window().show_quick_panel(
      [self.display_string(subtopic) for subtopic in self.topics], self.on_done
    )

  def enclosing_category(self, index_of_subtopic_definition, fileText):
    if (not re.search(self.category_definition, fileText)):
      return None

    return min(
      (category_match for category_match in self.category_definition.finditer(fileText) if (index_of_subtopic_definition - category_match.start()) >= 0),
      key=lambda m: (index_of_subtopic_definition - m.start())
    )

  def on_done(self, index):
    if (index > -1):
      self.view.sel().clear()
      self.view.sel().add(self.topics[index]['start'])
      self.view.show(self.view.sel())

  def display_string(self, topic):
    return '{}'.format(
      topic['name']
    )
