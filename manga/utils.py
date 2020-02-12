import zipfile
import rarfile
import pyunpack
import shutil
import base64
import tempfile
from os import walk
from .models import Directory

def sizeof_fmt(num, suffix='B'):
    """
    Returns the size of num with the proper suffix
    """
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def b64encode_image(image_file):
    """
    Base64 encodes an image file
    """
    b64Image = base64.b64encode(image_file)
    size = len(b64Image)
    return b64Image.decode(), size


def create_file_generator(file, page_size, page):
    """
    Creates a generator to get images from an archive.
    @param file The archive file
    @param page_size The number of images to display per page
    @param page The page to display
    @returns Image file generator
    """
    if page is None:
        page = 1
    if page_size is None:
        page_size = 9999
    file_generator = None
    if zipfile.is_zipfile(file):
        def zip_generator():
            begin_page = (page - 1) * page_size
            end_page = page * page_size
            zip_file = zipfile.ZipFile(file, 'r')
            file_list = zip_file.infolist()
            file_list = sorted(file_list, key=lambda x: x.filename)
            if end_page > len(file_list):
                end_page = len(file_list)
            for entry in file_list[begin_page:end_page]:
                if not entry.is_dir():
                    yield {
                            'content': zip_file.read(entry.filename),
                            'filename': entry.filename
                        }
            zip_file.close()
        file_generator = zip_generator
    elif rarfile.is_rarfile(file):
        def rar_generator():
            #TODO rarfile seems slower than pyunpack extracting to disk
            begin_page = (page - 1) * page_size
            end_page = page * page_size
            rar_file = rarfile.RarFile(file, 'r')
            file_list = rar_file.infolist()
            file_list = sorted(file_list, key=lambda x: x.filename)
            if end_page > len(file_list):
                end_page = len(file_list)
            for entry in file_list[begin_page:end_page]:
                if not entry.isdir():
                    yield {
                            'content': rar_file.read(entry.filename),
                            'filename': entry.filename
                        }
            rar_file.close()
        file_generator = rar_generator
    else:
        def generic_archive_generator():
            begin_page = (page - 1) * page_size
            end_page = page * page_size
            try:
                tempdir = tempfile.mkdtemp()
                archive_file = pyunpack.Archive(file)
                archive_file.extractall(tempdir)
                fileList = []
                for root, dirs, files in walk(tempdir):
                    for file in files:
                        fileList.append(root + "/" + file)
                fileList.sort()
                if end_page > len(file_list):
                    end_page = len(file_list)
                for file in fileList[begin_page:end_page]:
                    with open(file, 'rb') as image_file:
                        yield {
                                'content': image_file.read(),
                                'filename': file
                            }
            except Exception as e:
                print(e)
            finally:
                #delete temp files
                shutil.rmtree(tempdir)
        file_generator = generic_archive_generator
    return file_generator


def get_page_info(file, page_size, page):
    """
    Creates a generator to get images from an archive.
    @param file The archive file
    @returns total_pages, begin_page, end_page
    """
    if page is None:
        page = 1
    if page_size is None:
        page_size = 9999
    begin_page = (page - 1) * page_size
    end_page = page * page_size
    total_pages = 0
    if zipfile.is_zipfile(file):
        zip_file = zipfile.ZipFile(file, 'r')
        file_list = zip_file.infolist()
        if end_page > len(file_list):
            end_page = len(file_list)
        for entry in file_list:
            if not entry.is_dir():
                total_pages = total_pages + 1
        zip_file.close()
    elif rarfile.is_rarfile(file):
        rar_file = rarfile.RarFile(file, 'r')
        file_list = rar_file.infolist()
        if end_page > len(file_list):
            end_page = len(file_list)
        for entry in file_list:
            if not entry.isdir():
                total_pages = total_pages + 1
        rar_file.close()
    else:
        try:
            tempdir = tempfile.mkdtemp()
            archive_file = pyunpack.Archive(file)
            archive_file.extractall(tempdir)
            fileList = []
            for root, dirs, files in walk(tempdir):
                for file in files:
                    fileList.append(root + "/" + file)
            fileList.sort()
            if end_page > len(file_list):
                end_page = len(file_list)
            for file in fileList:
                total_pages = total_pages + 1
        except Exception as e:
            print(e)
        finally:
            #delete temp files
            shutil.rmtree(tempdir)
    return begin_page, end_page, total_pages


def performSearch(search_text, tags, genres, authors):
    """
    Searches the database directory structure for the given search_text
    """
    query = Directory.objects.only('title', 'full_path', 'tags', 'genres', 'authors')
    if search_text and len(search_text) > 0:
        query = Directory.objects.filter(title__icontains=search_text)
    if tags and len(tags) > 0:
        query = query.filter(tags__icontains=tags)
    if genres and len(genres) > 0:
        query = query.filter(genres__icontains=genres)
    if authors and len(authors) > 0:
        query = query.filter(authors__icontains=authors)
    search_results = []
    for dir in query:
        search_results.append(dir)
    search_results.sort(key=lambda x: x.title)
    return search_results


def getDirectoryParts(directory):
    """
    Splits a directory up
    """
    directory = '/' + directory
    remove_idx = []
    parts = directory.split('/')
    for idx in range(1, len(parts)):
        if parts[idx] == '':
            remove_idx.append(idx)

    for idx in remove_idx[::-1]:
        del parts[idx]
    del parts[0]

    directory_parts = []
    for idx in range(1, len(parts) + 1):
        directory_parts.append({'full_path': '/' + '/'.join(parts[:idx]), 'directory': parts[idx - 1]})
    return directory_parts


# Cache of search sets -- filled out on the first page load
all_tags = set()
all_genres = set()
all_titles = set()
all_authors = set()

def getAllTags():
    """
    Returns a set of all tags in the database
    """
    if len(all_tags) > 0: # check if cached
        return list(all_tags)
    dirs = Directory.objects.only('tags')
    for dir in dirs:
        for tag in dir.tags:
            all_tags.add(tag)
    return list(all_tags)

def getAllGenres():
    """
    Returns a set of all genres in the database
    """
    if len(all_genres) > 0: # check if cached
        return list(all_genres)
    dirs = Directory.objects.only('genres')
    for dir in dirs:
        for genre in dir.genres:
            all_genres.add(genre)
    return list(all_genres)

def getAllTitles():
    """
    Returns a set of all titles in the database
    """
    if len(all_titles) > 0: # check if cached
        return list(all_titles)
    dirs = Directory.objects.only('title')
    for dir in dirs:
        all_titles.add(dir.title)
    return list(all_titles)

def getAllAuthors():
    """
    Returns a set of all authors in the database
    """
    if len(all_authors) > 0: # check if cached
        return list(all_authors)
    dirs = Directory.objects.only('authors')
    for dir in dirs:
        for author in dir.authors:
            all_authors.add(author)
    return list(all_authors)
