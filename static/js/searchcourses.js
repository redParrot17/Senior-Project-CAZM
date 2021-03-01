var classes;
var reqs;
var requisites



window.addEventListener("DOMContentLoaded", function () {


    $.getJSON($SCRIPT_ROOT + '/getRequirements', {
        major_name: "Computer Science",
        major_year: 2020
    }, function (data) {
        reqs = data;
        loadStatusSheet(reqs);
        
    })

    $.getJSON($SCRIPT_ROOT + '/getRequisites', {
       
    }, function (data) {
        requisites = data;
        console.log(requisites);
        
    })

    

    let search = document.getElementById("search-button");

    search.addEventListener("click", function () {
        $.getJSON($SCRIPT_ROOT + '/searchClasses', {
            class_name: $('input[id="search-bar"]').val()
        }, function (data) {
            classes = data
            console.log(classes)
            console.log("--Search Done--");
            let container = document.getElementById("course-container");
            container.innerHTML = "";
            for (let i in classes) {
                let course = classes[i]

                /* Outer Div */
                let name = course.course_code;

                let courseID = name/*.replace(" ", "_") + "_" + course.semester + "_" + course.year*/;
                let div = document.createElement("div");
                div.id = courseID;
                div.className = "drag_item";
                div.draggable = "true";
                div.setAttribute("ondragstart", "drag(event)");
                div.setAttribute("ondragend", "dragEnd(event)");

                /* Arrows icon */
                let arrows = document.createElement("i");
                arrows.classList = "fas fa-arrows-alt";

                /* Class Text */
                let span = document.createElement("span");
                span.classList = "drag_item_text text-center";
                span.innerHTML = name;

                /* Trash Can */
                let trash = document.createElement("i");
                trash.classList = "fas fa-trash-alt ml-auto m-2 itemInvisible trashRed"
                trash.setAttribute("onclick", "removeDragItem(event)");

                /* Combine elements */

                div.appendChild(arrows)
                div.appendChild(span)
                div.appendChild(trash)
                container.appendChild(div)

            }
        });
    });
    addClassestoPools();

});
