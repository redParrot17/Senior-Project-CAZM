
function approveBtn(ev){
  let container = document.getElementById("main-schedule");
  let newSchedule = container.querySelectorAll(".drag_item_fill");
  //console.log(newSchedule);

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
    "newCredits": creds
  }
  $.ajax
    ({
        type: "POST",
        //the url where you want to sent the userName and password to
        url: '/studentSchReview/',
        dataType: 'json',
        contentType: "application/json",
        //json object to sent to the authentication url
        data: JSON.stringify(data),
        success: function (data) {
          //alert("Data: " + data);
          window.location.href='/studentLanding';

        }
    })
}


function setApproveBtnText() {
  let approveBtn = document.getElementById("approveBtn");

  if (studentStatus == 1 && scheduleChanged == false){
    approveBtn.classList.add("itemInvisible");
    //approveBtn.classList.add("itemInvisible");
  }
  else if (studentStatus == 1 && scheduleChanged == true){
    approveBtn.innerHTML = "Save and Submit for Approval";
    approveBtn.classList.remove("itemInvisible");
    //approveBtn.classList.remove("itemInvisible");
  }
  else if (studentStatus == 2){
    approveBtn.innerHTML = "Save and Submit for Approval";
    approveBtn.classList.remove("itemInvisible");
    //approveBtn.classList.remove("itemInvisible");
  }
  else if (studentStatus == 3 && scheduleChanged == false){
    approveBtn.innerHTML = "Approve Schedule";
    approveBtn.classList.remove("itemInvisible");
    //approveBtn.classList.remove("itemInvisible");
  }
  else if (studentStatus == 3 && scheduleChanged == true){
    approveBtn.innerHTML = "Save and Submit for Approval";
    approveBtn.classList.remove("itemInvisible");
    //approveBtn.classList.remove("itemInvisible");
  }
  else if (studentStatus == 4 && scheduleChanged == false){
    approveBtn.classList.add("itemInvisible");
    //approveBtn.classList.add("itemInvisible");
  }
  else{// (studentStatus == 4 && scheduleChanged = true){
    approveBtn.innerHTML = "Save and Submit for Approval";
    approveBtn.classList.remove("itemInvisible");
    //approveBtn.classList.remove("itemInvisible");
  }
}
setApproveBtnText();
