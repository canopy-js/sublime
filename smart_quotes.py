import sublime, sublime_plugin
import re

class SmartQuotesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    for selection in self.view.sel():
      if (selection.empty()):
        selection = self.view.line(self.view.sel()[0])
      selection_text = self.view.substr(selection)
      new_text = re.sub(r"([\s()[\]]|^)\"([^\"]*)\"", r"\1“\2”", selection_text)
      self.view.replace(edit, selection, new_text)
      print(new_text, 123)

# This is a “test”
