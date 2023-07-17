import sublime
import sublime_plugin
import re

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyJumpToLocalDefinitionCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    index = CanopyInterfaceManager.get_cursor_position()
    reference = CanopyParseData.references_by_index[index]
    current_topic = CanopyParseData.topics_by_index[index]

    if not reference:
      sublime.status_message('Cursor must be on a reference')

    target_subtopic = next(
      (subtopic
      for subtopic
      in CanopyParseData.subtopics
      if subtopic['topic']['name'] == current_topic['name']
        and subtopic['name'] == reference['target']
      ), None
    )

    if not target_subtopic:
      sublime.status_message('No subtopic in topic [' + current_topic['name'] + '] with name [' + reference['target'] + ']')
    else:
      CanopyInterfaceManager.set_cursor_position(target_subtopic['start'])
