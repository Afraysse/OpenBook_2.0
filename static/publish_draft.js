"use strict";

//build function that displays published drafts sent through html draft page 

function publishDocResults(results) {
    // console.log(results); //for debugging purposes
    var published = results;
    console.log(published);
    $("#publish_draft").html(published)

}

function publishDoc(evt) {
    $.post('/publish_draft', {}, function(data) {
        $('#publish-')
    }

})