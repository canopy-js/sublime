import sublime
import sublime_plugin
import re

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyCategoryBottomCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    cursor_position = CanopyInterfaceManager.get_cursor_position()
    category = CanopyParseData.categories_by_index[cursor_position]
    if category['end'] != cursor_position:
      CanopyInterfaceManager.set_cursor_position(category['end'])
    else:
      if cursor_position + 1 < CanopyInterfaceManager.file_length():
        category = CanopyParseData.categories_by_index[cursor_position + 1]
        CanopyInterfaceManager.set_cursor_position(category['end'])
