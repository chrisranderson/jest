import json

from censor import string_is_clean

data = []

to_delete = ['created_utc', 'edited', 'author', 'retrieved_on', 'distinguished', 'link_id', 'stickied', 'author_flair_text', 'author_flair_css_class']


with open('data/RC_2017-02') as file:
  for i, line in enumerate(file):
    if i % 10000 == 0:
      print('i', i)
    jsonified = json.loads(line)
    body = jsonified['body']

    if string_is_clean(body) and body != '[deleted]' and body != '[removed]':
    # if body != '[deleted]' and body != '[removed]':
      data.append(jsonified['body'])

      # for key in to_delete:
      #   jsonified.pop(key, None)
      

    if i > 10000000:
      break
