# -*- coding: utf-8 -*-
"""md2html.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vGlR2-mMD0Qo_gjOfrmgPSs6nURem_6U

This code extracts texts in READMEs in `ethereum_repos.json` to reduce noise in README files, facilitating further text analysis on these files.

This is done by first converting markdown readme into html format, and then extracting texts from them using `BeautifulSoup`.

The program further cleans the texts by removing links and code blocks in the content of files. Customized operations used for cleaning can be plugged in by inserting a function into list `clean_pipe`.
"""

!pip install markdown

for repo in json_data:
  if repo["readme"]:
    repo["readme"] = markdown.markdown(repo["readme"])

with open('/content/ethereum_repos_html.json', 'w') as f:
  json.dump(json_data, f)

from bs4 import BeautifulSoup

with open('/content/ethereum_repos_html.json', 'r') as file:
  json_data = json.load(file)

for repo in json_data:
  if repo['readme']:
    soup = BeautifulSoup(repo['readme'], 'html.parser')
    repo['readme'] = soup.get_text(separator=' ', strip=True)

with open('/content/ethereum_repos_extracted_text.json', 'w') as f:
  json.dump(json_data, f)

import re

def remove_links(text: str):
  return re.sub(r'\bhttps?\S+', '', text)

def remove_codeblock(text: str):
  return re.sub('```[\s\S]+?```', '', text)

clean_pipe = [remove_links, remove_codeblock]

def clean(text:str):
  for stage in clean_pipe:
    text = stage(text)
  return text

with open('/content/ethereum_repos_extracted_text.json', 'r') as file:
  json_data = json.load(file)

for repo in json_data:
  if repo['readme']:
    repo['readme'] = clean(repo['readme'])

with open('/content/ethereum_repos_extracted_text_cleaned.json', 'w') as f:
  json.dump(json_data, f)