from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, FileResponse, Http404
from django.template import loader
from os import listdir
from os.path import isfile, join
import time
from .utils import (sizeof_fmt, b64encode_image,
        create_file_generator, performSearch, getDirectoryParts,
        get_page_info, getAllTags, getAllGenres, getAllTitles,
        getAllAuthors)
from .settings import MANGA_DIR
from .models import Directory, WatchedSeries
import json

# Create your views here.
def watch(request, dir):
    d = Directory.objects.get(full_path=dir)
    try:
        WatchedSeries.objects.get(series = d)
    except Exception:
        WatchedSeries.objects.create(series = d)
    return HttpResponse(True)

def unwatch(request, dir):
    d = Directory.objects.get(full_path=dir)
    try:
        WatchedSeries.objects.filter(series = d).delete()
    except Exception as e:
        print(e)
        pass
    return HttpResponse(True)

def fileView(request, directory, file):
    """View for non-manga files"""
    file = MANGA_DIR + directory + file
    try:
        return FileResponse(open(file, 'rb'))
    except FileNotFoundError:
        raise Http404()

def home(request):
    template = loader.get_template('home.html')
    context = {
        "watched": []
    }
    for watchedSeries in WatchedSeries.objects.all():
        context["watched"].append({
            "title" : watchedSeries.series.title,
            "path" : watchedSeries.series.full_path[len(MANGA_DIR):],
            "image" : watchedSeries.series.manga_image
        })
    return HttpResponse(template.render(context, request))

def index(request, directory):
    """View when navigating directories"""
    template = loader.get_template('dir.html')
    print(request.user)
    #get current dir files
    dir = MANGA_DIR + directory
    files = listdir(dir)
    files.sort()

    directory_parts = getDirectoryParts(directory)
    tags = []
    genres = []
    authors = []
    title = ""
    year = ""
    completely_scanlated = False
    manga_updates_link = ""
    is_series_path = False
    manga_image = ""
    try:
        d = Directory.objects.get(full_path=dir)
        tags = d.tags
        genres = d.genres
        authors = d.authors
        title = d.title
        year = d.year
        completely_scanlated = d.completely_scanlated
        manga_updates_link = d.manga_updates_link
        manga_image = d.manga_image
        is_series_path = True
    except Exception:
        pass
    context = {
        "dir" : dir,
        "dirs" : files,
        "current_dir" : directory,
        "directory_parts" : directory_parts,
        "all_titles" : json.dumps(getAllTitles()),
        "is_series_path" : is_series_path,
        "tags" : tags,
        "genres" : genres,
        "authors" : authors,
        "title" : title,
        "year" : year,
        "completely_scanlated" : completely_scanlated,
        "manga_image" : manga_image,
        "manga_updates_link" : manga_updates_link
    }

    return HttpResponse(template.render(context, request))


def search(request):
    """View when navigating directories"""
    search_text = request.GET.get('search_text', None)
    tags = request.GET.get('tags', None)
    genres = request.GET.get('genres', None)
    authors = request.GET.get('authors', None)
    template = loader.get_template('search.html')
    search_results = performSearch(search_text, tags, genres, authors)

    paths = []
    for dir in search_results:
        paths.append({
            'full_path' : '/manga/' + str(dir.full_path[len(MANGA_DIR):]),
            'title' : str(dir.title)
        })

    context = {
        "paths" : paths,
        "all_tags" : json.dumps(getAllTags()),
        "all_genres" : json.dumps(getAllGenres()),
        "all_titles" : json.dumps(getAllTitles()),
        "all_authors" : json.dumps(getAllAuthors()),
    }

    return HttpResponse(template.render(context, request))


def mangaView(request, directory, file):
    """View when reading a manga chapter/volume"""
    dir = MANGA_DIR + directory
    chapter_list = [f for f in sorted(listdir(dir)) if isfile(join(dir, f))]
    current_chapter = file.split('/')[-1]
    page_size = request.GET.get('page_size', None)
    page = request.GET.get('page', None)
    if page_size is not None:
        page_size = int(page_size)
    if page is not None:
        page = int(page)
    file = MANGA_DIR + directory + file
    file_generator = create_file_generator(file, page_size, page)
    begin_page, end_page, total_pages = get_page_info(file, page_size, page)
    context = {
        "directory": directory,
        "chapter_list": chapter_list,
        "current_chapter": current_chapter,
        "directory_parts": getDirectoryParts(directory),
        "begin_page": begin_page,
        "end_page": end_page,
        "total_pages": total_pages
    }
    return StreamingHttpResponse(stream_manga_image_generator(file_generator, context))


def stream_manga_image_generator(images, context):
    #Stream so the first picture loads instantly
    start_time = time.time()
    total_size = 0
    yield loader.render_to_string('manga-view-buttons.html', context)
    yield "<body bgcolor=\"#000000\">"
    for image_file in images():
        b64Image, size = b64encode_image(image_file['content'])
        total_size += size
        yield "<font color=\"#555555\">%s</font><br/>" % image_file['filename']
        yield "<img src=\"data:image/jpeg;base64,%s\" /><br/>" % b64Image
    total_size = sizeof_fmt(total_size)
    yield "<font color=\"#999999\">Loaded: %s</font><br/>" % total_size
    yield "</body>"
    yield loader.render_to_string('manga-view-buttons.html', context)
    end_time = time.time()
    GREEN = "\033[1;32m"
    CLEAR = "\033[0m"
    print(GREEN + "Serve time: {0} seconds.  Total size: {1}".format(str(end_time - start_time), total_size) + CLEAR)
