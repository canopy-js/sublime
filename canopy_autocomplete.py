import sublime
import sublime_plugin

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyAutocompleteCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    CanopyInterfaceManager.create_quick_panel(
      self.generate_display_list(CanopyParseData.subtopics),
      self.on_done
    )

  def on_done(self, selection_index):
    if selection_index > -1:
      selected_topic = CanopyParseData.subtopics[selection_index]
      CanopyInterfaceManager.insert(selected_topic['name'])

  def generate_display_list(self, subtopics):
    return [
      subtopic['display'] for subtopic in subtopics
    ]
