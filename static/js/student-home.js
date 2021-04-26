let $studentInfo = $('#studentInfo')
let $studentSchedule = $('#studentSchedule')
let student = [];
let schedule = [];

function setStudentInfo(json) {
    student = json;
}

/**
 * Get student info and create DOM element for it
 * @param {*} student 
 * @returns student info DOM element
 */
function buildStudentInfo(student) {
    return [
        '<div class="bg-gcc-primary p-2 student-info rounded">',
                    `<h1>${student.name}</h1>`,
                    `<h2>Student ID: ${student.id}</h2>`,

                    '<div class="container" style="margin-top: 40px;">',
                        `<p>Credits Completed: ${student.credits}</p>`,
                        `<p>Graduation Semester: ${student.grad_semester}</p>`,
                        `<p>Major: ${student.major}</p>`,
                        `<p>Schedule Status: ${student.status}</p>`,
                    '</div>',
                '</div>'
    ].join('')
}
