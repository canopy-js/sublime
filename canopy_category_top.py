import sublime
import sublime_plugin
import re

class CanopyCategoryTopCommand(sublime_plugin.TextCommand):
  topic_definition = re.compile('(?:\\A|\n\n)(^\\*\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(?=\\s+|$)', re.M)
  subtopic_definition = re.compile('(?:\\A|\n\n)(^\\*?\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(?=\\s+|$)', re.M)
  category_definition = re.compile('(?:\\A|\n\n)(^\\[)([^\\]]+)\\]$', re.M)

  def run(self, edit):
    fileText = self.view.substr(sublime.Region(0, self.view.size()))
    category_matches = self.category_definition.finditer(fileText)
    category_top = previous((match.start() for match in category_matches if match.start() > self.view.sel()[0].begin()), self.view.size() - 1)

    self.view.sel().clear()
    self.view.sel().add(category_bottom)
    self.view.show(self.view.sel())
