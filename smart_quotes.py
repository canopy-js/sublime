import sublime, sublime_plugin
import re
import os
import sys
import importlib

class SmartQuotesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    for selection in self.view.sel():
      if (selection.empty()):
        selection = self.view.line(self.view.sel()[0])
      selection_text = self.view.substr(selection)
      new_text = re.sub(r"([\s()[\]\[{}]|^)\"([^\"]*)\"", r"\1“\2”", selection_text)
      new_text = re.sub(r"([\s()[\]\[{}]|^)\'([^\']*)\'", r"\1‘\2’", new_text)

      #new_text = re.sub(r"([\s()[\]\[]|^)\"([^\"]*)\"", r"\1“\2”", selection_text)
      new_text = re.sub(r"\'", r"’", new_text)

      self.view.replace(edit, selection, new_text)

# This is a “test”
