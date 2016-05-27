"use strict";

//build function that displays published drafts sent through html draft page 

function publishDraftResults(results) {
    alert(result);
}

function publishDraft(evt) {
    evt.preventDefault();
    console.log("published");

    var formInputs = {
        "title": $("#title_field").val(),
        "draft": $("#draft_field").val(),

    };
    console.log("published here too")

    $.post("/publish_draft",
            formInputs,
            publishDraftResults
            );
    
    console.log("published right here as well!")
}

$("#publish_draft").on("submit", publishDraft)

