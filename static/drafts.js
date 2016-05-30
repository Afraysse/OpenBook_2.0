"use strict";

$(function() { //says run this function once the DOM is ready

    var server = 'http://localhost:5000' //variable server connects to server
    var drafts = []; //a javascript array

    function getDrafts(onComplete) { //function called when request finishes
        $.ajax({ //used to perform an asychronous HTTP request
            url: server + '/api/drafts', //string containing the url to send request
            success: function(data) { //a function to be called if the request succeeds
                onComplete(data.drafts) //call function when request finishes with the data.drafts
                // 'data' refers to info sent to the server during the request
            }
        })
    }

    function displayDrafts() {
        var $draftContainer = $('#previousDrafts') //with $() signifies a change to a DOM element
        // DOM element set to id #previousDrafts - a <div>

            // for each draft in drafts run function with parameter (draft)
            // safer than a for loop in Java

        drafts.forEach(function(draft) {
            var $draft = $('<div></div>')
            // within the <div> in draft page, assiging var draft (DOM element)
            $draft.append('<p class=object id=' + draft.id +'>' + draft.title + '</p>') //append to draft var DOM element paragraph draft.title
            $draft.click(function(evt) { // 'e' is short for event
                console.log(draft)
        })
            $draftContainer.append($draft) //to the draftContainer, append var draft
            // $draft contains the paragraph component of draft.title 
            //event for class on <p> tags
        })
    }

    ////

    getDrafts(function(remoteDrafts) {
        drafts = remoteDrafts;
        displayDrafts(); 
    });
})

//jquery to display objects parsed from python dictionary in model
//Display draft to show draft on page




