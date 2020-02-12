var url = location.protocol + '//' + location.host + location.pathname;
var url_parameters = window.location.href;
url_parameters = new URL(url_parameters);
var page = url_parameters.searchParams.get("page");
var next_chapter;
var previous_chapter;
var total_pages;
var begin_page;
var end_page;
var directory;
var current_chapter;
if (page === null)
{
  page = 1;
}
var page_size = url_parameters.searchParams.get("page_size");
if (page_size === null)
{
  page_size = 9999;
}

function setupPage()
{
  total_pages = document.getElementById('total_pages').getAttribute('id-data');
  begin_page = document.getElementById('begin_page').getAttribute('id-data');
  end_page = document.getElementById('end_page').getAttribute('id-data');
  directory = document.getElementById('directory').getAttribute('id-data');
  current_chapter = document.getElementById('current_chapter').getAttribute('id-data');
  setupPageSelects(begin_page, end_page, total_pages);
  setupButtons(total_pages);
  setupChapterSelect(directory, current_chapter);
};

function setupChapterSelect(directory, currentChapter)
{
  const chapterSelects = document.getElementsByClassName("manga-chapter-select");
  for (const select of chapterSelects)
  {
    select.value = currentChapter;
    let index = 0;
    Object.values(select.options).forEach((option, i) => {
      if (option.value === select.value)
      {
        index = i;
      }
    });
    if (index < select.length - 1)
    {
      next_chapter = select.options[index + 1].value;
    }
    else
    {
      for (let nextBtn of document.getElementsByClassName("next-chapter"))
      {
        nextBtn.style.display = "none";
      }
    }
    if (index > 0)
    {
      previous_chapter = select.options[index - 1].value;
    }
    else
    {
      for (let prevBtn of document.getElementsByClassName("previous-chapter"))
      {
        prevBtn.style.display = "none";
      }
    }
  }
}

function setupButtons(total_pages)
{
  const prevBtns = document.getElementsByClassName("previous");
  for (const prevBtn of prevBtns)
  {
    if(page == 1)
    {
      prevBtn.classList = "previous-chapter";
      prevBtn.innerHTML = "&laquo; Previous Chapter";
    }
  }
  const nextBtns = document.getElementsByClassName("next");
  for (const nextBtn of nextBtns)
  {
    if(page * page_size >= total_pages)
    {
      nextBtn.classList = "next-chapter";
      nextBtn.innerHTML = "Next Chapter &raquo;";
    }
  }
}

function setupPageSelects(begin_page, end_page, total_pages) {
  const sizeElems = document.getElementsByClassName("manga-pageSize-select");
  for (let sizeElem of sizeElems)
  {
    sizeElem.value = page_size;
  }
  const pageSelects = document.getElementsByClassName("manga-page-select");
  for (let pageSelect of pageSelects)
  {
    setPageSelect(pageSelect, begin_page, end_page, total_pages);
  }
}

function previousClicked() {
  if(page == 1)
  {
    const newURL = '/manga/' + directory + previous_chapter;
    window.location.assign(newURL + '?page=1&page_size=' + page_size);
  }
  else
  {
    window.location.assign(url + '?page=' + (parseInt(page) - 1) + '&page_size=' + page_size);
  }
}

function nextClicked() {
  if(page * page_size >= total_pages)
  {
    const newURL = '/manga/' + directory + next_chapter;
    window.location.assign(newURL + '?page=1&page_size=' + page_size);
  }
  else
  {
    window.location.assign(url + '?page=' + (parseInt(page) + 1) + '&page_size=' + page_size);
  }
}

function pageSizeChanged(selectObject) {
  const newSize = selectObject.value;
  window.location.assign(url + '?page=' + page + '&page_size=' + newSize);
}

function setPageSelect(selectObject, begin_page, end_page, total_pages)
{
  let options = "";
  for(let i = 0; i < parseInt(total_pages); i += parseInt(page_size))
  {
    const page_num = parseInt(i / page_size) + 1;
    const start_page = i;
    let end_page = parseInt(i) + parseInt(page_size);
    if(end_page > total_pages)
    {
      end_page = total_pages;
    }
    options += "<option value='" + page_num + "'>" + start_page + "-" + end_page + "</option>";
  }
  selectObject.innerHTML = options;
  selectObject.value = begin_page / page_size + 1;
}

function pageSelectChanged(selectObject) {
  const newPosition = selectObject.value;
  window.location.assign(url + '?page=' + newPosition + '&page_size=' + page_size);
}

function chapterSelectChanged(selectObject, directory) {
  const newURL = '/manga/' + directory + selectObject.value;
  window.location.assign(newURL + '?page=1&page_size=' + page_size);
}
