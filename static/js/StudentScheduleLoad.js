var reqs;
var requisites;
var studentData;


/**
 * Load Student info
 */
window.addEventListener("DOMContentLoaded", function () {

    $.getJSON($SCRIPT_ROOT + '/studentData', {

    }, function (data) {
        studentData = data;

        //Get requirements list for student's major
        $.getJSON($SCRIPT_ROOT + '/getRequirements', {
            'id' : studentData.id
        }, function (reqData) {

            reqs = reqData;

            loadStatusSheet(reqs);
            document.getElementById("status-sheet-spinner").innerHTML = "";
        });

            // set up student schedule containers
            setUpStudentScheduleContainers(studentData);
            document.getElementById("schedule-spinner").innerHTML = "";

            if(viewedTutorial==false){
              setTimeout(() => {  introJs().setOptions({scrollToElement: false, disableInteraction: true}).start(); }, 200);
            }
            addClassestoPools();

            //Get requisite list for each course
            $.getJSON($SCRIPT_ROOT + '/getRequisites', {

            }, function (requisiteData) {
                requisites = requisiteData;
                checkPools(false);
            })

        }, function (requisiteData) {
            requisites = requisiteData;
            addClassestoPools();
            checkPools(false);
        });

    });


    /**
    FOR SEARCH FILTER ON SIDEBAR
    */
    // Get the input field
    let input = document.getElementById("search-bar");
    // Execute a function when the user releases a key on the keyboard
    input.addEventListener("keyup", function(event) {

        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("search-button").click();

    });
