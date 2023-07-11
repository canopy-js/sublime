import sublime
import sublime_plugin
import re

class CanopyCategorySelectCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    fileText = self.view.substr(sublime.Region(0, self.view.size()))
    definition = re.compile('^\\[([^^][^\\]]+)\\]', re.M)
    self.tuples = [[m.start(), m.groups()] for m in definition.finditer(fileText)]
    if (len(self.tuples) == 0):
      sublime.status_message('No Categories!')
      return
    sublime.active_window().show_quick_panel(
      [tuple[1] for tuple in self.tuples], self.on_done
    )

  def on_done(self, index):
    if (index > -1):
      self.view.sel().clear()
      self.view.sel().add(self.tuples[index][0])
      self.view.show(self.view.sel())

  def find_enclosing_topic(self, index_of_subtopic_definition, fileText):
    topic_definition = re.compile('^\\*?\\*? ?(\\S[^\n]+(?=\\?|\\:)\\??):?(?=>\\s+|$)')
    return min(
      (topic_match for topic_match in topic_definition.finditer(fileText) if (index_of_subtopic_definition - topic_match.start()) >= 0),
      key=lambda m: (index_of_subtopic_definition - m.start())
    ).groups()[0]

  def display_string(self, index_of_subtopic_definition, fileText, match_text):
    return '{}: {}'.format(self.find_enclosing_topic(index_of_subtopic_definition, fileText), match_text)
