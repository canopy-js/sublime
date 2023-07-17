import sublime
import sublime_plugin
import re

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyTopicTopCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    cursor_position = CanopyInterfaceManager.get_cursor_position()
    topic = CanopyParseData.topics_by_index[cursor_position]
    if not topic:
      return

    if topic['start'] != cursor_position:
      CanopyInterfaceManager.set_cursor_position(topic['start'])
    else:
      topic = CanopyParseData.topics[CanopyParseData.topics.index(topic) - 1] if topic in CanopyParseData.topics else None
      if topic:
        CanopyInterfaceManager.set_cursor_position(topic['start'])
