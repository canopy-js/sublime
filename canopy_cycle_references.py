import sublime
import sublime_plugin
import re

class CanopyCycleReferencesCommand(sublime_plugin.TextCommand):
  topic_definition = re.compile('(?:\\A|\n\n)(^\\*\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(\\s+|$)', re.M)
  subtopic_definition = re.compile('(?:\\A|\n\n)(^\\*?\\*? ?)(?!-)((?:[^:.!?\n]|(?<=\\\\)[:.!?]|[:.!?](?!\\s))+)(?::|(\\?))(\\s+|$)', re.M)
  category_definition = re.compile('(?:\\A|\n\n)(^\\[)([^\\]]+)\\]$', re.M)
  reference = re.compile(r'\[\[((?:(?!(?<!\\)\]\]).)+)\]\]', re.M)

  def run(self, edit):
    current_selection = self.view.sel()[0]
    fileText = self.view.substr(sublime.Region(0, self.view.size()))
    current_reference_match = next((match for match in self.reference.finditer(fileText) if (match.start() - 1 < current_selection.begin() and match.end() > current_selection.end())), None)
    current_subtopic_match = next((match for match in self.subtopic_definition.finditer(fileText) if (match.start() - 1 < current_selection.begin() and match.end() > current_selection.end())), None)

    if (current_reference_match or current_subtopic_match): # We are hovering over a link
      target_string = self.render(current_reference_match.groups()[0] if current_reference_match else current_subtopic_match.groups()[1])

      next_match = next(
        (reference_match for reference_match in self.reference.finditer(fileText)
          if self.render(reference_match.groups()[0]) == target_string and reference_match.start() > current_selection.begin()), None
      ) or next(
        (reference_match for reference_match in self.reference.finditer(fileText)
          if self.render(reference_match.groups()[0]) == target_string), None
      )

      if (not next_match):
        sublime.status_message('No matching references!')
        return
      self.view.sel().clear()
      self.view.sel().add(next_match.start())
      self.view.show(self.view.sel())
    else:
      sublime.status_message('Cursor needs to be on definition or reference!')
      return

  def render(self, linkContents):
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


# This is a [[A|B]] [[ABC]] [[{a}bc]] [[{{a}}bc]] [[{a}b{c|d}]] [[question?]]

# A:
