"use strict";

function displayDrafts() {

    var div = document.createElement('div');
    document.body.appendChild(div);
    document.getElementById("title_field").appendChild(div);
    console.log("here I am")
}

$("#save_draft").on("submit", saveDraft);