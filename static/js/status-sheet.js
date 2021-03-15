//TODO Fetch Current Semester from server
curSemester = {
	semester: 'Spring',
	year: '2021'
}


/* Gets number of credits for a coursecode */
function getCredits(code) {

	var returnedCredits = -1;

	let found = false;
	var courseIndex = 0;

	while (!found && courseIndex < listOfCourses.length) {
		let searchedCourse = listOfCourses[courseIndex];

		if (searchedCourse.courseCode === code[0]) {
			found = true;
			returnedCredits = searchedCourse.credits;
		}
		courseIndex++;
	}


	return returnedCredits;
}




function loadStatusSheet(reqs) {
	let keys = Object.keys(reqs)

	for (let key of keys) {
		let value = reqs[key]


		let fieldset = document.createElement("fieldset")
		fieldset.classList = "statusSheetSectionContainer container rounded"

		let legend = document.createElement("legend")
		legend.classList = "StatusSheetTitles"
		legend.innerText = value.title.replaceAll("_", " ")

		fieldset.appendChild(legend)

	

		let container = document.getElementById("req-list")
		container.appendChild(fieldset)

		let courselist = document.createElement("ul")
		courselist.className = "fa-ul"

		if (value.special !== "") {
			let message = value.special;
			let p = document.createElement("p");
			p.innerHTML = message;
			courselist.appendChild(p)

		}
		var courseAry = value.classes
		for (let i in courseAry) {


			let li = document.createElement("li")
			li.classList = "requirement-list-course"

			let code = courseAry[i]
			li.innerHTML = code



			/*Requirement Credits*/
			let creditSpan = document.createElement("span");
			let creds = getCredits(code)
			if (creds !== -1) {
				creditSpan.innerText = " - " + creds + " Credits";
			}
			else {
				creditSpan.innerText = " - Course Unavailable!";
			}


			/* Checkbox */
			let span = document.createElement("span")
			span.innerHTML = '<i class="far fa-square" style="color: red;"></i>'
			span.className = "fa-li"
			li.appendChild(span)
			li.appendChild(creditSpan)
			courselist.appendChild(li)

		}




		fieldset.appendChild(courselist)
		let alt_req_key = value.alternate_requirements


		//List alternates if available
		if (alt_req_key != null) {

			let or = document.createElement("h3")
			or.innerHTML = "OR"
			or.style = "font-weight: bold; font-size: 1.1em"
			fieldset.appendChild(or)
			let altCourseAry = reqs[alt_req_key].classes


			let altCourselist = document.createElement("ul")
			altCourselist.className = "fa-ul"


			for (let i in altCourseAry) {

				let li = document.createElement("li")
				li.classList = "requirement-list-course"
				let code = altCourseAry[i]
				li.innerHTML = code


				/*Requirement Credits*/
				let creditSpan = document.createElement("span");

				let creds = getCredits(code)
				if (creds !== -1) {
					creditSpan.innerText = " - " + creds + " Credits";
				}
				else {
					creditSpan.innerText = "Course Unavailable!";
				}




				let span = document.createElement("span")
				span.innerHTML = '<i class="far fa-square" style="color: red;"></i>'
				span.className = "fa-li"
				li.appendChild(span)
				li.appendChild(creditSpan)

				altCourselist.appendChild(li)




			}
			fieldset.appendChild(altCourselist)

			//REMOVE KEY FROM LIST
			for (let k in keys) {

				if (keys[k] == alt_req_key) {

					keys.splice(k, 1);
				}

			}


		} //End Alternates
	}
}

function updateStatusSheet(selectedCourses) {
	let statusSheetCourses = document.getElementsByClassName("requirement-list-course")
	console.log(selectedCourses)
	let selectedClasses = document.getElementsByClassName("drag_item drag_item_fill")
	for (let courseNum = 0; courseNum < statusSheetCourses.length; courseNum++) {
		let ssCourse = statusSheetCourses[courseNum];
		let ssCode = ssCourse.innerText;
		for (let classNum = 0; classNum < selectedClasses.length; classNum++) {
			if (selectedClasses[classNum].getAttribute("coursecode").includes(ssCode)) {
				let year = selectedClasses[classNum].getAttribute("year")
				let semesterIndex = ALL_SEMESTERS.indexOf(selectedClasses[classNum].getAttribute("semester"))
				if ((year < curSemester.year) || (year === curSemester.year && semesterIndex <= ALL_SEMESTERS.indexOf(curSemester.semester))) {
					console.log(year)
					console.log(year)
					ssCourse.childNodes[1].childNodes[0].classList = "fas fa-check-square"
					ssCourse.childNodes[1].childNodes[0].style = "color: green;"
				}
				else {

					ssCourse.childNodes[1].childNodes[0].classList = "fas fa-hourglass-start"
					ssCourse.childNodes[1].childNodes[0].style = "color: blue;"
				}
				console.log(ssCourse.childNodes)


			}
			// let selectedSemester = ALL_SEMESTERS.indexOf(selectedClasses[classNum].getAttribute("semester"))


		}

	}
}
