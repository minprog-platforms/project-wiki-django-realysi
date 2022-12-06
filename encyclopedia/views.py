from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django import forms
from django.shortcuts import redirect
from django.core.files.storage import default_storage
from django.contrib import messages
from . import util


class CreateNewPage(forms.Form):
    title = forms.CharField(max_length=40)
    content = forms.CharField(max_length= 2000)





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

def save(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    if request.method == "POST":
        form = CreateNewPage(request.POST)
        if not form.is_valid():
            return render(request, "encyclopeida/new_page.html")
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        naam = f"entries/{title}.md"
        if default_storage.exists(naam):
            messages.add_message(request, messages.ERROR, 'Entry with this title already exists')
            return render(request, "encyclopedia/new_page.html")
        else:
            util.save_entry(title, content)
            return redirect("entry", title)
    #return render(request, "encyclopedia/error-message.html", {
     #       "Error-message": ""
    #    })
    