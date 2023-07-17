import sublime
import sublime_plugin
import re

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopySubtopicSelectCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    CanopyInterfaceManager.create_quick_panel(
      self.generate_display_list(CanopyParseData.subtopics),
      self.on_done
    )

  def on_done(self, selection_index):
    if selection_index > -1:
      selected_topic = CanopyParseData.subtopics[selection_index]
      CanopyInterfaceManager.set_cursor_position(selected_topic['start'])

  def generate_display_list(self, subtopics):
    return [subtopic['display'] for subtopic in subtopics]
