import sublime
import sublime_plugin

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyTopicSelectCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    CanopyInterfaceManager.create_quick_panel(
      self.generate_display_list(CanopyParseData.topics),
      self.on_done,
      (CanopyParseData.topics_by_index[
        CanopyInterfaceManager.get_cursor_position()
      ] or {}).get('index') or 0
    )

  def on_done(self, selection_index):
    if selection_index > -1:
      selected_topic = CanopyParseData.topics[selection_index]
      CanopyInterfaceManager.set_cursor_position(selected_topic['start'])

  def generate_display_list(self, topics):
    return [topic['name'] for topic in topics]
