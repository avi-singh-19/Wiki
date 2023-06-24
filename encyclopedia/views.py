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
            'error_message': 'There is no entry under this title'
        })
    else:
        return render(request, 'encyclopedia/entry.html', {
            'content': markdown_conversion(title)
        })
