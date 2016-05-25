"use strict";

    function showInputResults(result) {
        alert(result);
    }

    function saveDraft(evt) {
        evt.preventDefault();
        console.log("hello");

        var formInputs = {
            "title": $("#title_field").val(),
            "draft": $("#draft_field").val(),
        };
        console.log("hello");

        $.post("/save_draft",
                formInputs,
                showInputResults
                );
        console.log("hello");

    }

    $("#save_draft").on("submit", saveDraft);
