from bs4 import BeautifulSoup
import requests


class DataCollection:
    BASEURL = 'https://my.gcc.edu'

    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__session = None
        self.response = None

    def http_get(self, url, **kwargs):
        if self.__session is None:
            self._create_session()
        self.response = self.__session.get(url, **kwargs)
        return self.response

    def http_post(self, url, **kwargs):
        if self.__session is None:
            self._create_session()
        self.response = self.__session.post(url, **kwargs)
        return self.response

    def ensure_screen(self, url):
        if self.response is None or self.response.url != url:
            self.http_get(url)

    def to_url(self, path):
        if path.startswith(self.BASEURL):
            return path
        path = '/' + path.lstrip('/')
        return self.BASEURL + path

    def make_soup(self, features='html.parser'):
        """Makes a BeautifulSoup object for the last GET or POST response.

        :param features: - Desirable features of the parser to be
         used. This may be the name of a specific parser ("lxml",
         "lxml-xml", "html.parser", or "html5lib") or it may be the
         type of markup to be used ("html", "html5", "xml"). It's
         recommended that you name a specific parser, so that
         Beautiful Soup gives you the same results across platforms
         and virtual environments. (defaults to html.parser)

        :return: the BeautifulSoup object or None if no response exists
        """
        if self.response is not None:
            return BeautifulSoup(self.response.text, features=features)
        return None

    def prepare_payload(self, payload=None, postback: str=None, search=''):
        """This formats a payload dictionary to include within POST and GET requests.

        https://my.gcc.edu/ uses the values of hidden html input tags to keep track
        of the context of actions. It requires the values of those tags to be attached
        to the payload, so this method automatically takes care of adding in those values.

        :param payload: - the dictionary to prepare (defaults to making a new dictionary)
        :param postback: - an optional postback string "javascript:__doPostBack('eventTargetValue','eventArgumentValue')"
        :param search: - the default search parameter (set to None to exclude search)
        :return: the newly prepared payload dictionary
        """

        # default to a new empty dictionary if none was provided
        if payload is None:
            payload = {}

        # mygcc uses the values of several hidden html tags to track the
        # current viewstate of the user in order to determine context.
        # This fetches and includes those tags within the payload.
        soup = self.make_soup()
        if soup is not None:
            for hidden_input in soup.find_all('input', {'type': 'hidden'}):
                input_name = hidden_input.get('name')
                input_value = hidden_input.get('value')
                if input_name is not None and input_value is not None:
                    payload[input_name] = input_value

        # If a formatted postback string was included, we need to parse it
        # this string tells mygcc what action the user is attempting to do.
        if postback is not None:
            # javascript:__doPostBack('eventTargetValue','eventArgumentValue')
            postback = postback.replace('javascript:__doPostBack(', '')
            postback = postback.replace(')', '')
            postback = postback.replace("'", '')
            postback_elements = postback.split(',', 1)
            if len(postback_elements) == 2:
                payload['__EVENTTARGET'] = postback_elements[0]
                payload['__EVENTARGUMENT'] = postback_elements[1]

        # This empty search tag is included in most requests, so we
        # automatically include it unless told otherwise.
        if search is not None:
            payload['siteNavBar$ctl00$tbSearch'] = search

        return payload

    def _create_session(self):
        """Creates a new Session and performs login"""
        url = self.to_url('/ICS/')
        payload = {
            '_scriptManager_HiddenField': '',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            '__VIEWSTATEGENERATOR': '',
            '___BrowserRefresh': '',
            'siteNavBar$ctl00$tbSearch': '',
            'userName': self.__username,
            'password': self.__password,
            'siteNavBar$btnLogin': 'Login'}
        self.__session = requests.Session()
        self.response = self.__session.post(url, data=payload)


