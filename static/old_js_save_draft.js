"use strict";

$(function() {
    function showInputResults(result) {
        alert(result.draft_id);
        $('#previousDrafts').append('<a href=' + "/draft_page/" + 
            result.draft_id + '>' + '<h2>' + 
            result.draft_title + '</h2>' + '</a>')
    }

    function saveDraft(evt) {
        evt.preventDefault();
        console.log("hello");
        console.log($("#draft_field").val())
        console.log($("#title_field").val())

        var formInputs = {
            "title": $("#title_field").val(),
            "draft": $("#draft_field").val(),
            "draft_id": $("")
        };
        console.log("hello");

        //make a post request - sending it to the route
        $.post("/save_draft",
                formInputs,

                showInputResults
                );
        console.log("hello");

    }

    $("#save_draft").on("submit", saveDraft); 
})
