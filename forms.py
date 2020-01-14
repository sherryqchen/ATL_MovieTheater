from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectMultipleField, SelectField, \
    DecimalField, RadioField
from wtforms import IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired, NumberRange, ValidationError, Optional
from wtforms.fields.html5 import DateField


class UserRegistrationForm(FlaskForm):
    firstname = StringField('First Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    submit2 = SubmitField('Back')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    # submit2 = SubmitField('Register')


class UserVisitHistoryForm(FlaskForm):
    company_name = SelectField(label="Company Name", validators=[InputRequired()])
    start_date = DateField(label="Start Date", validators=[Optional()])
    end_date = DateField(label="End Date", validators=[Optional()])
    filter = SubmitField(label="Filter")
    back = SubmitField(label="Back")


class CustomerRegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    submit2 = SubmitField('Back')


class ManagerRegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    streetaddress = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired(), Length(min=1, max=20)])
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=5)])
    STATE_ABBREV = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                    'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD',
                    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    state_pairs = STATE_ABBREV
    state = SelectField('State', choices=[(state, state) for state in STATE_ABBREV])

    company = SelectField('Company')
    submit = SubmitField('Register')
    submit2 = SubmitField('Back')


class ManagerCustomerRegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    streetaddress = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired(), Length(min=1, max=20)])
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=5)])
    STATE_ABBREV = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                    'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD',
                    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

    state_pairs = STATE_ABBREV
    state = SelectField('State', choices=[(state, state) for state in STATE_ABBREV])

    company = SelectField('Company')
    submit = SubmitField('Register')
    submit2 = SubmitField('Back')


class AdminCreateMovieForm(FlaskForm):
    movie_name = StringField('Name', validators=[DataRequired()])
    duration = IntegerField('Duration', validators=[InputRequired(), NumberRange(min=0)])
    release_date = DateField('Release Date', validators=[InputRequired()])
    create = SubmitField('Create')


class AdminCreateTheaterForm(FlaskForm):
    theater_name = StringField('Theater Name', validators=[DataRequired()])
    company_name = SelectField('Company Name', id='Company Name', validators=[InputRequired()], choices=[])
    manager = SelectField('Manager', id='Manager', validators=[InputRequired()], choices=[])
    street_addr = StringField('Street Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    STATE_ABBREV = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                    'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD',
                    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    state = SelectField('State', choices=[(state, state) for state in STATE_ABBREV])
    zipcode = StringField('Zipcode', validators=[DataRequired(), Length(min=5, max=5)])
    capacity = IntegerField('Capacity', validators=[DataRequired(), NumberRange(min=1)])
    create = SubmitField('Create')


class ManagerTheaterOverviewForm(FlaskForm):
    movie_name_include = StringField('Movie Name (Include)')
    min_duration = IntegerField('Movie Duration From', validators=[Optional()])
    max_duration = IntegerField('To', validators=[Optional()])
    min_release_date = DateField('Movie Release Date From', validators=[Optional()])
    max_release_date = DateField('To', validators=[Optional()])
    min_play_date = DateField('Movie Play Date From', validators=[Optional()])
    max_play_date = DateField('To', validators=[Optional()])
    checkbox = BooleanField('Only Include Not Played Movies')
    filter = SubmitField('Filter')


class UserExploreTheaterForm(FlaskForm):
    company_name = SelectField(label="Company Name", validators=[InputRequired()])
    theater_name = SelectField(label="Theater Name", validators=[InputRequired()])
    STATE_ABBREV = ['', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                    'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD',
                    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    state_pairs = STATE_ABBREV
    state = SelectField('State', choices=[(state, state) for state in STATE_ABBREV])
    city = StringField(label="City", validators=[Length(min=0, max=20)])
    filter = SubmitField(label="Filter")
    log_visit = SubmitField('Log Visit')
    visit_date = DateField('Visit Date', validators=[InputRequired()])
    submit = SubmitField('Back')
    test = RadioField('', choices=[('value', '')])


class ScheduleMovieForm(FlaskForm):
    name = SelectField(label="Name", validators=[InputRequired()], id="movie_name")
    release_date = SelectField(label="Release Date", validators=[InputRequired()], id="date")
    play_date = DateField('Play Date', validators=[InputRequired()])
    back = SubmitField('Back')
    add = SubmitField('Add')


class CustomerRegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # creditcardNumber = StringField('Credit Card Number', id="cd", validators=[Length(min=3, max=16)])
    creditcardNumber1 = IntegerField('Credit Card Number 1', id="cd1", validators=[InputRequired()])
    creditcardNumber2 = StringField('Credit Card Number 2', id="cd2")
    creditcardNumber3 = StringField('Credit Card Number 3', id="cd3")
    creditcardNumber4 = StringField('Credit Card Number 4', id="cd4")
    creditcardNumber5 = StringField('Credit Card Number 5', id="cd5")

    add = SubmitField("add")
    submit = SubmitField('Register')
    submit2 = SubmitField('Back')


class CustomerExploreMovieForm(FlaskForm):
    company_name = SelectField(label="Company Name", validators=[InputRequired()])
    movie_name = SelectField(label="Movie Name", validators=[InputRequired()])
    card_number = SelectField(label="Card Number", validators=[InputRequired()])
    city = StringField(label="City", validators=[Length(min=0, max=20)])
    STATE_ABBREV = ['ALL', 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                    'HI', 'ID', 'IL', 'IN', 'IO', 'KS', 'KY', 'LA', 'ME', 'MD',
                    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']
    state_pairs = STATE_ABBREV
    state = SelectField('State', choices=[(state, state) for state in STATE_ABBREV])
    movie_play_date_start = DateField('Play Date Start')
    movie_play_date_end = DateField('Play Date End')
    filter = SubmitField(label="Filter")
    view = SubmitField('View')


class AdminManageUserForm(FlaskForm):
    username = StringField(label="User Name", validators=[Length(min=1)])
    STATUS = ['ALL', 'Pending', 'Declined', 'Approved']
    status = STATUS
    status = SelectField('Status', choices=[(status, status) for status in STATUS])

    # SORTBY = ['username', 'creditCardCount', 'user', 'Status']
    # sortBy= SelectField('Sort by', choices=[(item, item) for item in SORTBY])

    # DIRECTION = ['ASC', 'DESC']
    # sortDirection = SelectField('Sort Direction', choices=[(item, item) for item in DIRECTION])

    sortBy = StringField(label="Sort By", validators=[DataRequired(), Length(min=1)])
    sortDirection = StringField(label="Sort Direction", validators=[DataRequired(), Length(min=1)])
    filter = SubmitField(label="Filter")
    submit = SubmitField(label='back')


class AdminManageCompanyForm(FlaskForm):
    companyName = SelectField(label="Company Name", validators=[InputRequired()])
    cityNumberFrom = StringField(label="# City Covered (From)")
    cityNumberTo = StringField(label="# City Covered (To)")
    TheatersNumberFrom = StringField(label="# Theaters Number (From)")
    TheatersNumberTo = StringField(label="# Theaters Number (To)")
    EmployeeNumberFrom = StringField(label="# Employees Number (From)")
    EmployeeNumberTo = StringField(label="# Employees Number (To)")

    sortBy = StringField(label="Sort By", validators=[DataRequired(), Length(min=1)])
    sortDirection = StringField(label="Sort Direction", validators=[DataRequired(), Length(min=1)])

    filter = SubmitField(label="Filter")
    createTheater = SubmitField('Create Theater')
    Detail = SubmitField('Detail')
    submit = SubmitField('Back')
