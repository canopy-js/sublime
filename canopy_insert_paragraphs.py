import sublime
import sublime_plugin

from .canopy_parse_listener import CanopyParseData
from .canopy_interface_manager import CanopyInterfaceManager

class CanopyInsertParagraphsCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    cursor = CanopyInterfaceManager.get_cursor_position()
    subtopic = CanopyParseData.subtopics_by_index[cursor]
    if not subtopic:
      return

    references = [
      reference['key']
      for reference
      in CanopyParseData.references
      if reference['topic']['name'] == subtopic['topic']['name']
        and reference['subtopic']['name'] == subtopic['name']
    ]

    print(list(r['target'] for r in CanopyParseData.references))
    CanopyInterfaceManager.set_cursor_position(
      subtopic['end']
    )

    CanopyInterfaceManager.insert('\n\n' + '\n\n'.join(references))
