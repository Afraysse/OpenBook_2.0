"use strict";

$(function() {

    var server = 'http://localhost:5000'
    var drafts = [];

    function getDrafts(onComplete) {
        $.ajax({
            url: server + '/api/drafts',
            success: function(data) {
                onComplete(data.drafts)
            }
        })
    }

    function displayDrafts() {
        var $draftContainer = $('#previousDrafts')

        drafts.forEach(function(draft) {
            var $draft = $('<div></div>')
            $draft.append('<p>' + draft.title + '</p>')
            $draft.click(function(e) {
                console.log(draft)
            })

            $draftContainer.append($draft)
        })
    }

    getDrafts(function(remoteDrafts) {
        drafts = remoteDrafts;
        displayDrafts();
    });
})

//jquery to display objects parsed from python dictionary in model
//Display draft to show draft on page