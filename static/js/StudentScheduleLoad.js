var reqs;
var requisites;
var studentData;



window.addEventListener("DOMContentLoaded", function () {

    $.getJSON($SCRIPT_ROOT + '/studentData', {

    }, function (data) {
        studentData = data;

        //Get requirements list for student's major
        $.getJSON($SCRIPT_ROOT + '/getRequirements', {
            major_name: studentData.major_name,
            major_year: studentData.major_year
        }, function (reqData) {

            reqs = reqData;

            loadStatusSheet(reqs);

        })


        // set up student schedule containers
        setUpStudentScheduleContainers(studentData);


        //Get requisite list for each course
        $.getJSON($SCRIPT_ROOT + '/getRequisites', {

        }, function (requisiteData) {
            requisites = requisiteData;
            addClassestoPools();
            console.log("Page load checking")
            checkPools(false);

        })

    })


    /**
    FOR SEARCH FILTER ON SIDEBAR
    */
    // Get the input field
    let input = document.getElementById("search-bar");
    // Execute a function when the user releases a key on the keyboard
    input.addEventListener("keyup", function(event) {
      // Number 13 is the "Enter" key on the keyboard
      if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("search-button").click();
      }
    });


});
