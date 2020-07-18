// Add a title at the top of the document 
function setIndexPageHeader(title) {
    document.getElementById("title").innerHTML = title;
}

// Add a description at the top of the document
function setIndexPageDescription(description) {
    document.getElementById("description").innerHTML = description;
}

// Add some text at the bottom of the document
function setIndexPageFooter(footer) {
    document.getElementById("footer").innerHTML = footer;
}

// Add a single item/page to the grid displayed in the static index page
function addPage(parentDom, name, description, author, keywords, url) {
    var pageItem = document.createElement("li");
    pageItem.className = "content-item";
    var header = '<a href="' + url + '" target="_blank"></a>' + '<h3>' + name + '</h3>';
    var authorName;
    if (author === '') {
        authorName = '<div class="author"><span>' + ' ' + '</span></div>';
    }
    else {
        authorName = '<div class="author"><span>' + '‣ ' + author + '</span></div>';
    }
    var keywordsList;
    if (keywords === '') {
        keywordsList = '<div class="keywords"><span>' + ' ' + '</span></div>';
    }
    else {
        keywordsList = '<div class="keywords"><span>' + '‣ ' + keywords.join(', ') + '</span></div>';
    }
    var pageDescription;
    if (description === '') {
        pageDescription = '<p class="text">' + ' ' + '</p>';
    }
    else {
        pageDescription = '<p class="text">' + description + '</p>';
    }
    pageItem.innerHTML = header + pageDescription + authorName  + keywordsList;
    parentDom.appendChild(pageItem);
}

// Add all items/pages to the grid displayed in the static index page
function loadData(index_page_data, file_list) {
    if (!index_page_data || !file_list) return;
    setIndexPageHeader(index_page_data.title);
    setIndexPageDescription(index_page_data.description);
    setIndexPageFooter(index_page_data.footer);
    var content = document.getElementById("content");
    var file, counter = 0, listDom;
    for (var i = 0; i < file_list.length; i++) {
        file = file_list[i];
        if (counter == 0) {
            listDom = document.createElement("ol");
            listDom.className = "content-list";
            content.appendChild(listDom);
        }
        addPage(listDom, file.name, file.description, file.author, file.keywords, file.url);
        counter++;
    }
}

// Load metadata contained in the "INDEX_PAGE_DATA" variable 
// Load all other collected static page data contained in the "FILE_LIST" variable
loadData(INDEX_PAGE_DATA, FILE_LIST);
