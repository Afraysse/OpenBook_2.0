"use strict";

////////////////////////////// for saving //////////////////////////////////

$(function() { //says run this function once the DOM is ready

    var server = 'http://127.0.0.1:5000' //variable server connects to server
    var drafts = []; //a javascript array
    var currentDraft = null;

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
                currentDraft = draft;

                $("#title_field").val(draft.title)
                $("#draft_field").val(draft.contents)
                $("#id_field").val(draft.id)
        })
            $draftContainer.append($draft) //to the draftContainer, append var draft
            // $draft contains the paragraph component of draft.title 
            //event for class on <p> tags
        })
    }

//////////////////////////////// SAVE DRAFT ////////////////////////////////////

    function showResult(result) {
        alert(result.draft_id);
    }

    function saveDraft() {
        console.log("not doing anything");

        if (!currentDraft) {
            return;
        }

        var formInputs = {
            "title": $("#title_field").val(),
            "draft": $("#draft_field").val()
        }

        var draftId = $("#id_field").val()

        $.post("/save_draft/" + draftId,
            formInputs
                    );

        console.log(formInputs);
        console.log(currentDraft)
    }

    // $.post("/save_draft",
    //     formInputs,
    //     showResult);

    function setup() {
        getDrafts(function(remoteDrafts) {
            drafts = remoteDrafts;
            displayDrafts(); 

        });

        $("#save_btn").click(function(evt) {
            evt.preventDefault();
            saveDraft();
        });
    }

    setup();

    // $("#save_btn").click(function;
})








