import sublime
import sublime_plugin
import re

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyJumpToReferenceCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    index = CanopyInterfaceManager.get_cursor_position()
    subtopic = CanopyParseData.subtopics_by_index[index]
    references = [
      reference
      for reference
      in CanopyParseData.references
      if reference['target'] == subtopic['name']
    ]

    if len(references) > 1:
      CanopyInterfaceManager.create_quick_panel(
        self.generate_display_list(references),
        self.on_done
      )
    elif len(references) == 1:
      CanopyInterfaceManager.set_cursor_position(references[0]['start'])
    else:
      sublime.status_message('No matching references found: ' + subtopic['name'])

  def on_done(self, selection_index):
    if selection_index > -1:
      selected_reference = CanopyParseData.references[selection_index]
      CanopyInterfaceManager.set_cursor_position(selected_reference['start'])

  def generate_display_list(self, references):
    return [
    '[{category}] {display_subtopic}: {reference}'.format(
        category=reference['category']['name'],
        display_subtopic=reference['subtopic']['display'],
        reference=reference['text']
      )
      for reference in references
    ]
