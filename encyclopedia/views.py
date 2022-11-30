from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse



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

def search(request):
    q = request.GET.get('q')
    if util.get_entry(q):
        return HttpResponseRedirect((reverse("entry", args=(q, ))))
    else:
        return HttpResponse("Moet dit nog aanpassen!!!!!!!")

def new_page(request):
    return render(request, "encyclopedia/new_page.html")