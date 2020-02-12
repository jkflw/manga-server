function httpGet(url) {
  let xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", url, false);
  xmlHttp.send(null);
  return xmlHttp.responseText;
}

function watch(dir) {
  let url = location.protocol + '//' + location.host + '/watch/' + encodeURI(dir);
  let resp = httpGet(url);
  console.log(resp);
}

function unwatch(dir) {
  let url = location.protocol + '//' + location.host + '/unwatch/' + encodeURI(dir);
  let resp = httpGet(url);
  console.log(resp);
}
