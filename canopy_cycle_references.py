import sublime
import sublime_plugin
import re

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyCycleReferencesCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    index = CanopyInterfaceManager.get_cursor_position()
    current_reference = CanopyParseData.references_by_index[index]
    if not current_reference:
      sublime.status_message('Cursor must be on a reference')

    next_matching_reference = next(
      (
        reference for reference
        in CanopyParseData.references
        if reference['target'] == current_reference['target']
          and reference['start'] > index
      ), None
    )

    if not next_matching_reference:
      next_matching_reference = next(
        (
          reference for reference
          in CanopyParseData.references
          if reference['target'] == current_reference['target']
        ), None
      )

    if not next_matching_reference:
      sublime.status_message('No reference matches ' + reference['name'])
    else:
      CanopyInterfaceManager.set_cursor_position(next_matching_reference['start'])
