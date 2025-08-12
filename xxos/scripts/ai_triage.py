#!/usr/bin/env python3
"""Offline AI triage script for GitHub Actions.
This script reads the GitHub event payload (issue opened/edited) and classifies the issue into labels.
It uses Hugging Face transformers models which are cached in the Actions runner after first download.
"""
import os, json, sys
from pathlib import Path

# Attempt to import transformers; in Actions the workflow will pip install transformers and torch
try:
    from transformers import pipeline
except Exception as e:
    print('transformers not available:', e)
    sys.exit(0)

EVENT_PATH = os.environ.get('GITHUB_EVENT_PATH', '/github/workflow/event.json')
with open(EVENT_PATH, 'r', encoding='utf-8') as f:
    event = json.load(f)

# Only handle issues
issue = event.get('issue')
if not issue:
    print('No issue found in event. Exiting.')
    sys.exit(0)

title = issue.get('title', '')
body = issue.get('body', '') or ''
text = title + '\n' + body

# model choices: lightweight classification and summarization
classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english', top_k=3)
# summarizer is optional and may be larger; comment out if you want tiny-run
try:
    summarizer = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')
except Exception as e:
    print('summarizer not available (will skip):', e)
    summarizer = None

labels = ['bug', 'feature', 'security', 'documentation', 'other']
# heuristic keyword mapping
mapping = {
    'crash': 'bug',
    'error': 'bug',
    'panic': 'bug',
    'vuln': 'security',
    'vulnerability': 'security',
    'exploit': 'security',
    'feature': 'feature',
    'request': 'feature',
    'doc': 'documentation',
    'install': 'bug'
}

preds = classifier(text[:1000])  # classify top sentiment/intent
pred_texts = [p['label'].lower() for p in preds if 'label' in p]
chosen = 'other'
# simple keyword map
for k,v in mapping.items():
    if k in text.lower():
        chosen = v
        break

# fallback based on sentiment
if chosen == 'other':
    if any('NEG' in p['label'].upper() for p in preds):
        chosen = 'bug'

summary = ''
if summarizer:
    try:
        s = summarizer(body or title, max_length=60, min_length=12, do_sample=False)
        summary = s[0]['summary_text']
    except Exception as e:
        summary = ''

print('::group::AI Triage Results')
print('Labels suggested:', chosen)
print('Summary:', summary)
print('::endgroup::')

# Post labels/comment via GitHub API if GITHUB_TOKEN available
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
if GITHUB_TOKEN:
    repo = os.environ.get('GITHUB_REPOSITORY')
    issue_number = issue.get('number')
    import requests
    headers = {'Authorization': f'token {GITHUB_TOKEN}', 'Accept': 'application/vnd.github.v3+json'}
    # add label
    try:
        url = f'https://api.github.com/repos/{repo}/issues/{issue_number}/labels'
        r = requests.post(url, headers=headers, json={'labels': [chosen]})
        print('Label post status:', r.status_code)
    except Exception as e:
        print('Label post error:', e)
    # post summary comment
    if summary:
        try:
            url = f'https://api.github.com/repos/{repo}/issues/{issue_number}/comments'
            r = requests.post(url, headers=headers, json={'body': f'**AI Summary:** {summary}'})
            print('Comment post status:', r.status_code)
        except Exception as e:
            print('Comment post error:', e)
