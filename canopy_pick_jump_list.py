import sublime
import sublime_plugin
import re
import inspect

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyPickJumpListCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    print(CanopyParseData.jump_list())
    CanopyInterfaceManager.create_quick_panel(
      self.generate_display_list(CanopyParseData.jump_list()),
      self.on_done
    )

  def on_done(self, selection_index):
    selection = CanopyParseData.jump_list()[selection_index]

    if (not selection[2]) or selection[1] == selection[2]:
      index = CanopyParseData.topics_by_name()[selection[1]]['start']
    elif not selection[1]:
      index = CanopyParseData.categories_by_name()[selection[0]]['start']
    else:
      index = CanopyParseData.subtopics_by_name()[selection[2]]['start']

    print(index)
    CanopyInterfaceManager.set_cursor_position(index)

  def generate_display_list(self, jump_list):
    return ['[{category}] ({topic}) {subtopic}'.format(category=jump[0], topic=jump[1], subtopic=jump[2]) for jump in jump_list]
