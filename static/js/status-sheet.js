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
		console.log(value)


		let fieldset = document.createElement("fieldset")
		fieldset.classList = "statusSheetSectionContainer container rounded"

		let legend = document.createElement("legend")
		legend.classList = "StatusSheetTitles"
		legend.innerText = value.title.replaceAll("_", " ")

		fieldset.appendChild(legend)

		let container = document.getElementById("req-list")
		container.appendChild(fieldset)



		/*Special Requirement*/

		if (value.special !== "") {
			let message = value.special;
			let p = document.createElement("p");
			p.innerHTML = message;
			fieldset.appendChild(p)

		}

		/*Normal Requirement*/


		else {

			var clusters = value.clusters
			let clusterKeys = Object.keys(clusters);
			let clusterValues = Object.values(clusters);




			//Examine each cluster
			var count = 0
			for (let cKey of clusterKeys) {
				// console.log(clusters[i])

				

				

				//credit requirement?
				let creds = clusters[cKey].credits;
				let courses = clusters[cKey].courses;
				let alts = clusters[cKey].alternate_clusters;
				// console.log(courses)


				if (creds !== null) {
					let credMsg = "Select " + creds + " credits";
					let msg = document.createElement("p");
					msg.innerHTML = credMsg;
					 fieldset.appendChild(msg)
				}

				

				//Each course in current cluster
				let courselist = document.createElement("ul")
				courselist.className = "fa-ul"
				for (let course = 0; course < courses.length; course++) {
					// console.log(courses[course])
					let currentCourse = courses[course];
					let li = document.createElement("li")
					li.classList = "requirement-list-course"
					li.innerHTML = currentCourse;

					//Add Credits
					let creditSpan = document.createElement("span");
					let creds = getCredits(currentCourse)
					if (creds !== -1) {
						creditSpan.innerText = " - " + creds + " Credits";
					}
					else {
						creditSpan.innerText = " - Course Unavailable!";
					}

					let span = document.createElement("span")
					span.innerHTML = '<i class="far fa-square" style="color: red;"></i>'
					span.className = "fa-li"
					li.appendChild(span)
					li.appendChild(creditSpan)
					courselist.appendChild(li)
				}
				if (count > 0){
					let or = document.createElement("h3");
					or.innerText = "OR"
					fieldset.appendChild(or)
				}
				 fieldset.appendChild(courselist)
				

				for(let i = 0; i < alts.length; i++){
		
					// let altcourselist = document.createElement("ul")
					// let alt = alts[i];

					// let alternate_creds = clusters[alt].credits;
					// let alternate_courses = clusters[alt].courses;
					// if (alternate_creds !== null) {
					// 	let altcredMsg = "Select " + alternatecreds + " credits";
					// 	let altmsg = document.createElement("p");
					// 	msg.innerHTML = altcredMsg;
					// 	fieldset.appendChild(msg)
					// }

					// for (let altcourse = 0; altcourse < alternate_courses.length; altcourse++) {
					// 	// console.log(courses[course])
					// 	let currentAltCourse = alternate_courses[altcourse];
					// 	let li = document.createElement("li")
					// 	li.classList = "requirement-list-course"
					// 	li.innerHTML = currentAltCourse;
	
					// 	//Add Credits
					// 	let altcreditSpan = document.createElement("span");
					// 	let altcreds = getCredits(currentAltCourse)
					// 	if (altcreds !== -1) {
					// 		altcreditSpan.innerText = " - " + altcreds + " Credits";
					// 	}
					// 	else {
					// 		altcreditSpan.innerText = " - Course Unavailable!";
					// 	}
	
					// 	let altspan = document.createElement("span")
					// 	altspan.innerHTML = '<i class="far fa-square" style="color: red;"></i>'
					// 	altspan.className = "fa-li"
					// 	li.appendChild(altspan)
					// 	li.appendChild(altcreditSpan)
					// 	altcourselist.appendChild(li)
	
					// }
					//fieldset.appendChild(altcourselist)
					
					// for (let k in keys) {

				 	// 	if (keys[k] == alt_req_key) {

					// 		keys.splice(k, 1);
					// 	}

				 	// }

				
				}



				count++;
			}

		}



		// let alt_req_key = value.alternate_requirements


		//List alternates if available
		// if (alt_req_key != null) {

			
		// 	let altCourseAry = reqs[alt_req_key].classes


		// 	let altCourselist = document.createElement("ul")
		// 	altCourselist.className = "fa-ul"


		// 	for (let i in altCourseAry) {

		// 		let li = document.createElement("li")
		// 		li.classList = "requirement-list-course"
		// 		let code = altCourseAry[i]
		// 		li.innerHTML = code


		// 		/*Requirement Credits*/
		// 		let creditSpan = document.createElement("span");

		// 		let creds = getCredits(code)
		// 		if (creds !== -1) {
		// 			creditSpan.innerText = " - " + creds + " Credits";
		// 		}
		// 		else {
		// 			creditSpan.innerText = "Course Unavailable!";
		// 		}




		// 		let span = document.createElement("span")
		// 		span.innerHTML = '<i class="far fa-square" style="color: red;"></i>'
		// 		span.className = "fa-li"
		// 		li.appendChild(span)
		// 		li.appendChild(creditSpan)

		// 		altCourselist.appendChild(li)




		// 	}
		// 	fieldset.appendChild(altCourselist)

		// 	//REMOVE KEY FROM LIST



		// } //End Alternates
	}
}

function updateStatusSheet(selectedCourses) {
	let statusSheetCourses = document.getElementsByClassName("requirement-list-course")
	console
	let selectedClasses = document.getElementsByClassName("drag_item drag_item_fill")
	console.log(statusSheetCourses)

	// console.log (selectedClasses)

	for (let courseNum = 0; courseNum < statusSheetCourses.length; courseNum++) {
		let ssCourse = statusSheetCourses[courseNum];
		let ssCode = ssCourse.innerText;
		// console.log(ssCode)
		for (let classNum = 0; classNum < selectedClasses.length; classNum++) {
			console.log("sscode: ", ssCode)
			console.log("other : ", selectedClasses[classNum].getAttribute("coursecode"))

			if (ssCode.includes(selectedClasses[classNum].getAttribute("coursecode"))) {
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
