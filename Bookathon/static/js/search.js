$(document).ready(function(){
    var item, title, author, publisher, bookLink, bookImg;
    var outputList = document.getElementById("list-output");
    var apiKey = "{{book_api}}";
    var bookUrl = "https://www.googleapis.com/books/v1/volumes?q=";
    var placeHolder = "https://via.placeholder.com/150";
    var searchData;

    // listener for the search button 
    $("#search").click(function(){
        outputList.innerHTML = " "; //empty html output
        document.body.style.backgroundImage = "url('')"
        searchData = $("#search-box").val();
        // handling empty search input field
        if(searchData === " " || searchData === null){
            displayError();
        }
        else{
            // display searchData 
            // $.get("https://www.googleapis.com/books/v1/volumes?q="+searchData, getBookData()});
            $.ajax({
                url: bookUrl + searchData,
                dataType: "json", 
                success: function(responce){
                    console.log(responce)
                    if(responce.totalItem === 0){
                        alert("no results!.. try again")
                    }
                    else{
                        $("#title").animate({"margin-top": "5px"}, 1000); //search box animation
                        $(".book-list").css("visibility", "visible");
                        displayResults(responce)
                    }
                },
                error: function(){
                    alert("Something went wrong.. " + "Try again!");
                }
            });
        }
        $("#search-box").val(" "); //clearn search box
    });
    
    // function to display search result
    // @param response

    function displayResults(responce){
        for (var i=0; i< responce.items.length; i+=2){
            item = responce.items[i];
            title1 = item.volumeInfo.title;
            author1 = item.volumeInfo.authors;
            publisher1 = item.volumeInfo.publisher;
            bookLink1 = item.volumeInfo.previewLink;
            bookIsbn = item.volumeInfo.industryIdentifiers[1].identifier;
            bookImg1 = (item.volumeInfo.imageLinks) ? item.volumeInfo.imageLinks.thumbnail : placeHolder;
            
            item2 = responce.items[i+1];
            title2 = item2.volumeInfo.title;
            author2 = item2.volumeInfo.authors;
            publisher2 = item2.volumeInfo.publisher;
            bookLink2 = item2.volumeInfo.previewLink;
            bookIsbn2= item2.volumeInfo.industryIdentifiers[1].identifier;
            bookImg2= (item2.volumeInfo.imageLinks) ? item2.volumeInfo.imageLinks.thumbnail :placeHolder;

            // in production code, item.text should have the HTML entities escaped.
            outputList.innerHTML += '<div class="row mt-4">' +
                                    formatOutput(bookImg1, title1, author1, publisher1, bookLink1, bookIsbn) +
                                    formatOutput(bookImg2, title2, author2, publisher2, bookLink2, bookIsbn2) +
                                    '</div>';

            console.log(outputList);
        }
    }
    // template for boostrap cards
    function formatOutput(bookImg, title, author, publisher, bookLink, bookIsbn){
        var viewUrl = 'test.html?isbn=' + bookIsbn;
        var htmlCard = 
        `<div class="col-lg-6">
            <div class="card" style=" ">
                <div class="row no-gutters">
                <div class="col-md-4">
                    <img src="${bookImg}" class="card-img" alt="...">
                </div>
                <div class="col-md-8">
                    <div class="card-body">
                    <h5 class="card-title">${title}</h5>
                    <p class="card-text">Author: ${author}</p>
                    <p class="card-text">Publisher: ${publisher}</p>
                    <a target="_blank" href="${viewUrl}" class="btn btn-secondary">Read Book</a>
                    </div>
                </div>
                </div>
            </div>
        </div>`
        return htmlCard;
    }
    //handling error for empty search box
    function displayError() {
        alert("search term can not be empty!")
    }
})