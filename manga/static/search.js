var url = location.protocol + '//' + location.host + location.pathname;
var url_parameters = window.location.href;
url_parameters = new URL(url_parameters);
var search_text = url_parameters.searchParams.get("search_text");
var tags_text = url_parameters.searchParams.get("tags");
var genres_text = url_parameters.searchParams.get("genres");
var authors_text = url_parameters.searchParams.get("authors");

function setupPage() {
  if (search_text)
  {
    document.getElementById("title-search-input").value = search_text;
  }
  if (tags_text)
  {
    document.getElementById("tag-search-input").value = tags_text;
  }
  if (genres_text)
  {
    document.getElementById("genre-search-input").value = genres_text;
  }
  if (authors_text)
  {
    document.getElementById("author-search-input").value = authors_text;
  }
}
