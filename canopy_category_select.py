import sublime
import sublime_plugin

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyCategorySelectCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    CanopyInterfaceManager.create_quick_panel(
      self.generate_display_list(CanopyParseData.categories),
      self.on_done,
      CanopyParseData.categories_by_index[CanopyInterfaceManager.get_cursor_position()
      ]['index']
    )

  def on_done(self, selection_index):
    if selection_index > -1:
      category = CanopyParseData.categories[selection_index]
      CanopyInterfaceManager.set_cursor_position(category['start'])

  def generate_display_list(self, categories):
    return [category['name'] for category in categories]
