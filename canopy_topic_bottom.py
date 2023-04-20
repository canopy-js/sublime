import sublime
import sublime_plugin
import re

class CanopyTopicBottomCommand(sublime_plugin.TextCommand):
  topic_definition = re.compile('(?:\\A|\n\n)(^\\*\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(?=\\s+|$)', re.M)
  subtopic_definition = re.compile('(?:\\A|\n\n)(^\\*?\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(?=\\s+|$)', re.M)
  category_definition = re.compile('(?:\\A|\n\n)(^\\[)([^\\]]+)\\]$', re.M)
  topic_or_category_definition = re.compile(
    '(?:' +
    '(?:\\A|\n\n)(^\\*\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(\\s+|$)' + # topic def
    '|' +
    '(?:\\A|\n\n)(^\\[)([^\\]]+)\\]$' + # category def
    '(?:\n+\\* )(?:(?:.|\n)(?!\n\n^\\* )(?!\n\n(^\\[)([^\\]]+)\\]$))*' + # include up to one following topic def and all text until next category or topic
                                                                         # this causes jump to the next reasonable entry point
                                                                         # prior double newlines are necessary to allow subsequent cat/topic to be recognized
    ')', re.M)

  def run(self, edit):
    fileText = self.view.substr(sublime.Region(0, self.view.size()))
    topic_or_category_matches = self.topic_or_category_definition.finditer(fileText)
    topic_or_category_bottom_match = next((match for match in topic_or_category_matches if match.start() > self.view.sel()[0].begin()), self.view.size() - 1)
    print(re.findall(self.topic_or_category_definition, fileText))
    self.view.sel().clear()
    self.view.sel().add(topic_or_category_bottom_match.start())
    self.view.show(self.view.sel())
