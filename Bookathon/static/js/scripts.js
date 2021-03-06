function get_book_json(link) { 
    $.ajax({
        url: "/json/" + link + "",
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

function get_book_img(bookId) { 
    $.ajax({
        url: "/img/" + bookId + "",
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
            $(`#${bookId}`).hide();
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

function add_remove_friend(user_id) { 
    $.ajax({
        url: "/update_friend/" + user_id + "/follow",
        success: function (response){   
            $('#add_book').hide();
            // console.log('added');
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

