import sublime, sublime_plugin
import re

class CanopyExtractKeysCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    selection = self.view.sel()[0]
    if (selection.empty()):
      selection = self.view.line(self.view.sel()[0])
    selectionText = self.view.substr(selection)
    matches = re.findall(r'\[\[((?:(?!(?<!\\)\]\]).)+)\]\]', selectionText)
    def render(linkContents):
      target_string = '';
      exclusive_target_string = '';
      exclusive_display_syntax = False;

      segments = re.findall(r'(((?<!\\)\{\{?)((?:(?!(?<!\\)\}).)+)((?<!\\)\}\}?)|((?:(?!(?<!\\)[{}]).)+))', linkContents);
      for segment in segments:
        #print(segment[0], re.search(r'(?<!\\)\{', segment[0]))
        if (re.search(r'(?<!\\)\{', segment[0])): # if there are braces at all
          #print('bracket')
          if (segment[4]): # plaintext segment
            target_string += segment[4];
            #print('plain')
          if (segment[1] == '{'):
            pipe_segments = re.split(r'(?<!\\)\|', segment[2])
            if (len(pipe_segments) == 2): # interpolation syntax
              target_string += pipe_segments[0]
              exclusive_target_string += pipe_segments[0]
              #print('interpolation')
            else: # exclusive display string syntax {{a}}
              target_string += pipe_segments[0]
              #print('exclusive display')
          elif (segment[1] == '{{'): # exclusive target syntax
            exclusive_target_string += segment[2]
            exclusive_display_syntax = True
            #print('exclusive target')
        elif(re.search(r'(?<!\\)\|', segment[0])):
          pipe_segments = re.split(r'(?<!\\)\|', segment[0])
          #print(pipe_segments)
          target_string = pipe_segments[0] # whether there is a pipe or isn't
          #print('pipe')
        else: # plaintext link
          target_string += segment[0]
          #print('plain')

      target_string = exclusive_target_string if exclusive_display_syntax else target_string
      target_string = target_string[:1].upper() + target_string[1:]
      #print('target: ', target_string)
      return target_string
    link_targets = [render(match) for match in matches]

    def addColon(string):
      if (string[len(string) - 1] == '?'):
        return string
      else:
        return string + ':';

    keys = [addColon(link_target) for link_target in link_targets]

    text = '\n\n'.join(keys) + '\n'

    sublime.set_clipboard(text)
    if (len(keys) > 0):
      sublime.status_message('Copied Keys')
    else:
      sublime.status_message('No references in selection!')

# Tests: [[A|B]] [[ABC]] [[{a}bc]] [[{{a}}bc]] [[{a}b{c|d}]] [[question?]]
