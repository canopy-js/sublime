import sublime
import sublime_plugin

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyCategoryTopCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    cursor_position = CanopyInterfaceManager.get_cursor_position()
    category = CanopyParseData.categories_by_index[cursor_position]
    if category['start'] != cursor_position:
      CanopyInterfaceManager.set_cursor_position(category['start'])
    else:
      category = CanopyParseData.categories[CanopyParseData.categories.index(category) - 1] if category in CanopyParseData.categories else None
      if category:
        CanopyInterfaceManager.set_cursor_position(category['start'])
