function toggleSideBar(event){
  let btn=document.getElementById("toggleBtn");
  if(btn.classList.contains("selected")){
    document.getElementById("mySidebar").style.width = "0";
    document.getElementById("middle").style.marginRight= "0";
    document.getElementById("nav").style.marginRight= "0";
    btn.classList.remove("selected");
    btn.innerHTML='<i class=" openbtn fas fa-arrow-circle-left rounded-circle" ></i>';
  }
  else{
    btn.classList.add("selected");
    document.getElementById("mySidebar").style.width = "25%";
    document.getElementById("middle").style.marginRight = "25%";
    document.getElementById("nav").style.marginRight = "25%";

    btn.innerHTML='<i class=" openbtn fas fa-arrow-circle-right rounded-circle" ></i>';
  }

}
function openNav() {
  document.getElementById("mySidebar").style.width = "50hw";
  document.getElementById("middle").style.marginRight = "50hw";
  //document.getElementById("nav").style.marginRight = "275px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("middle").style.marginRight= "0";
  //document.getElementById("nav").style.marginRight= "0";
}

function searchClasses() {
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
          div.courseCode = courseID;
          div.className = "drag_item";
          div.draggable = "true";

          div.setAttribute("courseCode",courseID);
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
