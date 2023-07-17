import sublime
import sublime_plugin
import re
import inspect

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyPickEditCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    if len(CanopyParseData.edit_list) > 0:
      CanopyInterfaceManager.create_quick_panel(
        self.generate_display_list(CanopyParseData.edit_list),
        self.on_done
      )
    else:
      sublime.status_message('No edits yet')

  def on_done(self, selection_index):
    if selection_index > -1:
      selection = CanopyParseData.edit_list[selection_index]

      if (selection['topic'] and not selection['subtopic']) or (selection['subtopic'] and selection['topic'] == selection['subtopic']):
        index = CanopyParseData.topics_by_name[selection['topic']]['start']
      elif not selection['topic']:
        index = CanopyParseData.categories_by_name[selection['category']]['start']
      else:
        index = CanopyParseData.subtopics_by_name[selection['subtopic']]['start']

      CanopyInterfaceManager.set_cursor_position(index)

  def generate_display_list(self, edit_list):
    return ['{category}{topic} {subtopic}'.format(
      category='[' + str(edit['category']) + ']' if (not edit['topic'] and not edit['subtopic']) else '',
      topic='(' + str(edit['topic']) + ')' if edit['topic'] else '',
      subtopic=edit['subtopic'] if edit['subtopic'] else ''
    ) for edit in edit_list]