class ProfileInformation:
    PROFILEURL = 'https://my.gcc.edu/ICS/'

    def __init__(self, data_collection: DataCollection):
        self.dc = data_collection
        self._screen = None

        # About me
        self.__user_id = None
        self.__photo = None
        self.__name = None
        self.__birthday = None
        self.__gender = None
        self.__ethnicity = None
        self.__marital_status = None

        # Contact information
        # TODO: implement contact information properties

        # Academic information
        self.__major = None
        self.__minor = None
        self.__certification = None
        self.__concentration = None
        self.__degree_honor = None
        self.__course_of_study = None
        self.__classification = None
        self.__division = None
        self.__academic_status = None
        self.__enrolled_date = None
        self.__planned_grad = None
        self.__max_credits = None
        self.__ss_benefits = None
        self.__vet_benefits = None

    ### ABOUT ME ###

    @property
    def user_id(self):
        if self.__user_id is None:
            header = self._span_template('AboutMeView', 'CP_V_ViewHeader_SiteManagerLabel')
            self.__user_id = header.split('#')[-1]
        return self.__user_id

    @property
    def photo(self):
        if self.__photo is None:
            self._ensure_screen('AboutMeView')
            soup = self.dc.make_soup()
            element = soup.find('span', dict(id='UploadedImage'))
            img_text = element.get('style') if element else ''
            self.__photo = self.dc.to_url(img_text.split("'")[1]) if img_text else ''
        return self.__photo

    @property
    def name(self):
        if self.__name is None:
            self._ensure_screen('AboutMeView')
            soup = self.dc.make_soup()

            # get prefix
            prefix_elem = soup.find('select', dict(id='CP_V_LegalPrefix'))
            if prefix_elem is not None:
                prefix_option = prefix_elem.find('option', dict(selected='selected'))
                prefix = prefix_option.text if prefix_option else ''
            else:
                prefix = ''

            # get first name
            fname_elem = soup.find('input', dict(id='CP_V_LegalFirstName'))
            fname = fname_elem.get('value') if fname_elem else ''

            # get middle name
            mname_elem = soup.find('input', dict(id='CP_V_LegalMiddleName'))
            mname = mname_elem.get('value') if mname_elem else ''

            # get last name
            lname_elem = soup.find('input', dict(id='CP_V_LegalLastName'))
            lname = lname_elem.get('value') if lname_elem else ''

            # get suffix
            suffix_elem = soup.find('select', dict(id='CP_V_LegalSuffix'))
            if suffix_elem is not None:
                suffix_option = suffix_elem.find('option', dict(selected='selected'))
                suffix = suffix_option.text if suffix_option else ''
            else:
                suffix = ''

            self.__name = {
                'prefix': prefix,
                'firstname': fname,
                'middlename': mname,
                'lastname': lname,
                'suffix': suffix}

        return self.__name

    @property
    def birthday(self):
        if self.__birthday is None:
            self.__birthday = self._span_template('AboutMeView', 'CP_V_StaticDateOfBirth')
        return self.__birthday

    @property
    def gender(self):
        if self.__gender is None:
            self.__gender = self._span_template('AboutMeView', 'CP_V_StaticGenderValue')
        return self.__gender

    @property
    def ethnicity(self):
        if self.__ethnicity is None:
            self.__ethnicity = self._span_template('AboutMeView', 'CP_V_StaticEthnicityValue')
        return self.__ethnicity

    @property
    def marital_status(self):
        if self.__marital_status is None:
            self.__marital_status = self._span_template('AboutMeView', 'CP_V_StaticMaritalStatus')
        return self.__marital_status

    ### CONTACT INFORMATION ###

    ### ACADEMIC INFORMATION ###

    @property
    def major(self):
        if self.__major is None:
            self.__major = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl00_InformationItemsRepeater_ctl00_Value')
        return self.__major

    @property
    def minor(self):
        if self.__minor is None:
            self.__minor = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl00_InformationItemsRepeater_ctl01_Value')
        return self.__minor

    @property
    def certification(self):
        if self.__certification is None:
            self.__certification = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl00_InformationItemsRepeater_ctl02_Value')
        return self.__certification

    @property
    def concentration(self):
        if self.__concentration is None:
            self.__concentration = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl00_InformationItemsRepeater_ctl03_Value')
        return self.__concentration

    @property
    def degree_honor(self):
        if self.__degree_honor is None:
            self.__degree_honor = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl00_InformationItemsRepeater_ctl04_Value')
        return self.__degree_honor

    @property
    def course_of_study(self):
        if self.__course_of_study is None:
            self.__course_of_study = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl01_InformationItemsRepeater_ctl00_Value')
        return self.__course_of_study

    @property
    def classification(self):
        if self.__classification is None:
            self.__classification = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl01_InformationItemsRepeater_ctl01_Value')
        return self.__classification

    @property
    def division(self):
        if self.__division is None:
            self.__division = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl01_InformationItemsRepeater_ctl02_Value')
        return self.__division

    @property
    def academic_status(self):
        if self.__academic_status is None:
            self.__academic_status = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl01_InformationItemsRepeater_ctl03_Value')
        return self.__academic_status

    @property
    def enrolled_date(self):
        if self.__enrolled_date is None:
            self.__enrolled_date = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl01_InformationItemsRepeater_ctl04_Value')
        return self.__enrolled_date

    @property
    def planned_graduation(self):
        if self.__planned_grad is None:
            self.__planned_grad = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl01_InformationItemsRepeater_ctl05_Value')
        return self.__planned_grad

    @property
    def max_credits(self):
        if self.__max_credits is None:
            value = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl01_InformationItemsRepeater_ctl06_Value')
            self.__max_credits = float(value) if value else 0.0
        return self.__max_credits

    @property
    def social_security_benefits(self):
        if self.__ss_benefits is None:
            self.__ss_benefits = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl02_InformationItemsRepeater_ctl00_Value')
        return self.__ss_benefits

    @property
    def veterans_benefits(self):
        if self.__vet_benefits is None:
            self.__vet_benefits = self._span_template('AcademicInformationView', 'CP_V_AcademicInformationCards_ctl00_AcademicInformationCard_InformationSetsRepeater_ctl02_InformationItemsRepeater_ctl01_Value')
        return self.__vet_benefits

    ## helper methods ##

    def _ensure_screen(self, screen):
        if self._screen != screen:
            self._screen = screen
            params = self._get_params(screen)
            self.dc.http_get(self.PROFILEURL, params=params)

    def _span_template(self, screen, elem_id):
        self._ensure_screen(screen)
        soup = self.dc.make_soup()
        element = soup.find('span', dict(id=elem_id))
        return element.text if element else ''

    @staticmethod
    def _get_params(screen):
        return {
            'tool': 'myProfileSettings',
            'screen': screen,
            'screenType': 'next'}


