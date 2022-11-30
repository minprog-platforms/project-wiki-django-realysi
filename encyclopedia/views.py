from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown



from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    content = util.get_entry(title)
    html_content = markdown_to_html(content) if content else None
    return render(request, "encyclopedia/entries.html", {
        "content": html_content,
        "exists": content is not None,
        "title": title if content is not None else "Error"
    })

def markdown_to_html(entry):
    to_convert = Markdown()
    return to_convert.convert(entry)
