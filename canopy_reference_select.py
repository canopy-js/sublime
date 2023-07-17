import sublime
import sublime_plugin
import re

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyReferenceSelectCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    CanopyInterfaceManager.create_quick_panel(
      self.generate_display_list(CanopyParseData.references),
      self.on_done
    )

  def on_done(self, selection_index):
    if selection_index > -1:
      selected_topic = CanopyParseData.references[selection_index]
      CanopyInterfaceManager.set_cursor_position(selected_topic['start'])

  def generate_display_list(self, references):
    return [
    '[{category}] {display_subtopic}: {reference}'.format(
        category=reference['category']['name'],
        display_subtopic=reference['subtopic']['display'],
        reference=reference['text']
      )
      for reference in references
    ]
