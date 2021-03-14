var filterClasses;

function filterDuplicates(checkbox) {
    $.getJSON($SCRIPT_ROOT + '/searchClasses', {
        class_name: $('input[id="search-bar"]').val()
    }, function (data, status) {
        classes = data
        let container = document.getElementById("course-container");
        container.innerHTML = "";
        for (let i in classes) {
            let course = classes[i]

            if (checkbox.checked) {
                var duplicate = false

                for (let sem = 0; sem < pools.length; sem++) {
                    for (c in pools[sem]) {
                        if (document.getElementById(pools[sem][c]).getAttribute("coursecode").includes(course.course_code)) {
                            duplicate = true
                            break
                        }
                    }

                    if (duplicate)
                        break
                }

                if (duplicate)
                    continue
            }

            /* Outer Div */
            let name = course.course_code;

            let courseID = name/*.replace(" ", "_") + "_" + course.semester + "_" + course.year*/;
            let div = document.createElement("div");
            div.id = courseID;
            div.className = "drag_item";
            div.draggable = "true";

            div.setAttribute("semester", course.semester);
            div.setAttribute("courseCode", courseID);
            div.setAttribute("ondragstart", "set_valid_drag_locations(event);drag(event);");
            div.setAttribute("ondragend", "revert_drag_locations(event);dragEnd(event);");

            /* Arrows icon */
            let arrows = document.createElement("i");
            arrows.classList = "col-1 pr-0 pl-0 ml-2 fas fa-arrows-alt";

            /* Class Text */
            let span = document.createElement("span");
            span.classList = "col pr-0 pl-0 drag_item_text text-center";
            span.innerHTML = name;

            /* Trash Can */
            let trash = document.createElement("i");
            trash.classList = "col-1 pr-0 pl-0 fas fa-trash-alt ml-auto m-2 itemInvisible trashRed"
            trash.setAttribute("onclick", "removeDragItem(event)");

            /* Combine elements */

            div.appendChild(arrows)
            div.appendChild(span)
            div.appendChild(trash)
            container.appendChild(div)
        }
    });
}

function filterSemester(semesterDropdown) {
    if (semesterDropdown.value != -1) {
        $.getJSON($SCRIPT_ROOT + '/filterSemester', {
            semester: semesterDropdown.value
        }, function (data, status) {
            classes = data

            let container = document.getElementById("course-container");
            container.innerHTML = "";
            for (let i in classes) {
                let course = classes[i]

                /* Outer Div */
                let name = course.courseCode;

                let courseID = name/*.replace(" ", "_") + "_" + course.semester + "_" + course.year*/;
                let div = document.createElement("div");
                div.id = courseID;
                div.className = "drag_item";
                div.draggable = "true";

                div.setAttribute("semester", course.semester);
                div.setAttribute("courseCode", courseID);
                div.setAttribute("ondragstart", "set_valid_drag_locations(event);drag(event);");
                div.setAttribute("ondragend", "revert_drag_locations(event);dragEnd(event);");

                /* Arrows icon */
                let arrows = document.createElement("i");
                arrows.classList = "col-1 pr-0 pl-0 ml-2 fas fa-arrows-alt";

                /* Class Text */
                let span = document.createElement("span");
                span.classList = "col pr-0 pl-0 drag_item_text text-center";
                span.innerHTML = name;

                /* Trash Can */
                let trash = document.createElement("i");
                trash.classList = "col-1 pr-0 pl-0 fas fa-trash-alt ml-auto m-2 itemInvisible trashRed"
                trash.setAttribute("onclick", "removeDragItem(event)");

                /* Combine elements */

                div.appendChild(arrows)
                div.appendChild(span)
                div.appendChild(trash)
                container.appendChild(div)
            }
        });
    }
    else {
        $.getJSON($SCRIPT_ROOT + '/searchClasses', {
            class_name: $('input[id="search-bar"]').val()
        }, function (data, status) {
            classes = data
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

                div.setAttribute("semester", course.semester);
                div.setAttribute("courseCode", courseID);
                div.setAttribute("ondragstart", "set_valid_drag_locations(event);drag(event);");
                div.setAttribute("ondragend", "revert_drag_locations(event);dragEnd(event);");

                /* Arrows icon */
                let arrows = document.createElement("i");
                arrows.classList = "col-1 pr-0 pl-0 ml-2 fas fa-arrows-alt";

                /* Class Text */
                let span = document.createElement("span");
                span.classList = "col pr-0 pl-0 drag_item_text text-center";
                span.innerHTML = name;

                /* Trash Can */
                let trash = document.createElement("i");
                trash.classList = "col-1 pr-0 pl-0 fas fa-trash-alt ml-auto m-2 itemInvisible trashRed"
                trash.setAttribute("onclick", "removeDragItem(event)");

                /* Combine elements */

                div.appendChild(arrows)
                div.appendChild(span)
                div.appendChild(trash)
                container.appendChild(div)
            }
        });
    }
}