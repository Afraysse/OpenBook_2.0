function newDraft(evt)

    $('.draft-control').ready(function() {
            console.log("adding event handler");
            $('#save').click(function(evt) {
                debugger;
                evt.preventDefault();
                console.log("you clicked save");
                $.post("/book/{{ session['book_id'] }}",
                    {
                        title: $('#title_field').val(),
                        draft: $('#draft_field').val()
                    },
                    function (data) {
                        console.log("successfully saved");
                        $('#save-draft').text('Your draft is now saved!');
                        // $('publish').attr('disabled', true);
                    });
        });
    });