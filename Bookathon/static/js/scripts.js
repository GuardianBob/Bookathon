function get_book_json(link) { 
    $.ajax({
        url: "/books/json" + link + "",
        success: function (response){            
            //console.log(response.schedule);
            // add_events(response.schedule)
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

function remove_from_collection(bookId) {
    $.ajax({
        url: "/remove/" + bookId + "",
        success: function (response){   
            // console.log(response);
            var books = response['books'];
            $("#book_list tr").remove();
            books.forEach((book)=>{
                // console.log(book.title);
                $("#book_list").append(
                    `<tr>
                        <td><a href="/info/${book.google_id}">${book.title}</a></td>
                        <td><a href="#" onclick="remove_from_collection('${book.id}')">Remove</a></td>
                    </tr>`
                );
            })
            return response
        },
        error: function (response) {
            // alert the error if any error occured
            console.log(response.responseJSON.errors)
        }
    });
}

$(document).ready(function(){
    var descr = $('#description').text();
    descr.replace(/"/g, '');
    $('#description').html(descr);
    // $('#description').html($('#description').html().replace(/['"]+/g, ''));
});

