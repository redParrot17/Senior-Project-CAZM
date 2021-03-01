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


    ''' 
    EXAMPLE JSON:

    {
        "COURSE CODE": {
            REQUIREMENT_TYPE: {
                REQUIREMENT_GROUP: [REQUISITE CODE, REQUISITE CODE],
                REQUIREMENT_GROUP: [REQUISITE CODE, REQUISITE CODE, REQUISITE CODE]
            }
    }

    }

    '''
    def getRequisites(self):
        cursor = self.db.cursor(buffered=True)
        
        sql = """
        SELECT COURSE_CODE, REQUISITE_CODE, TYPE, REQUISITE_GROUP FROM REQUISITES
            """
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        courses = {}

        for course_code, requisite_code, type, group in results:
            if course_code not in courses:
                #Make new K/V Pair course_code
                courses[course_code] =  {type : {group: [requisite_code]}}
            else:

                if type in courses[course_code]:
                    if group in courses[course_code][type]:
                        courses[course_code][type][group].append(requisite_code)
                    else:
                        courses[course_code][type][group] = [requisite_code]
                else:
                    courses[course_code][type] = {group: [requisite_code]}
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