class AdvisingInformation:
    ADVISINGURL = 'https://my.gcc.edu/ICS/Advising/'

    def __init__(self, data_collection: DataCollection):
        self.dc = data_collection
        self.__is_advisor = None

    @property
    def is_advisor(self):
        if self.__is_advisor is None:
            self.dc.ensure_screen(self.ADVISINGURL)
            error = "The page you are requesting may require you to be " \
                    "logged in or you do not have permission to see it."
            self.__is_advisor = error not in self.dc.response.text
        return self.__is_advisor


class MyGcc:

    def __init__(self, username, password):
        self._dc = DataCollection(username, password)
        self._logged_in = False
        self.__profile = None
        self.__student = None
        self.__advising = None

    def login(self):
        dc = self._dc
        dc.http_get(dc.to_url('/ICS/'))
        soup = dc.make_soup()

        # check for invalid login
        error_elem = soup.find('div', dict(id='CP_V_Summary'))
        if error_elem is not None:
            raise Exception(error_elem.text.strip('"') or 'Invalid login')

        # check for not being logged in
        login_btn = soup.find('input', dict(id='siteNavBar_btnLogin'))
        if login_btn is not None:
            raise Exception('Invalid login')

        self._logged_in = True
        return True


    def logout(self):
        pass

    @property
    def profile(self):
        if self.__profile is None:
            self._ensure_login()
            self.__profile = ProfileInformation(self._dc)
        return self.__profile

    @property
    def advising(self):
        if self.__advising is None:
            self._ensure_login()
            self.__advising = AdvisingInformation(self._dc)
        return self.__advising

    def _ensure_login(self):
        if self._logged_in is False:
            self.login()
