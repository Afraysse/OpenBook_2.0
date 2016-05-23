"use strict";

function showInputResults(result) {
    alert(result);
}

function saveDraft(evt) {
    evt.preventDefault();

    var formInputs = {
        "title": $("#title-field").val(),
        "draft": $("#draft-field").val()
    };

    $.post("/save_draft",
            formInputs,
            showInputResults
            );

}

$(".draft-control").on("save", saveDraft)