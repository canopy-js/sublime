import pprint
pp = pprint.PrettyPrinter(indent=4)

def parse_file(self, sublime):
  print('parsing')
  canopy_parse_data = {}
  text = self.view.substr(sublime.Region(0, self.view.size()))

  state = 'initial'
  current_category = None
  current_topic = None
  current_subtopic = None
  current_reference = None

  categories = []
  topics = []
  subtopics = []
  references = []

  topics_by_index = [None for i in range(len(text) + 1)]
  subtopics_by_index = [None for i in range(len(text) + 1)]
  categories_by_index = [None for i in range(len(text) + 1)]
  topic_definitions_by_index = [None for i in range(len(text) + 1)]
  subtopic_definitions_by_index = [None for i in range(len(text) + 1)]
  references_by_index = [None for i in range(len(text) + 1)]

  categories_by_name = {}
  topics_by_name = {}
  subtopics_by_name = {}
  references_by_target = {}

  buffer = ''
  i = 0

  while i < len(text):
    # print(i, state, text[i].encode('utf-8'))
    # print(subtopics_by_index)
    if state == 'initial':
      if text[i] == '[':
        state = 'in_category_name'
        current_category = {}
        current_category['start'] = i
        categories_by_index[i] = current_category
      else:
        return

    elif state == 'in_category_name':
      if text[i] == ']' and i < len(text) - 1 and text[i + 1] == '\n':
        current_category['name'] = buffer
        categories.append(current_category)
        categories_by_name[self.remove_markdown(buffer)] = current_category
        categories_by_index[i] = current_category
        categories_by_index[i + 1] = current_category
        buffer = ''
        i += 1
        state = 'in_category'
      else:
        categories_by_index[i] = current_category
        buffer += text[i]

    elif state == 'in_category':
      if text[i - 1] == '\n' and text[i] == '*' and text[i + 1] == ' ':
        current_topic = {}
        current_subtopic = {}
        current_topic['start'] = i
        current_subtopic['start'] = i

        topic_definitions_by_index[i] = current_topic
        topic_definitions_by_index[i + 1] = current_topic
        subtopic_definitions_by_index[i] = current_subtopic
        subtopic_definitions_by_index[i + 1] = current_subtopic

        topics_by_index[i] = current_topic
        topics_by_index[i + 1] = current_topic
        subtopics_by_index[i] = current_subtopic
        subtopics_by_index[i + 1] = current_subtopic
        categories_by_index[i] = current_category
        categories_by_index[i + 1] = current_category

        i += 1
        state = 'in_topic_name'

      else:
        categories_by_index[i] = current_category

    elif state == 'in_topic_name':
      if (text[i] == ':' or text[i] == '?') and text[i - 1] != '\\' and (i < len(text) - 1 and text[i + 1] == ' ' or text[i + 1] == '\n'):
        current_topic['name'] = buffer
        current_subtopic['name'] = buffer
        current_subtopic['topic'] = current_topic
        current_topic['category'] = current_category
        current_subtopic['category'] = current_category

        topics_by_index[i] = current_topic
        topics_by_index[i + 1] = current_topic

        subtopics_by_index[i] = current_subtopic
        subtopics_by_index[i + 1] = current_subtopic

        categories_by_index[i] = current_category
        categories_by_index[i + 1] = current_category

        topic_definitions_by_index[i] = current_topic
        topic_definitions_by_index[i + 1] = current_topic

        subtopic_definitions_by_index[i] = current_subtopic
        subtopic_definitions_by_index[i + 1] = current_subtopic

        topics.append(current_topic)
        topics_by_name[self.remove_markdown(buffer)] = current_topic
        subtopics.append(current_subtopic)
        subtopics_by_name[self.remove_markdown(buffer)] = current_subtopic

        buffer = ''

        if text[i + 1] == ' ' and text[i + 2] != '\n':
          state = 'in_paragraph'
        else:
          state = 'in_topic'

        i += 1

      elif text[i] == '\n':
        categories_by_index[i] = current_category

        buffer = ''
        state = 'in_note'

      else:
        topic_definitions_by_index[i] = current_topic
        subtopic_definitions_by_index[i] = current_subtopic
        topics_by_index[i] = current_topic
        subtopics_by_index[i] = current_subtopic
        categories_by_index[i] = current_category

        buffer += text[i]

    elif state == 'in_paragraph':
      if text[i] == '\n' and i < len(text) - 1 and text[i + 1] == '\n':
        topics_by_index[i] = current_topic
        topics_by_index[i + 1] = current_topic
        subtopics_by_index[i] = current_subtopic
        subtopics_by_index[i + 1] = current_subtopic
        categories_by_index[i] = current_category
        categories_by_index[i + 1] = current_category
        current_subtopic['end'] = i

        state = 'in_topic'

      elif text[i] == '[' and i < len(text) - 1 and text[i + 1] == '[':
        current_reference = {}
        current_reference['start'] = i
        references_by_index[i] = current_reference
        topics_by_index[i] = current_topic
        subtopics_by_index[i] = current_subtopic
        categories_by_index[i] = current_category
        i += 1
        state = 'in_reference'

      else:
        topics_by_index[i] = current_topic
        subtopics_by_index[i] = current_subtopic
        categories_by_index[i] = current_category

    elif state == 'in_topic':
      if text[i] == '*' and i < len(text) - 1 and text[i + 1] == ' ':
        current_topic['end'] = i - 1
        current_topic = {}
        current_topic['start'] = i
        current_subtopic = {}
        current_subtopic['start'] = i

        topic_definitions_by_index[i] = current_topic
        topic_definitions_by_index[i + 1] = current_topic
        subtopic_definitions_by_index[i] = current_subtopic
        subtopic_definitions_by_index[i + 1] = current_subtopic

        topics_by_index[i] = current_topic
        topics_by_index[i + 1] = current_topic
        subtopics_by_index[i] = current_subtopic
        subtopics_by_index[i + 1] = current_subtopic
        categories_by_index[i] = current_category
        categories_by_index[i + 1] = current_category

        i += 1
        state = 'in_topic_name'

      elif text[i] == '[':
        current_category['end'] = i - 1
        current_category = {}
        current_category['start'] = i
        current_topic['end'] = i - 1
        current_topic = None

        categories_by_index[i] = current_category

        state = 'in_category_name'

      elif text[i] != '*' and text[i] != '\n' and text[i] != '[':
        buffer += text[i]
        current_subtopic = {}
        current_subtopic['start'] = i
        subtopic_definitions_by_index[i] = current_subtopic

        topics_by_index[i] = current_topic
        subtopics_by_index[i] = current_subtopic
        categories_by_index[i] = current_category

        state = 'in_subtopic_name'
      else:
        topics_by_index[i] = current_topic
        categories_by_index[i] = current_category

    elif state == 'in_subtopic_name':
      if (text[i] == ':' or text[i] == '?') and text[i - 1] != '\\' and (i < len(text) - 1 and text[i + 1] == ' ' or text[i + 1] == '\n'):
        current_subtopic['name'] = buffer
        current_subtopic['topic'] = current_topic
        current_subtopic['category'] = current_category

        subtopic_definitions_by_index[i] = current_subtopic
        subtopics.append(current_subtopic)
        subtopics_by_name[self.remove_markdown(buffer)] = current_subtopic

        topics_by_index[i] = current_topic
        subtopics_by_index[i] = current_subtopic
        categories_by_index[i] = current_category

        buffer = ''
        state = 'in_paragraph'

      elif text[i] == '\n' or (text[i] == '.' and text[i - 1] != '\\') or (text[i] == ',' and text[i - 1] != '\\'):
        subtopic_definitions_by_index[i] = current_subtopic
        topics_by_index[i] = current_topic
        categories_by_index[i] = current_category

        buffer = ''
        state = 'in_note'

      else:
        buffer += text[i]

    elif state == 'in_note':
      if text[i] == '\n' and ((i < len(text) - 1 and text[i + 1] == '\n') or (text[i - 1] == '\n')):
        state = 'in_topic'
        topics_by_index[i] = current_topic
        categories_by_index[i] = current_category

    elif state == 'in_reference':
      if text[i] == ']' and i < len(text) - 1 and text [i + 1] == ']':
        current_reference['text'] = buffer
        current_reference['target'] = self.render(buffer)
        current_reference['end'] = i + 2
        current_reference['subtopic'] = current_subtopic
        current_reference['topic'] = current_topic
        current_reference['category'] = current_category

        references_by_index[i] = current_reference
        references_by_index[i + 1] = current_reference
        references_by_index[i + 2] = current_reference

        topics_by_index[i] = current_topic
        topics_by_index[i + 1] = current_topic
        subtopics_by_index[i] = current_subtopic
        subtopics_by_index[i + 1] = current_subtopic
        categories_by_index[i] = current_category
        categories_by_index[i + 1] = current_category

        references.append(current_reference)
        current_reference = {}

        references_by_target[self.render(buffer)] = current_reference

        buffer = ''
        i += 1

        state = 'in_paragraph'
      else:
        references_by_index[i] = current_reference

        topics_by_index[i] = current_topic
        subtopics_by_index[i] = current_subtopic
        categories_by_index[i] = current_category

        buffer += text[i]

    i += 1

  current_category['end'] = i
  categories_by_index[i] = current_category
  topics_by_index[i] = current_topic

  if (not (text[i - 2] == '\n' and text[i - 1] == '\n')):
    subtopics_by_index[i] = current_subtopic

  canopy_parse_data['categories'] = categories
  canopy_parse_data['topics'] = topics
  canopy_parse_data['subtopics'] = subtopics
  canopy_parse_data['references'] = references

  canopy_parse_data['categories_by_name'] = categories_by_name
  canopy_parse_data['topics_by_name'] = topics_by_name
  canopy_parse_data['subtopics_by_name'] = subtopics_by_name
  canopy_parse_data['references_by_target'] = references_by_target

  canopy_parse_data['topics_by_index'] = [topic if topic and topic.get('name') else None for topic in topics_by_index]
  canopy_parse_data['topic_definitions_by_index'] = topic_definitions_by_index
  canopy_parse_data['subtopics_by_index'] = [subtopic if subtopic and subtopic.get('name') else None for subtopic in subtopics_by_index]
  canopy_parse_data['subtopic_definitions_by_index'] = subtopic_definitions_by_index
  canopy_parse_data['references_by_index'] = references_by_index
  canopy_parse_data['categories_by_index'] = categories_by_index

  # for i in range(0, len(text)):
  #   print(i,
  #     (
  #       (categories_by_index[i] or {}).get('name'),
  #       (topics_by_index[i] or {}).get('name'),
  #       (subtopics_by_index[i] or {}).get('name')
  #     )
  #   )

  return canopy_parse_data
