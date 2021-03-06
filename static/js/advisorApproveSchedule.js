/**
 * Submits the current schedule from the edit page
 * @param {*} ev 
 */
function approveBtn(ev){
  let container = document.getElementById("main-schedule");
  let newSchedule = container.querySelectorAll(".drag_item_fill");
  let approve = document.getElementById("approveBtn")
  approve.innerHTML = `<div id="status-sheet-spinner" class="d-flex justify-content-center">
                      <div class="spinner-border text-light" role="status">
    <span class="sr-only">Loading...</span>
  </div>
</div>`

  let changed = (scheduleChangesAdded.length > 0 || scheduleChangesRemoved.length > 0);

  let myCourses = [];
  let creds = totalCreds();
  newSchedule.forEach((item, index) => {
    let elements = (item.id).split("-");
    let course_code = elements[0];
    let semester = elements[1];
    let year = elements[2];

    myCourses.push({"course_code":course_code, "semester":semester, "year":year});

  });

  let data = {
    "changed": changed,
    "courses":myCourses,
    "newCredits": creds,
    "student_id":student_id
  }
  $.ajax
    ({
        type: "POST",
        //the url where you want to sent the userName and password to
        url: '/advisorSchReviewPost/',
        dataType: 'json',
        contentType: "application/json",
        //json object to sent to the authentication url
        data: JSON.stringify(data),
        success: function (data) {

          document.getElementById("advisorBackBtn").click();

        }
    })
}

/**
 * Changes the Approve button text based on what the approve button will set the status to. i.e., "Approve Schedule", or "Submit for student approvel"
 */
function setApproveBtnText() {
  let approveBtn = document.getElementById("approveBtn");

  if (studentStatus == 1 && scheduleChanged == false){
    approveBtn.innerHTML = "Approve Schedule";
    approveBtn.classList.remove("itemInvisible");
  }
  else if (studentStatus == 1 && scheduleChanged == true){
    approveBtn.innerHTML = "Save and Submit for Student's Approval";
    approveBtn.classList.remove("itemInvisible");
  }
  else if (studentStatus == 2){
    approveBtn.innerHTML = "Save and Submit for Student's Approval";
    approveBtn.classList.remove("itemInvisible");
  }
  else if (studentStatus == 3 && scheduleChanged == false){
    approveBtn.classList.add("itemInvisible");
  }
  else if (studentStatus == 3 && scheduleChanged == true){
    approveBtn.innerHTML = "Save and Submit for Student's Approval";
    approveBtn.classList.remove("itemInvisible");
  }
  else if (studentStatus == 4 && scheduleChanged == false){
    approveBtn.classList.add("itemInvisible");
  }
  else{
    approveBtn.innerHTML = "Save and Submit for Student's Approval";
    approveBtn.classList.remove("itemInvisible");
  }
}
setApproveBtnText();
