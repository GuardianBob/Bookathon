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