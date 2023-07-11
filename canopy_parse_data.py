import pprint
pp = pprint.PrettyPrinter(indent=4)

def split_text_into_lines_with_indexes(text):
    lines = text.splitlines()
    index = 0
    for line in lines:
        line_with_index = (index, line)
        index += len(line)
        yield line_with_index

def parse_file(self, sublime):
  print('parsing')
  canopy_parse_data = {}
  text = self.view.substr(sublime.Region(0, self.view.size()))

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

  lines = split_text_into_lines_with_indexes(text)

  current_category = None
  current_topic = None
  current_subtopic = None

  for index, line in lines:
    category_match = re.match(r"^\[(\w+(?:\/\w+)+)\]$", line)
    topic_match = re.match(r"^\* [^\n]+(\?|(?=:))$", line)
    subtopic_match = re.match(r"^[^\n]+(\?|(?=:))$", line)

    if category_match:
      current_category = { 'name': category_match[1], 'start': index }

    elif topic_match:
      current_topic = { 'name': topic_match[1], 'start': index }

    elif subtopic_match:
      current_subtopic = { 'name': subtopic_match[1], 'start': index }

    else:
      categories_by_index
      topics_by_index
      subtopics_by_index


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

  return canopy_parse_data
