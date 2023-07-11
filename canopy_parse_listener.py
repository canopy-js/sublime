__export__ = True

import sublime
import sublime_plugin
import re
import pprint
pp = pprint.PrettyPrinter(indent=4)

from .canopy_parse_data import parse_file
from .canopy_interface_manager import CanopyInterfaceManager

canopy_parse_data = {}
canopy_jump_list = []
canopy_edit_list = []

class CanopyParseData():
  global canopy_parse_data
  global canopy_jump_list
  global canopy_edit_list

  @classmethod
  def categories(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['categories']

  @classmethod
  def topics(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['topics']

  @classmethod
  def subtopics(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['subtopics']

  @classmethod
  def references(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['references']

  @classmethod
  def categories_by_name(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['categories_by_name']

  @classmethod
  def topics_by_name(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['topics_by_name']

  @classmethod
  def subtopics_by_name(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['subtopics_by_name']

  @classmethod
  def references_by_target(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['references_by_target']

  @classmethod
  def topics_by_index(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['topics_by_index']

  @classmethod
  def topic_definitions_by_index(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['topic_definitions_by_index']

  @classmethod
  def subtopics_by_index(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['subtopics_by_index']

  @classmethod
  def subtopic_definitions_by_index(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['subtopic_definitions_by_index']

  @classmethod
  def references_by_index(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['references_by_index']

  @classmethod
  def categories_by_index(self):
    return canopy_parse_data[sublime.active_window().active_view().file_name()]['categories_by_index']

  @classmethod
  def jump_list(self):
    return canopy_jump_list

  @classmethod
  def edit_list(self):
    return canopy_edit_list


class CanopyParseListener(sublime_plugin.ViewEventListener):
  pending = 0

  def on_selection_modified_async(self):
    if self.view.substr(sublime.Region(0, 1)) != '[':
      return
    self.register_cursor_move()

  def on_activated(self):
    self.initiate_file_parse()

  def on_modified_async(self):
    if self.view.substr(sublime.Region(0, 1)) != '[':
      return
    self.pending += 1
    sublime.set_timeout_async(self.initiate_file_parse, 500)

    self.register_edit()

  def initiate_file_parse(self):
    global canopy_parse_data
    canopy_parse_data[self.view.file_name()] = parse_file(self, sublime)

  def register_edit(self):
    global canopy_parse_data
    canopy_parse_data[self.view.file_name()]['edit_list'] = canopy_edit_list

    category = self.parse_data()['categories_by_index'][CanopyInterfaceManager.get_cursor_position()]
    topic = self.parse_data()['topics_by_index'][CanopyInterfaceManager.get_cursor_position()]
    subtopic = self.parse_data()['subtopics_by_index'][CanopyInterfaceManager.get_cursor_position()]

    item = (category and category['name'], topic and topic['name'], subtopic and subtopic['name'])
    if item in canopy_edit_list:
      index = canopy_edit_list.index(item)
      canopy_edit_list.remove(item)
      canopy_edit_list.insert(0, item)
    else:
      canopy_edit_list.insert(0, item)

  def parse_data(self):
    return canopy_parse_data[self.view.file_name()]

  def register_cursor_move(self):
    global canopy_parse_data
    canopy_parse_data[self.view.file_name()]['jump_list'] = canopy_jump_list

    category = self.parse_data()['categories_by_index'][CanopyInterfaceManager.get_cursor_position()]
    topic = self.parse_data()['topics_by_index'][CanopyInterfaceManager.get_cursor_position()]
    subtopic = self.parse_data()['subtopics_by_index'][CanopyInterfaceManager.get_cursor_position()]

    item = (category and category['name'], topic and topic['name'], subtopic and subtopic['name'])
    if item in canopy_jump_list:
      index = canopy_jump_list.index(item)
      canopy_jump_list.remove(item)
      canopy_jump_list.insert(0, item)
    else:
      canopy_jump_list.insert(0, item)

    print(canopy_jump_list)

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
