import mysql.connector



class Database:

    def __init__(self, config_file='mysql.cnf'):
        self.db = mysql.connector.connect(option_files=config_file, autocommit=True)

    def close(self):
        self.db.close()

    def select_example(self, argument1, argument2):

        # create a cursor to execute sql statements with
        cursor = self.db.cursor(buffered=True)

        # define the sql statement you want to execute
        sql = "SELECT foo, bar FROM table-name WHERE foo=%s AND bar=%s;"

        # create a tuple of arguments you need to pass
        arg = (argument1, argument2)

        # execute the sql statement
        cursor.execute(sql, arg)

        # fetch all the rows resulting from the sql statement return value
        results = cursor.fetchall()

        # close the cursor
        cursor.close()

        # do something with the results
        return_value = []
        for foo, bar in results:
            return_value.append([foo, bar])
        return return_value

    def getRequirementClasses(self, requirement_id, title):
        cursor = self.db.cursor(buffered=True)
        args = (title, requirement_id)
        sql = """
        SELECT
        COURSE_CODE
        FROM REQUIREMENT INNER JOIN REQUIREMENT_COURSES
        USING(REQUIREMENT_ID)
        WHERE TITLE=%s AND REQUIREMENT_ID=%s;
            """
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        courses = []

        for course in results:
            courses.append(course)

        return courses

    def getRequirements(self, major_name, major_year):
        cursor = self.db.cursor(buffered=True)
        args = (major_name, major_year)
        sql = """
        SELECT
        REQUIREMENT_ID, TITLE, REQUIRED_CREDITS, ALTERNATE_REQUIREMENTS
        FROM MAJOR_REQUIREMENTS INNER JOIN REQUIREMENT
        ON REQUIREMENT.REQUIREMENT_ID = MAJOR_REQUIREMENTS.MAJOR_REQUIREMENT_ID
        WHERE MAJOR_NAME=%s AND MAJOR_YEAR=%s;
            """
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        req_info = {}
        for requirement_id, title, required_credits, alternate_requirements in results:
            req_info[requirement_id] = {
                "alternate_requirements" : alternate_requirements,
                "required_credits" : required_credits,
                "title": title,
                "classes": self.getRequirementClasses(requirement_id, title)
            }

        return req_info

    def search_course_codes(self, argument1):
         cursor = self.db.cursor(buffered=True)
         arg1 = argument1 + "%"
         arg2 = arg1
         args = (arg1,arg2)
         sql = 'SELECT COURSE_CODE, ANY_VALUE(NAME), ANY_VALUE(YEAR), ANY_VALUE(SEMESTER) FROM COURSE WHERE COURSE_CODE LIKE %s OR NAME LIKE %s GROUP BY COURSE_CODE;'
         cursor.execute(sql, args)
         results = cursor.fetchall()
         cursor.close()

         course_info = []
         for course_code, name, year, semester in results:
             course_info.append({"course_code":course_code,"name":name,"year": year, "semester": semester})
         return course_info

    def get_all_courses(self):
         cursor = self.db.cursor(buffered=True)
         sql = 'SELECT COURSE_CODE, ANY_VALUE(YEAR), ANY_VALUE(SEMESTER) FROM COURSE GROUP BY COURSE_CODE;'
         cursor.execute(sql)
         results = cursor.fetchall()
         cursor.close()

         course_info = []
         for course_code, year, semester in results:
             course_info.append({"courseCode": course_code, "year":year, "semester":semester})
         print(course_info)
         return course_info

    def get_template(self, major_code):
        cursor = self.db.cursor(buffered=True)

        args = (major_code,)
        sql = 'SELECT COURSE_CODE, SEMESTER, YEAR FROM SCHEDULE_COURSES WHERE SCHEDULE_ID=%s ORDER BY YEAR ASC, SEMESTER DESC;'
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        template = []
        courses = []
        current_semester = "FALL"
        current_year = "2020"
        for course_code, semester, year in results:
            if courses and semester + str(year) != current_semester + current_year:
                template.append({'semester': current_semester, 'year':current_year, 'classes': courses}) #append semester schedule to template
                courses = [] #clear courses
                current_semester = semester
                current_year = str(year)
            courses.append(course_code)

        return template

    # METHODS FOR THE MAJOR TABLE #

    def does_major_exist(self, major_name: str, major_year: int) -> bool:
        """ Checks whether or not a specific major exists within the database.

        :param major_name: name of the major
        :param major_year: year the major is offered
        :return: True if the entry exists, False otherwise
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'SELECT 1 FROM MAJOR WHERE MAJOR_NAME=%s AND MAJOR_YEAR=%s;'
        arguments = (major_name, major_year,)

        cursor.execute(sql_query, arguments)
        major_exists = cursor.fetchone() is not None

        cursor.close()
        return major_exists

    def create_new_major(self, major_name: str, major_year: int):
        """ Adds a new major to the database.

        :param major_name: name of the major
        :param major_year: year the major is offered
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'INSERT IGNORE INTO MAJOR (MAJOR_NAME, MAJOR_YEAR) VALUES (%s, %s);'
        arguments = (major_name, major_year,)

        cursor.execute(sql_query, arguments)
        cursor.close()

    def delete_old_major(self, major_name: str, major_year: int):
        """ Deletes an existing major from the database.

        :param major_name: name of the major
        :param major_year: year the major is offered
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'DELETE FROM MAJOR WHERE MAJOR_NAME=%s AND MAJOR_YEAR=%s;'
        arguments = (major_name, major_year,)

        cursor.execute(sql_query, arguments)
        cursor.close()

    # METHODS FOR THE STUDENT MAJOR TABLE #

    def get_student_majors(self, student_id: int) -> list:
        """ Gets a student's major and year information from the database.

        Example return:

            [('Computer Science', 2017), ('Mathematics', 2017)]

        :param student_id: student's unique identifier
        :return: list of tuples of the major name and year
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'SELECT MAJOR_NAME, MAJOR_YEAR FROM STUDENT_MAJOR WHERE STUDENT_ID=%s;'
        arguments = (student_id,)

        cursor.execute(sql_query, arguments)
        results = cursor.fetchall()

        cursor.close()
        return results

    def add_major_to_student(self, student_id: int, major_name: str, major_year: int):
        """ Adds the specified major information to the database and ignores duplicate entries.

        Example::

            # Define parameters to use
            major_name = 'Advanced Pottery'
            major_year = 2017

            # Ensure the major exists
            if not database.does_major_exist(major_name, major_year):
                create_new_major(major_name, major_year)

            # Add the major to student
            database.add_major_to_student(123456, major_name, major_year)

        :param student_id: student's unique identifier
        :param major_name: name of the student's major
        :param major_year: year the student joined the major

        :raises mysql.connector.errors.IntegrityError: if the major does not exist in the major table
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'INSERT INTO STUDENT_MAJOR (STUDENT_ID, MAJOR_NAME, MAJOR_YEAR) VALUES (%s, %s, %s) ' \
                    'ON DUPLICATE KEY UPDATE STUDENT_ID=VALUES(STUDENT_ID), MAJOR_NAME=VALUES(MAJOR_NAME), ' \
                    'MAJOR_YEAR=VALUES(MAJOR_YEAR);'
        arguments = (student_id, major_name, major_year,)

        cursor.execute(sql_query, arguments)
        cursor.close()

    def remove_major_from_student(self, student_id: int, major_name: str, major_year: int):
        """ Removes the specified major information from the database for a student.

        :param student_id: student's unique identifier
        :param major_name: name of the student's major
        :param major_year: year the student joined the major
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'DELETE FROM STUDENT_MAJOR WHERE STUDENT_ID=%s AND MAJOR_NAME=%s AND MAJOR_YEAR=%s;'
        arguments = (student_id, major_name, major_year,)

        cursor.execute(sql_query, arguments)
        cursor.close()

    def remove_all_majors_from_student(self, student_id: int):
        """ Removes all major information from the database for a student.

        :param student_id: student's unique identifier
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'DELETE FROM STUDENT_MAJOR WHERE STUDENT_ID=%s;'
        arguments = (student_id,)

        cursor.execute(sql_query, arguments)
        cursor.close()

    # METHODS FOR THE STUDENTS TABLE #




    # ADVISEE METHODS #

    def update_advisee(
            self, 
            advisor_id, 
            student_id, 
            first_name, 
            last_name, 
            email,
            classification,
            graduation_year, 
            credits_completed):
        cursor = self.db.cursor(buffered=True)

        sql_query = """
            INSERT INTO STUDENTS 
            (ADVISOR_ID, STUDENT_ID, FIRST, LAST, EMAIL, CLASSIFICATION, GRAD_YEAR, CREDITS_COMPLETED) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE 
            ADVISOR_ID=VALUES(ADVISOR_ID), FIRST=VALUES(FIRST), LAST=VALUES(LAST), EMAIL=VALUES(EMAIL), 
            CLASSIFICATION=VALUES(CLASSIFICATION), GRAD_YEAR=VALUES(GRAD_YEAR), CREDITS_COMPLETED=VALUES(CREDITS_COMPLETED);
            """
        
        arguments = (
            advisor_id, 
            student_id, 
            first_name, 
            last_name, 
            email, 
            classification, 
            graduation_year, 
            credits_completed,)

        cursor.execute(sql_query, arguments)
        cursor.close()

    def get_advisee(self):
        pass

    def get_all_advisees(self, advisor_id: int) -> list:
        return []

    def delete_advisee(self, advisor_id: int, advisee_id: int):
        cursor = self.db.cursor(buffered=True)
        sql_query = 'DELETE FROM STUDENTS WHERE ADVISOR_ID=%s AND STUDENT_ID=%s;'
        arguments = (advisor_id, advisee_id,)
        cursor.execute(sql_query, arguments)
        cursor.close()

    def delete_all_advisees(self, advisor_id: int):
        cursor = self.db.cursor(buffered=True)
        sql_query = 'DELETE FROM STUDENTS WHERE ADVISOR_ID=%s;'
        arguments = (advisor_id,)
        cursor.execute(sql_query, arguments)
        cursor.close()
