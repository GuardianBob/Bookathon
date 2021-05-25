function get_book_json(link) { 
    $.ajax({
        url: "/books/json" + link + "",
        success: function (response){            
            //console.log(response.schedule);
            add_events(response.schedule)
            data = response
            return response
        },
        error: function (response) {
            // alert the error if any error occured
            console.log(response.responseJSON.errors)
        }
    });
};

function add_from_search(bookId) { 
    $.ajax({
        url: "/add/" + bookId + "",
        success: function (response){   
            $('#add_book').hide();
            return response
        },
        error: function (response) {
            // alert the error if any error occured
            console.log(response.responseJSON.errors)
        }
    });
};

$(document).ready(function(){
    var descr = $('#description').text();
    descr.replace(/"/g, '');
    $('#description').html(descr);
    // $('#description').html($('#description').html().replace(/['"]+/g, ''));
});