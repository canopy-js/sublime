import sublime
import sublime_plugin
import re
import inspect

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyPickJumpCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    if len(CanopyParseData.jump_list) > 0:
      CanopyInterfaceManager.create_quick_panel(
        self.generate_display_list(CanopyParseData.jump_list),
        self.on_done
      )
    else:
      sublime.status_message('No jumps yet')

  def on_done(self, selection_index):
    if selection_index > -1:
      selection = CanopyParseData.jump_list[selection_index]

      if (selection['topic'] and not selection['subtopic']) or (selection['subtopic'] and selection['topic'] == selection['subtopic']):
        index = CanopyParseData.topics_by_name[selection['topic']]['start']
      elif not selection['topic']:
        index = CanopyParseData.categories_by_name[selection['category']]['start']
      else:
        index = CanopyParseData.subtopics_by_name[selection['subtopic']]['start']

      CanopyInterfaceManager.set_cursor_position(index)

  def generate_display_list(self, jump_list):
    return ['{category}{topic} {subtopic}'.format(
      category='[' + jump['category'] + ']' if (not jump['topic'] and not jump['subtopic']) else '',
      topic='(' + jump['topic'] + ')' if jump['topic'] else '',
      subtopic=jump['subtopic'] if jump['subtopic'] else ''
    ) for jump in jump_list]
