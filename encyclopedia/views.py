from django.shortcuts import render
import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def markdown_conversion(md_file):
    markdowner = markdown.Markdown()
    md_content = util.get_entry(md_file)

    if md_content is None:
        return None
    else:
        return markdowner.convert(md_content)


def entry(request, title):
    if markdown_conversion(title) is None:
        return render(request, 'encyclopedia/no_entry.html', {
            'error_message': 'There is no entry saved under this title, sorry'
        })
    else:
        return render(request, 'encyclopedia/entry.html', {
            'content': markdown_conversion(title),
            'title': title
        })


def search(request):
    if request.method == "POST":
        entry_lookup = request.POST['q']
        content = markdown_conversion(entry_lookup)
        if content is not None:
            return render(request, 'encyclopedia/entry.html', {
                'content': content,
                'title': entry_lookup
            })
        else:
            entries = util.list_entries()
            results = []
            for entry in entries:
                if entry_lookup.lower() in entry.lower():
                    results.append(entry)

            return render(request, 'encyclopedia/search_results.html', {
                'results': results,
                'error_message': 'There are no entries matching your search, sorry',
                'search_query': entry_lookup
            })


def create(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/create.html', {
            'message': 'Create a new entry on this page about any new topic you want'
        })
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['text']

        if util.get_entry(title):
            return render(request, 'encyclopedia/create.html', {
                'message': 'An entry with this title already exists, please create an entry with a new title'
            })
