from django.shortcuts import render
import os

from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django import forms
from django.shortcuts import redirect
from django.core.files.storage import default_storage
from django.contrib import messages
from . import util
from .form import NewPage
import re
from random import randint

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


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
    entry = util.get_entry(q)
    titles = util.list_entries()
    if util.get_entry(q):
        return HttpResponseRedirect((reverse("entry", args=(q, ))))

    lijst = []
    for item in titles:
        if re.search(q, item, re.IGNORECASE):
            lijst.append(item)

    return render(request, "encyclopedia/search_results.html", {
        "name": q, 
        "entries": lijst
    })
    
def new_page(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
            else:
                return render(request, "encyclopedia/new_page.html", {
                "form": form,
                "existing": True,
                "entry": title
                })
        else:
            return render(request, "encyclopedia/new_page.html", {
            "form": form,
            "existing": False
            })
    else:
        return render(request,"encyclopedia/new_page.html", {
            "form": NewEntryForm(),
            "existing": False
        })    

def random(request):
    pages = util.list_entries()
    random_page = pages[randint(0, len(pages) - 1)]
    return redirect("entry", random_page) 

