__export__ = True

import sublime
import sublime_plugin
import re
import pprint

pp = pprint.PrettyPrinter(indent=4)

from .canopy_data_parser import parse_file
from .canopy_interface_manager import CanopyInterfaceManager

canopy_parse_data = {}
canopy_jump_lists = {}
canopy_edit_lists = {}

class CanopyParseDataClass():
  global canopy_parse_data
  global canopy_jump_lists
  global canopy_edit_lists

  @property
  def canopy_bulk_file(self):
    return bool(canopy_parse_data.get(sublime.active_window().active_view().file_name()))

  @property
  def categories(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['categories']

  @property
  def topics(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['topics']

  @property
  def subtopics(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['subtopics']

  @property
  def references(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['references']

  @property
  def categories_by_name(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['categories_by_name']

  @property
  def topics_by_name(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['topics_by_name']

  @property
  def subtopics_by_name(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['subtopics_by_name']

  @property
  def references_by_target(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['references_by_target']

  @property
  def topics_by_index(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['topics_by_index']

  @property
  def topic_definitions_by_index(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['topic_definitions_by_index']

  @property
  def subtopics_by_index(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['subtopics_by_index']

  @property
  def subtopic_definitions_by_index(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['subtopic_definitions_by_index']

  @property
  def references_by_index(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['references_by_index']

  @property
  def categories_by_index(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['categories_by_index']

  @property
  def jump_list(self):
    return canopy_jump_lists[sublime.active_window().active_view().file_name()]

  @property
  def edit_list(self):
    return canopy_edit_lists[sublime.active_window().active_view().file_name()]

CanopyParseData = CanopyParseDataClass()

class CanopyParseListener(sublime_plugin.ViewEventListener):
  pending = 0

  def in_bulk_file(self):
    lines = self.view.substr(sublime.Region(0, self.view.size())).splitlines()
    first_line = lines[0] if len(lines) > 0 else None
    return first_line and first_line.startswith('[') and first_line.endswith(']')

  def on_activated(self):
    if not self.in_bulk_file():
      return
    if not canopy_jump_lists.get(self.view.file_name()):
      canopy_jump_lists[self.view.file_name()] = []

    if not canopy_edit_lists.get(self.view.file_name()):
      canopy_edit_lists[self.view.file_name()] = []

    self.initiate_file_parse()

  def on_modified_async(self):
    if not self.in_bulk_file():
      return
    self.pending += 1
    sublime.set_timeout_async(self.initiate_file_parse, 500)

    sublime.set_timeout_async(self.register_edit, 501) # must wait for file parse

  def initiate_file_parse(self):
    global canopy_parse_data
    canopy_parse_data[self.view.file_name()] = parse_file(self, sublime)

  def register_edit(self):
    global canopy_edit_lists
    canopy_edit_list = canopy_edit_lists[self.view.file_name()]

    category = self.parse_data['categories_by_index'][CanopyInterfaceManager.get_cursor_position()]
    topic = self.parse_data['topics_by_index'][CanopyInterfaceManager.get_cursor_position()]
    subtopic = self.parse_data['subtopics_by_index'][CanopyInterfaceManager.get_cursor_position()]

    item = {
      'category': category and category.get('name'),
      'topic': topic and topic.get('name'),
      'subtopic': subtopic and subtopic.get('name')
    }

    if item in canopy_edit_list:
      index = canopy_edit_list.index(item)
      canopy_edit_list.remove(item)
      canopy_edit_list.insert(0, item)
    else:
      canopy_edit_list.insert(0, item)

  @property
  def parse_data(self):
    if not self.in_bulk_file():
      return

    return canopy_parse_data[self.view.file_name()]

  def on_selection_modified_async(self):
    if not self.in_bulk_file():
      return

    sublime.set_timeout_async(self.register_cursor_move, 501) # must wait for on_modified_async to reparse file

  def register_cursor_move(self):
    global canopy_jump_lists
    if not canopy_jump_lists.get(self.view.file_name()):
      canopy_jump_lists[self.view.file_name()] = []

    jump_list = canopy_jump_lists[self.view.file_name()]

    category = self.parse_data['categories_by_index'][CanopyInterfaceManager.get_cursor_position()]
    topic = self.parse_data['topics_by_index'][CanopyInterfaceManager.get_cursor_position()]
    subtopic = self.parse_data['subtopics_by_index'][CanopyInterfaceManager.get_cursor_position()]

    item = {
      'category': category and category.get('name'),
      'topic': topic and topic.get('name'),
      'subtopic': subtopic and subtopic.get('name')
    }

    if item in jump_list:
      index = jump_list.index(item)
      jump_list.remove(item)
      jump_list.insert(0, item)
    else:
      jump_list.insert(0, item)

  def render(self, linkContents):
    linkContents = self.remove_markdown(linkContents)

    target_string = '';
    exclusive_target_string = '';
    exclusive_display_syntax = False;

    segments = re.findall(r'(((?<!\\)\{\{?)((?:(?!(?<!\\)\}).)+)((?<!\\)\}\}?)|((?:(?!(?<!\\)[{}]).)+))', linkContents);
    for segment in segments:
      if (re.search(r'(?<!\\)\{', segment[0])): # if there are braces at all
        if (segment[4]): # plaintext segment
          target_string += segment[4];
        if (segment[1] == '{'):
          pipe_segments = re.split(r'(?<!\\)\|', segment[2])
          if (len(pipe_segments) == 2): # interpolation syntax
            target_string += pipe_segments[0]
            exclusive_target_string += pipe_segments[0]
          else: # exclusive display string syntax {{a}}
            target_string += pipe_segments[0]
        elif (segment[1] == '{{'): # exclusive target syntax
          exclusive_target_string += segment[2]
          exclusive_display_syntax = True
      elif(re.search(r'(?<!\\)\|', segment[0])):
        pipe_segments = re.split(r'(?<!\\)\|', segment[0])
        target_string = pipe_segments[0] # whether there is a pipe or isn't
      else: # plaintext link
        target_string += segment[0]

    target_string = exclusive_target_string if exclusive_display_syntax else target_string
    target_string = target_string[:1].upper() + target_string[1:]
    return target_string

  def remove_markdown(self, string):
    return string.replace('*', '')\
      .replace('_', '')\
      .replace('~', '')\
      .replace('`', '')\
      .replace('\n<', '')\
      .replace('\n>', '')\
      .replace('(', '')\
      .replace(')', '')\
      .replace('\'', '')\
      .replace('"', '')\
      .replace('‘', '')\
      .replace('’', '')\
      .replace('“', '')\
      .replace('”', '')
