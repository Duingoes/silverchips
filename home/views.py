"""The home view directory.

Contains the methods for normal news views. This app mainly consists
of everything a normal user would see while visiting the website.
"""

# Django imports
from django.shortcuts import render, get_object_or_404

# News imports
from core import models


def load_context(request):
    return {
        "section_roots": models.Section.objects.filter(parent=None),
        "stories": models.Story.objects.filter(visibility=models.Content.PUBLISHED)
    }


def index(request):
    """Return the index page of the Silver Chips site."""

    return render(request, "home/index.html")


SECTION_COUNT = 5


def view_section(request, name):
    """Render a section of the newspaper."""

    section = get_object_or_404(models.Section, name=name)

    top_stories = section.all_stories()[:SECTION_COUNT]
    subsections = [(None, top_stories)]

    for subsection in section.subsections.all():
        subsections.append((subsection,
                            subsection.all_stories().filter(visibility=models.Content.PUBLISHED)
                            .exclude(id__in=top_stories.values_list('id', flat=True))))

    return render(request, "home/section.html", {
        "section": section,
        "subsections": subsections
    })


def view_content(request, pk):
    """Render specific content in the newspaper."""

    content = get_object_or_404(models.Content, id=int(pk))

    content.views += 1
    content.save()

    return render(request, "home/content.html", {
        "content": content
    })


def view_profile(request, pk):
    """Render the profile of a given staff member."""

    user = get_object_or_404(models.User, id=int(pk))

    # Find all the content that this user authored
    stories = models.Story.objects.filter(authors__in=[user], visibility=models.Content.PUBLISHED)
    images = models.Image.objects.filter(authors__in=[user], visibility=models.Content.PUBLISHED)

    return render(request, "home/profile.html", {
        "user": user,
        "stories": stories,
        "images": images
    })
