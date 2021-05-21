$(document).ready(function(){
    var item, title, author, publisher, bookLink, bookImg;
    var outputList = document.getElementById("list-output");
    var bookUrl = "https://www.googleapis.com/books/v1/volumes?q=";
    var placeHolder = "https://via.placeholder.com/150";
    var searchData;
    var apiKey = "AIzaSyBxGHxEpGyYmtab5CUFMjuEy272zij7blE";

    // listener for the search button 
    $("#search").click(function(){
        outputList.innerHTML = " "; //empty html output
        searchData = $("#search-box").val();
        // handling empty search input field
        if(searchData === " " || searchData === null){
            displayError();
        }
        else{
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
                        // displayResults(responce)
                    }
                },
                error: function(){
                    alert("Something went wrong.. br>"+"Try again!");
                }
            });
        }
        $("#search-box").val(" "); //clearn search box
    });





})