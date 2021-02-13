let $studentInfo = $('#studentInfo')
let $studentSchedule = $('#studentSchedule')
let student = [];
let schedule = [];

function setStudentInfo(json) {
    student = json;
}

function buildStudentInfo(student) {
    return [
        '<div class="col-4 bg-gcc-primary student-info">',
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

function buildStudentSchedule(schedule) {

}

$(document).ready(function() {
    //Set up student info
    $studentInfo.html('')
    student.forEach(s => {
        $studentInfo.html($studentInfo.html() + buildStudentInfo(s))
    });
});