import sublime
import sublime_plugin
import re

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyJumpToGlobalDefinitionCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    index = CanopyInterfaceManager.get_cursor_position()
    reference = CanopyParseData.references_by_index[index]

    if not reference:
      sublime.status_message('Cursor must be on a reference')

    topic = CanopyParseData.topics_by_name.get(reference['target'])

    if not topic:
      sublime.status_message('No topic with name: ' + reference['target'])
    else:
      CanopyInterfaceManager.set_cursor_position(topic['start'])
