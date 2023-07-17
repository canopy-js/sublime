import sublime
import sublime_plugin

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyDefinitionSelectCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    index = CanopyInterfaceManager.get_cursor_position()

    reference = CanopyParseData.references_by_index[index]
    if not reference:
      sublime.status_message('Cursor must be on a reference')

    self.matching_subtopics = [
      subtopic
      for subtopic
      in CanopyParseData.subtopics
      if subtopic['name'] == reference['target']
    ]

    if len(self.matching_subtopics) > 1:
      CanopyInterfaceManager.create_quick_panel(
        self.generate_display_list(self.matching_subtopics),
        self.on_done
      )
    elif len(self.matching_subtopics) == 1:
      CanopyInterfaceManager.set_cursor_position(self.matching_subtopics[0]['start'])
    else:
      sublime.status_message('No matching definition found: ' + reference['target'])

  def on_done(self, selection_index):
    if selection_index > -1:
      selected_reference = self.matching_subtopics[selection_index]
      CanopyInterfaceManager.set_cursor_position(selected_reference['start'])

  def generate_display_list(self, subtopics):
    return [
    '[{category}] {display_subtopic}'.format(
        category=subtopic['category']['name'],
        display_subtopic=subtopic['display'],
      )
      for subtopic in subtopics
    ]
