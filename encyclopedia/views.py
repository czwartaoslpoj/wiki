from django.shortcuts import render, redirect
from . import util
from django import forms
from django.http import HttpResponseRedirect

import markdown2

class searchForm(forms.Form):
    query = forms.CharField(max_length=10)

class newQueryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(max_length=1000, widget=forms.Textarea, label="Content")


def index(request):
    print(7485)
    return render(request, "encyclopedia/index.html", {
        "form":searchForm(),
        "entries": util.list_entries()
    })

def showEntry(request, entry):
    print(1)
    right_entry = util.get_entry(entry)
    if right_entry is None:
        return render(request, "encyclopedia/notfounderror.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry" : markdown2.markdown(right_entry),
            "title" : entry
            })

def search(request):
    entries = util.list_entries()
    if request.method == "GET":
        form = searchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if query in entries:
                query = util.get_entry(query)
                return render(request, "encyclopedia/entry.html", {
                    "entry" : markdown2.markdown(query),
                    "form" : searchForm()
                } )
            elif query not in entries:
                for entry in entries:
                    if query in entry:
                        query = util.get_entry(entry)
                        return render(request,"encyclopedia/entry.html", {
                            "entry" : markdown2.markdown(query),
                            "form" : searchForm()
                        })
            
            else:
                return render(request, "encyclopedia/notfounderror.html", {
                    "form": searchForm()
                })
    else:
        return render(request,"encyclopedia/index.html", {
            "form": searchForm()
        })

def addEntry(request):
    if request.method == "POST":
        form = newQueryForm(request.POST)
        entries = util.list_entries()
        if form.is_valid():
            title= form.cleaned_data["title"]
            content= form.cleaned_data["content"]
            if title in entries:
                return render(request, "encyclopedia/alreadyexist.html")
            else:
                util.save_entry(title, content)
                entry = util.get_entry(title)
                return render(request,"encyclopedia/entry.html", {
                    "entry" : markdown2.markdown(entry),
                    "form" : searchForm()

                } )

    return render(request, "encyclopedia/add.html", {
        "form": newQueryForm()
    })





