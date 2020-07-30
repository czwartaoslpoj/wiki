from django.shortcuts import render, redirect
from . import util
from django import forms
from django.http import HttpResponseRedirect

import markdown2

class searchForm(forms.Form):
    query = forms.CharField(max_length=10)


def index(request):
    print(7485)
    return render(request, "encyclopedia/index.html", {
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
    print(10)
    entries = util.list_entries()
    if request.method == "GET":
        form = searchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            if query in entries:
                return redirect("entry", entry = query)
            elif query not in entries:
                for entry in entries:
                    if query in entry:
                        return redirect("entry", entry= entry)
        else:
            return render(request, "encyclopedia/notfounderror.html")
    else:
        return render(request,"encyclopedia/index.html", {
            "form": searchForm()
        })



