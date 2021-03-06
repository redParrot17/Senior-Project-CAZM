function createDiv(parentNode) {
    let div = document.createElement('div');
    div.setAttribute('class', 'col-6 drag_box');
    div.innerHTML = '<div class="drag_container rounded" ondrop="drop(event)" ondragover="allowDrop(event)"></div>';
    parentNode.appendChild(div);
}

function removeDiv(div) {
    div.remove();
}


function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    // get data
    let targetNode = ev.target;                              // get the target node (drag_container)
    let targetNodeParent = targetNode.parentElement;         // get the target node (drag_box)
    let targetNodeContainer = targetNodeParent.parentElement;// get the target node (drag_box_container)

    // if the place dragged from was a (drag_box > drag_container) div, add
    if( targetNodeContainer.classList.contains("drag_box") ) {
        targetNodeContainer.id = "CurrentDrag";
    }

    ev.dataTransfer.setData("text", ev.target.id);         // set drag item id
}

function dragEnd(ev) {
        ev.preventDefault();
        // if dropType is none, the item wasn't dropped in a valid location
        let dropType = ev.dataTransfer.dropEffect;

        // if sourceParent.id = CurrentDrag remove it
        let sourceParentContainer = ev.srcElement.parentElement.parentElement;
        if(dropType === "none" || sourceParentContainer.id === "CurrentDrag") {
            // get data
            let targetNode = ev.target;                              // get the target node (drag_container)
            let targetNodeParent = targetNode.parentElement;         // get the target node (drag_box)
            let targetNodeContainer = targetNodeParent.parentElement;// get the target node (drag_box_container)

            // if the place dragged from was a (drag_box > drag_container) div, add
            if( targetNodeContainer.classList.contains("drag_box") ) {
                targetNodeContainer.id = ""; // remove the "CurrentDrag" id

            }
        }

    }

function drop(ev) {
    ev.preventDefault();                                     // prevent default behaivor (link opening)

    // get data
    let id = ev.dataTransfer.getData("text");                // Get the item transfered id

    let targetNode = ev.target;                              // get the target node (drag_container)
    let targetNodeParent = targetNode.parentElement;         // get the target node (drag_box)
    let targetNodeContainer = targetNodeParent.parentElement;// get the target node (drag_box_container)
    let targetNodeSemester = targetNodeContainer.parentElement; //get the semester box dragged into
    let courseNode = document.getElementById(id)
    // check if (drag_box > drag_container) div already has an item
    if (!targetNode.classList.contains("drag_container")) {
        return;
    }

    document.getElementById(id).setAttribute("year", targetNodeSemester.dataset.year)
    document.getElementById(id).setAttribute("semester", targetNodeSemester.dataset.semester)


    // add dragged item to drag_container
    let clone = courseNode.cloneNode(true);
    targetNode.appendChild(clone);     // add the item transfered to the target element
    ev.preventDefault();
    targetNode.classList.add("border");

    if(document.getElementById(id).childNodes.length == 7){
      document.getElementById(id).childNodes[5].classList.remove("itemInvisible");
    }               // makes spot white bg
    if(document.getElementById(id).childNodes.length == 3){
      document.getElementById(id).childNodes[2].classList.remove("itemInvisible");
    }
    clone.classList.add("drag_item_fill");
    let newID = clone.getAttribute("courseCode")+"-"+targetNodeContainer.id;
    clone.id = document.getElementById(id).getAttribute("courseCode")+"-"+targetNodeContainer.id;
    // create a new (drag_box > drag_container) div

    //add dragged item to list of changed courses on Schedule
    if(scheduleChangesRemoved.includes(clone.id)){
      scheduleChangesRemoved = scheduleChangesRemoved.filter(function(e) { return e != clone.id});
    }
    else{
      scheduleChangesAdded.push(clone.id);
    }
    scheduleChanged = (scheduleChangesAdded.length > 0 || scheduleChangesRemoved.length > 0);
    setApproveBtnText();

    createDiv(targetNodeContainer);                          // create a new div for elements to be dragged to


    // remove the (drag_box > drag_container) div the node was dragged from
    let parentNode = document.getElementById("CurrentDrag"); // Select the node previous to the drop
    if( parentNode != null && parentNode.classList.contains("drag_box") ) {
        removeDiv(parentNode);                               // if a valid item to remove remove the item
    }

    // setWarnings(clone.getAttribute("coursecode"), clone.getAttribute("semester"), clone.getAttribute("year"), clone,true)

    addClassestoPools();
    checkPools(true);
    updateStatusSheet(pools);

    //Refilter courses in case hide duplicates is checked
    filterCourses()

    //reset credit count
    let creditSemester = targetNodeSemester.getAttribute("data-semester");
    let creditYear = targetNodeSemester.getAttribute("data-year");
    let creditCount = 0;
    targetNodeSemester.querySelectorAll(".drag_item_fill").forEach((item) => {
      creditCount += getCreditsForSum(item.getAttribute("coursecode"));
    });

    if(creditSemester == "Winter Online" || creditSemester == "January" || creditSemester == "May" || creditSemester == "Early Summer" || creditSemester == "Late Summer"){
      let creditDisplay = document.getElementById(creditSemester+"-"+creditYear+"-credits");
      creditDisplay.innerHTML = `Scheduled Credits: ${creditCount}`;
    }
    else{
      let creditDisplay = document.getElementById(creditSemester+"-"+creditYear+"-credits");
      if(creditCount >17){
        creditDisplay.innerHTML = `<i data-toggle="tooltip" data-delay="0" title="Credit Count High: There will be an added fee" class="fas fa-exclamation-triangle"></i> Scheduled Credits: ${creditCount}`;
			}
			else if(creditCount < 12 ){
        creditDisplay.innerHTML = `<i data-toggle="tooltip" data-delay="0" title="Credit Count Low: Need more credits for full time" class="fas fa-exclamation-triangle"></i> Scheduled Credits: ${creditCount}`;
			}
			else{
        creditDisplay.innerHTML = `Scheduled Credits: ${creditCount}`;

			}

    }
}

