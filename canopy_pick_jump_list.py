import sublime
import sublime_plugin
import re
import inspect

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyPickJumpListCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    CanopyInterfaceManager.create_quick_panel(
      self.generate_display_list(CanopyParseData.jump_list()),
      self.on_done
    )

  def on_done(self, selection_index):
    selection_tuple = CanopyParseData.jump_list()[selection_index]

    if selection_tuple[1] == selection_tuple[2]: # topic
      index = CanopyParseData.topics_by_name()[selection_tuple[1]]['start']
    else:
      index = CanopyParseData.subtopics_by_name()[selection_tuple[2]]['start']

    CanopyInterfaceManager.set_cursor_position(index)

  def generate_display_list(self, jump_list):
    return ['({topic}) {subtopic}'.format(topic=jump[1], subtopic=jump[2]) for jump in jump_list]
