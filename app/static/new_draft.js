"use strict";

$(function) {
    function saveNewDraftResults(result) {
        alert(result.draft_id + "successfully saved!")
    }

    function saveNewDraft(evt) {
        evt.preventDefault();

        var formInputs = {
            "title": $("#title_field").val(),
            "draft": $("#draft_field").val(),
        };

        $.post("/new_draft.json",
                formInputs,
                saveNewDraftResults
                );
    }

    $("#new_draft").on("submit", saveNewDraft);


})