//when the trash can is clicked remove the item from it's semester container
function removeDragItem(ev) {

  let parentNode = ev.target.parentElement.parentElement.parentElement;
  let targetNodeSemester = parentNode.parentElement.parentElement;
  if( parentNode != null && parentNode.classList.contains("drag_box") ) {
      removeDiv(parentNode);                               // if a valid item to remove remove the item
  }

  let idCheck = ev.target.parentElement.id;

  if(scheduleChangesAdded.includes(idCheck)){
    scheduleChangesAdded = scheduleChangesAdded.filter(function(e) { return e != idCheck});
  }
  else{
    scheduleChangesRemoved.push(idCheck);
  }
  scheduleChanged = (scheduleChangesAdded.length > 0 || scheduleChangesRemoved.length > 0);
  setApproveBtnText();

  addClassestoPools();
  checkPools(true);
  updateStatusSheet(pools);

  //Refilter courses in case hide duplicates is checked
  filterCourses()

  //reset credit count
  let creditSemester = targetNodeSemester.getAttribute("data-semester");
  let creditYear = targetNodeSemester.getAttribute("data-year");
  let creditCount = 0;
  targetNodeSemester.querySelectorAll(".drag_item_fill").forEach((item) => {
    creditCount += getCreditsForSum(item.getAttribute("coursecode"));
  });

  if(creditSemester == "Winter Online" || creditSemester == "January" || creditSemester == "May" || creditSemester == "Early Summer" || creditSemester == "Late Summer"){
    let creditDisplay = document.getElementById(creditSemester+"-"+creditYear+"-credits");
    creditDisplay.innerHTML = `Scheduled Credits: ${creditCount}`;
  }
  else{
    let creditDisplay = document.getElementById(creditSemester+"-"+creditYear+"-credits");
    if(creditCount >17){
      creditDisplay.innerHTML = `<i data-toggle="tooltip" data-delay="0" title="Credit Count High: There will be an added fee" class="fas fa-exclamation-triangle"></i> Scheduled Credits: ${creditCount}`;
    }
    else if(creditCount < 12 ){
      creditDisplay.innerHTML = `<i data-toggle="tooltip" data-delay="0" title="Credit Count Low: Need more credits for full time" class="fas fa-exclamation-triangle"></i> Scheduled Credits: ${creditCount}`;
    }
    else{
      creditDisplay.innerHTML = `Scheduled Credits: ${creditCount}`;

    }

  }


}


