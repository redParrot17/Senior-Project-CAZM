let ALL_SEMESTERS = ["January", "Spring", "May", "Summer", "Fall", "Winter Online"];
let invalidCombos = [];
var studentData





function addClassHolder(semester, year, semesterOrder) {
  document.getElementById("main-schedule").innerHTML += `
  <fieldset class="container scheduleContainer rounded" data-semester="${semester}" data-year="${year}" data-order="${semesterOrder}">
    <legend > ${semester} ${year}</legend>
    <div class="row rounded mb-2 drag_box_container mt-0" id="${semester}-${year}">
        <div class="col-6 drag_box">
            <div class="drag_container rounded" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
        </div>
    </div>
  </fieldset>`;
}

function setUpStudentScheduleContainers(studentData) {
  year = studentData.enrolled_year;

  while (year <= studentData.grad_year){
    counter = 0;
    for (i = 0; i < 6; i++) {

      if ((year === studentData.enrolled_year)&&(i === 0)&&(counter === 0)){
        i = ALL_SEMESTERS.indexOf(studentData.enrolled_semester);
        counter = counter + 1;
      }
      addClassHolder(ALL_SEMESTERS[i], year, 0);
      if ((year === studentData.grad_year) && (i>=ALL_SEMESTERS.indexOf(studentData.grad_semester))){
        year ++;
        break;
      }
      if (i===5){
        year++;
      }
    }
  }
}


function set_valid_drag_locations(event) {

  let dragItem = event.target; // item being dragged
  let dragItemId = dragItem.id; // id of item being dragged

  // find what are valid drop locations
  validSemesters = [];
  years = [];
  combined = [];
  for (i = 0; i < listOfCourses.length; i++) {
    // get the current course
    let currentCourse = listOfCourses[i];
    // see if it is the one we want
    console.log(dragItemId)
    if (dragItemId.includes(currentCourse.courseCode)) {

      // get items
      let year = currentCourse.year;
      let semester = currentCourse.semester;
      
      // add to array
      years.push(year);
      validSemesters.push(semester);
      combined.push(`${semester}-${year}`);
    }
  }
  //console.log(validSemesters, years, combined);

  // block non-valid
  invalidSemesters = [];
  for (let i = 0; i < ALL_SEMESTERS.length; i++) {
    if(!validSemesters.includes(ALL_SEMESTERS[i])) {
      invalidSemesters.push(ALL_SEMESTERS[i]);

      for (let year = studentData.enrolled_year; year <= studentData.grad_year; year++) {
        invalidCombos.push(`${ALL_SEMESTERS[i]}-${year}`)
      }
    }
  }

  //console.log("INVALID", invalidSemesters, invalidCombos);

  // go over invalid objects
  invalidCombos.forEach((item, index) => {
      let dropContainer = document.getElementById(item);

      if (dropContainer) { // if item found
        // make unable to drop

        dropContainer.parentElement.classList.add('greyOut');
        dropContainer.querySelectorAll(".drag_container").forEach((item) => {
          item.removeAttribute("ondrop");
        });
        dropContainer.querySelectorAll(".drag_container").forEach((item) => {
          item.removeAttribute("ondragover");
        });
      }
  });

  combined.forEach((item1, index) => {
    let dropContainer = document.getElementById(item1);
    // console.log(dropContainer);

    let checkId = dragItemId + "-" + item1;
    // console.log(checkId);

    let hasCourse = dropContainer.querySelectorAll(".drag_item_fill");
    // console.log(hasCourse);

    if(hasCourse.length > 0){
      // console.log("got in");

      hasCourse.forEach((item2, index) => {
        if(item2.id == checkId){

          dropContainer.parentElement.classList.add('greyOut');
          dropContainer.querySelectorAll(".drag_container").forEach((item3) => {
            item3.removeAttribute("ondrop");
          });
          dropContainer.querySelectorAll(".drag_container").forEach((item3) => {
            item3.removeAttribute("ondragover");
          });


          invalidCombos.push(item1);
        }
      });
    }
  });

}


function revert_drag_locations(event) {
  // go over invalid objects
  invalidCombos.forEach((item, index) => {
      let dropContainer = document.getElementById(item);

      if (dropContainer) { // if item found
        // make able to drop

        dropContainer.parentElement.classList.remove('greyOut');
        dropContainer.querySelectorAll(".drag_container").forEach((item) => {
          item.setAttribute("ondrop", "drop(event)");
        });
        dropContainer.querySelectorAll(".drag_container").forEach((item) => {
          item.setAttribute("ondragover", "allowDrop(event)");
        });
      }
  });

  // clear invalid positions
  while (invalidCombos.length) { invalidCombos.pop(); }
}









//------------------------------------------------------------------------------
$.getJSON($SCRIPT_ROOT + '/studentData', {

}, function (data) {
    studentData = data;
    console.log(studentData);
    // set up student schedule containers
    setUpStudentScheduleContainers(studentData);

})

