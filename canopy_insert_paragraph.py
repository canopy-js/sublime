import sublime
import sublime_plugin

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyInsertParagraphCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    cursor = CanopyInterfaceManager.get_cursor_position()
    subtopic = CanopyParseData.subtopics_by_index[cursor]

    previous_reference = [
      reference
      for reference
      in CanopyParseData.references
      if reference['topic']['name'] == subtopic['topic']['name']
        and reference['subtopic']['name'] == subtopic['name']
        and reference['end'] < cursor
      ][-1]

    try:
      next_reference = [
        reference
        for reference
        in CanopyParseData.references
        if reference['topic']['name'] == subtopic['topic']['name']
          and reference['subtopic']['name'] == subtopic['name']
          and reference['start'] > cursor
        ][0]
    except (IndexError, TypeError):
      next_reference = None

    if previous_reference == None:
      return

    if not next_reference:
      # We have inserted a new last reference, and so we can't
      # be sure where the children of the second to last reference
      # end and where unrelated subtopics start, so we insert
      # after the previous reference.
      # TODO: do an actual DFS to find where the descendants of the
      # previous reference end, and insert there

      previous_subtopic = CanopyParseData.subtopics_by_name.get(previous_reference['target'])

      CanopyInterfaceManager.set_cursor_position(
        previous_subtopic['end']
      )

      new_reference = CanopyParseData.references_by_index[cursor]

      CanopyInterfaceManager.insert('\n\n' + new_reference['key'])
    else:
      # Here we can see where the next reference's subtopic is, and
      # so we use that to find the place to insert the new subtopic
      # without having to know which subtopics have further children
      next_subtopic = CanopyParseData.subtopics_by_name.get(next_reference['target'])

      CanopyInterfaceManager.set_cursor_position(
        next_subtopic['start']
      )

      new_reference = CanopyParseData.references_by_index[cursor]

      CanopyInterfaceManager.insert(new_reference['key'] + '\n\n')

      CanopyInterfaceManager.set_cursor_position(
        CanopyInterfaceManager.get_cursor_position() - 2
      )
