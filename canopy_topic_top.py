import sublime
import sublime_plugin
import re

from .canopy_parse_data import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyTopicTopCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    interfaceManager = CanopyInterfaceManager(self.view)
    cursor_position = interfaceManager.get_cursor_position()
    topic = CanopyParseData.topics_by_index[cursor_position]
    interfaceManager.set_cursor_position(topic['start'])
