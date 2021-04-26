
/**
 * Create a draggable div DOM element for the course code
 * @param {*} course
 * course code to use
 * @returns draggable course code DOM element
 */
function createCourseDiv(course) {
    let name = course.course_code;
    let courseID = name;
    let div = document.createElement("div");
    div.id = courseID;
    div.className = "drag_item";
    div.draggable = "true";

    div.setAttribute("semester", course.semester);
    div.setAttribute("courseCode", courseID);
    div.setAttribute("ondragstart", "set_valid_drag_locations(event);drag(event);");
    div.setAttribute("ondragend", "revert_drag_locations(event);dragEnd(event);");
    div.setAttribute("data-toggle", "tooltip");
    div.setAttribute("data-placement", "left");
    
    div.setAttribute("data-delay", 0);
   
    div.setAttribute("title", course.name);



    /* Arrows icon */
    let arrows = document.createElement("i");
    arrows.classList = "col-1 pr-0 pl-0 ml-2 fas fa-arrows-alt";

    /* Class Text */
    let span = document.createElement("span");
    span.classList = "col pr-0 pl-0 drag_item_text text-center";
    span.innerHTML = name;

    /* Trash Can */
    let trash = document.createElement("i");
    trash.classList = "col-1 pr-0 pl-0 fas fa-trash-alt ml-auto m-2 itemInvisible trashRed";
    trash.setAttribute("onclick", "removeDragItem(event)");

    /*Warning*/
    let warning = document.createElement("i");



    /* Combine elements */
    div.appendChild(arrows);
    div.appendChild(span);
    div.appendChild(trash);
    span.appendChild(warning);
    return div;
}

/**
 * Applies filters to searched courses
 */
function filterCourses() {
    var filteredCourses

    //Filter by search
    $.getJSON($SCRIPT_ROOT + '/searchClasses', {
        class_name: $('input[id="search-bar"]').val()
    }, function (data, status) {
        filteredCourses = data

        //Filter major
        if (document.getElementById("major-checkbox").checked) {
            var majorReqs = [...document.getElementsByClassName("requirement-list-course")].map(e=>e.childNodes[0].textContent)
            filteredCourses = $.grep(filteredCourses, function (n, i) {
                for(c in majorReqs) {
                    if(n.course_code === majorReqs[c])
                        return true
                }
                return false
            });
        }

        //Filter duplicates
        if (document.getElementById("duplicates-checkbox").checked) {
            filteredCourses = $.grep(filteredCourses, function (n, i) {
                for (let sem = 0; sem < pools.length; sem++) {
                    for (c in pools[sem]) {
                        if (document.getElementById(pools[sem][c]).getAttribute("coursecode").includes(n.course_code)) {
                            return false
                        }
                    }
                }

                return true
            });
        }

        //Filter prereq
        if (document.getElementById("prereq-checkbox").checked) {
            filteredCourses = $.grep(filteredCourses, function (n, i) {
                      return checkRequisites(n.course_code, studentData["grad_semester"], studentData["grad_year"])
            });
        }

        //Filter semester
        var semesterDropdown = document.getElementById("semester-dropdown")
        if (semesterDropdown.value != -1) { //-1 if no semester selected
            filteredCourses = $.grep(filteredCourses, function (n, i) {
                for (let i in listOfCourses) {
                    let course = listOfCourses[i]

                    if (n.course_code === course.courseCode && course.semester === semesterDropdown.value) {
                        return true
                    }
                }

                return false
            });
        }

        //Display courses
        let container = document.getElementById("course-container");
        container.innerHTML = "";
        for (let i in filteredCourses) {
            let course = filteredCourses[i]

            let div = createCourseDiv(course)

            container.appendChild(div)
        }
    });
}




