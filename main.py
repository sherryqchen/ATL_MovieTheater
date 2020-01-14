from flask import Flask, render_template, url_for, flash, redirect, request, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User
from .forms import *
from app import app, mysql
from hashlib import md5
from .util import db_query, checkQuote


def redirect_login_user(user):
    """
    Redirect the already logged in user to the functionality page.
    :param user: user
    :return: object corresponding to the redirected page
    """
    if user.usertype == "Customer":
        return redirect(url_for('customer_functionality'))
    elif user.usertype == "Manager":
        return redirect(url_for('manager_only_functionality'))
    elif user.usertype == "Admin":
        return redirect(url_for('admin_only_functionality'))
    elif user.usertype == "CustomerAdmin":
        return redirect(url_for('admin_customer_functionality'))
    elif user.usertype == "CustomerManager":
        return redirect(url_for('manager_customer_functionality'))
    else:  # User
        return redirect(url_for('user_functionality'))


@app.route("/")
@app.route("/index")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register_options")
def register_options():
    return render_template('nav-register.html', title='Register Options')

@app.route("/user_register", methods=['GET', 'POST'])
def user_register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        result, error = db_query("call user_register(%s, %s, %s, %s);",
                                 (form.username.data, form.password.data, form.firstname.data, form.lastname.data))
        if error:
            flash("Duplicate username: " + error, 'danger')
        # flash(f'Account created for {form.username.data}!','success')
        else:
            flash("Account created for {}! Wait for an administrator to approve your registration.".format(
                form.username.data), 'success')
            # flash('You have registered successfully. Please wait for the admin to approve your registration.')
            return redirect(url_for('login'))
    return render_template('user-register.html', title='Register', form=form)


@app.route("/customer_register", methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegistrationForm()
    # if form.validate_on_submit():
    #     print(form.username.data)
    if request.method == 'POST':
        print(form.username.data)
        if len(form.password.data) < 8:
            flash("Please enter password with at least 8 characters",'danger')
            return redirect(url_for('customer_register'))
        data = request.form.get("input")
        # check if it has credit cards
        if len(data) == 0:
            flash('Must have at least one credit card!', 'danger')
            return redirect(url_for('customer_register'))
        print(data)
        # split string into array
        datas = data.split(",")
        datas.pop()
        # check credit card data type
        for i in datas:
            if not i.isdigit():
                flash("Input must be numbers!", 'danger')
                return redirect(url_for('customer_register'))
        result1, error1 = db_query("call customer_only_register(%s, %s, %s, %s);",
                                   (form.username.data, form.password.data, form.firstname.data, form.firstname.data))
        if error1:
            flash("Duplicate username :" + error1, 'danger')
            return redirect(url_for('customer_register'))
        for i in datas:
            result2, error2 = db_query("call customer_add_creditcard(%s, %s);",
                                       (form.username.data, i))
            if error2:
                flash('Duplicate credit card:' + i, 'danger')
                db_query("delete from user where Username = '{}';".format(form.username.data), None)
                return redirect(url_for('customer_register'))
        flash("Account created for {}! Wait for an administrator to approve your registration.".format(
            form.username.data), 'success')
        return redirect(url_for('login'))
    return render_template('customer-register.html', title='Register', form=form)

@app.route("/manager_register", methods=['GET', 'POST'])
def manager_register():
    form = ManagerRegistrationForm()
    result, error = db_query('select CompanyName from company', None)
    form.company.choices = [(cname[0], cname[0]) for cname in result]
    if form.validate_on_submit():
        result, error = db_query("call manager_only_register(%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                                 (form.username.data, form.password.data, form.firstname.data,
                                  form.lastname.data, form.company.data, form.streetaddress.data,
                                  form.city.data, form.state.data, form.zipcode.data))
        if error:
            flash(error, 'danger')
        # flash(f'Account created for {form.username.data}!','success')
        else:
            flash("Account created for {}! Wait for an administrator to approve your registration.".format(
                form.username.data), 'success')
            # flash('You have registered successfully. Please wait for the admin to approve your registration.')
            return redirect(url_for('login'))
    return render_template('manager-register.html', title='Register', form=form)


@app.route("/manager_customer_register", methods=['GET', 'POST'])
def manager_customer_register():
    form = ManagerCustomerRegistrationForm()
    result, error = db_query('select CompanyName from company', None)
    form.company.choices = [(cname[0], cname[0]) for cname in result]
    if form.validate_on_submit():
        data = request.form.get("input")
        # check if it has credit cards
        if len(data) == 0:
            flash('Must have at least one credit card!', 'danger')
            return redirect(url_for('manager_customer_register'))
        # split string into array
        datas = data.split(",")
        datas.pop()
        # check credit card data type
        for i in datas:
            if not i.isdigit():
                flash("Input must be numbers!", 'danger')
                return redirect(url_for('manager_customer_register'))
        if(len(form.zipcode.data)) is not 5:
            flash("Please enter 5 digits for zipcode", 'danger')
            return redirect(url_for('manager_customer_register'))
        result1, error1 = db_query("call manager_customer_register(%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                                   (form.username.data, form.password.data, form.firstname.data,
                                    form.lastname.data, form.company.data, form.streetaddress.data,
                                    form.city.data, form.state.data, form.zipcode.data))
        if error1:
            flash(error1, 'danger')
            return redirect(url_for('manager_customer_register'))

        for i in datas:
            result2, error2 = db_query("call manager_customer_add_creditcard(%s, %s);",
                                       (form.username.data, i))
            if error2:
                flash(error2, 'danger')
                db_query("delete from user where Username = '{}';".format(form.username.data), None)
                return redirect(url_for('manager_customer_register'))
        flash("Account created for {}! Wait for an administrator to approve your registration.".format(
            form.username.data), 'success')
        return redirect(url_for('login'))
    return render_template('manager-customer-registration.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_login_user(current_user)
    form = LoginForm()
    if form.validate_on_submit():
        # create cursor
        cur = mysql.connection.cursor()
        # get hashed input password
        md = md5()
        md.update("{}".format(form.password.data).encode())
        hashed_input_pass = md.hexdigest()
        # get password by username from db
        result = cur.execute("SELECT Password FROM user where Username = '{}';".format(form.username.data))
        # if success execution success
        if result > 0:
            if cur.fetchall()[0][0] == hashed_input_pass:
                cur.execute("select Status from user where Username = '{}';".format(form.username.data))
                status = cur.fetchall()[0][0]
                if status == "Pending":
                    flash("Your registration has not been approved. Please wait for an administrator to approve your "
                          "request or contact support if needed.", category="warning")
                elif status == "Declined":
                    flash("Your registration has been declined. Please contact administrator for support.",
                          category="error")
                else:
                    user = User.get(form.username.data)
                    # user = User.get(form.username.data)
                    login_user(user)
                    flash('You have logged in!', 'success')
                    return redirect_login_user(user)
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        else:  # if username not in the db
            flash('NO USER', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/user_visit_history", methods=['GET', 'POST'])
@login_required
def user_visit_history():
    form = UserVisitHistoryForm()
    cur = mysql.connection.cursor()
    cur.execute("select CompanyName from Company")
    company_list = [('ALL', 'ALL')]
    for cname in cur.fetchall():
        company_list.append((cname[0], cname[0]))
    # form.company_name.choices = [(cname[0], cname[0]) for cname in cur.fetchall()]
    form.company_name.choices = company_list
    data_details = None
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        db_query("call user_filter_visitHistory(%s, %s, %s)",
                 (current_user.username, start_date, end_date))
        data_details, error = db_query(
            "SELECT * FROM UserVisitHistory where ComName = '{}' or '{}' = 'ALL';"
                .format(form.company_name.data, form.company_name.data), None)
    return render_template("user-visit-history.html", title='Visit History', form=form, data_details=data_details)


@app.route("/user_functionality", methods=['GET', 'POST'])
@login_required
def user_functionality():
    if current_user.usertype == 'User':
        return render_template('user-functionality.html', title='User Functionality')
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/customer_functionality", methods=['GET', 'POST'])
@login_required
def customer_functionality():
    if current_user.usertype == 'Customer':
        return render_template('customer-functionality.html', title='Customer Functionality')
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/manager_only_functionality", methods=['GET', 'POST'])
@login_required
def manager_only_functionality():
    if current_user.usertype == 'Manager':
        return render_template('manager-only-functionality.html', title='Manager Only Functionality')
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/manager_customer_functionality", methods=['GET', 'POST'])
@login_required
def manager_customer_functionality():
    if current_user.usertype == 'CustomerManager':
        return render_template('manager-customer-functionality.html', title='Manager Customer Functionality')
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/admin_only_functionality", methods=['GET', 'POST'])
@login_required
def admin_only_functionality():
    if current_user.usertype == 'Admin':
        return render_template('admin-only-functionality.html', title='Admin Only Functionality')
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/admin_customer_functionality", methods=['GET', 'POST'])
@login_required
def admin_customer_functionality():
    if current_user.usertype == 'CustomerAdmin':
        return render_template('admin-customer-functionality.html', title='Admin Customer Functionality')
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/admin_create_movie", methods=['GET', 'POST'])
@login_required
def admin_create_movie():
    if current_user.usertype == 'Admin' or current_user.usertype == 'CustomerAdmin':
        form = AdminCreateMovieForm()
        if form.validate_on_submit():
            result, error = db_query('call admin_create_movie(%s, %s, %s);',
                                     (form.movie_name.data, form.duration.data, form.release_date.data))
            print(error)
            if error:
                flash('Movie already exists.', 'danger')
            else:
                flash('Movie successfully created.', 'success')
        return render_template('admin-create-movie.html', title='Create Movie', form=form)
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/admin_create_theater", methods=['GET', 'POST'])
@login_required
def admin_create_theater():
    if current_user.usertype == 'Admin' or current_user.usertype == 'CustomerAdmin':
        form = AdminCreateTheaterForm()
        result, error = db_query('select CompanyName from company', None)
        comList = [('', '')]
        for cname in result:
            comList.append((cname[0], cname[0]))
        form.company_name.choices = comList
        result, error = db_query('select Username from manager', None)
        # print(result)
        form.manager.choices = [(mname[0], mname[0]) for mname in result]
        # print(form.manager.choices)
        if form.validate_on_submit():
            result, error = db_query('call admin_create_theater(%s, %s, %s, %s, %s, %s, %s, %s)',
                                     (form.theater_name.data, form.company_name.data,
                                      form.street_addr.data, form.city.data, form.state.data,
                                      form.zipcode.data, form.capacity.data, form.manager.data))
            if error:
                # print(error)
                flash('DB error: ' + error, 'danger')
            else:
                # print('success')
                flash('Successfully create theater {}.'.format(form.theater_name.data), 'success')
        return render_template('admin-create-theater.html', title='Create Theater', form=form)
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/manager_not_manage_theater/<company>")
@login_required
def manager(company):
    managers, error = db_query("select Username from manager where Works_In = '{}' and Username not in "
                               "(select Manager from theater where CompanyName = '{}')".format(company, company), None)
    manager_array = []
    for manager in managers:
        managerObj = {'id': manager[0], 'name': manager[0]}
        manager_array.append(managerObj)

    return jsonify({'managers': manager_array})


@app.route("/manager_theater_overview", methods=['GET', 'POST'])
@login_required
def manager_theater_overview():
    if current_user.usertype == 'Manager' or current_user.usertype == 'CustomerManager':
        form = ManagerTheaterOverviewForm()
        data_details = None
        if form.validate_on_submit():
            min_release_date = form.min_release_date.data
            max_release_date = form.max_release_date.data
            min_play_date = form.min_play_date.data
            max_play_date = form.max_play_date.data
            result, error = db_query("call manager_filter_th(%s,%s,%s,%s,%s,%s,%s,%s,{})".format(form.checkbox.data),
                                     (current_user.username, checkQuote(form.movie_name_include.data),
                                      form.min_duration.data, form.max_duration.data,
                                      min_release_date, max_release_date, min_play_date,
                                      max_play_date))
            if error:
                flash('Error: ' + error, 'danger')
            else:
                data_details, error = db_query('select * from manfilterth', None)
                # print(data_details)
        return render_template('manager-theater-overview.html', title='Manager Theater Overview', form=form,
                               data_details=data_details)

    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/manager_schedule_movie", methods=['GET', 'POST'])
@login_required
def manager_schedule_movie():
    form = ScheduleMovieForm()
    if current_user.usertype == 'Manager' or current_user.usertype == 'CustomerManager':
        movieListResult, error = db_query("select distinct MovieName from movie", None)
        movList = [('', '')]
        for cname in movieListResult:
            movList.append((cname[0], cname[0]))
        form.name.choices = movList
        dateListResult, error = db_query("select ReleaseDate from movie", None)
        dateList = [('', '')]
        for cname in dateListResult:
            dateList.append((str(cname[0]), str(cname[0])))
        form.release_date.choices = dateList
        if form.validate_on_submit():
            result_schedule_movie, error = db_query("call manager_schedule_mov(%s, %s, %s, %s);",
                                                    (current_user.username, form.name.data, form.release_date.data,
                                                     form.play_date.data))
            if error:
                flash('Error: ' + error, 'danger')
            else:
                flash('Movie {} has been scheduled.'.format(form.name.data), 'success')
        return render_template('manager-schedule-movie.html', title='Schedule Movie', form=form)
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/manager_schedule_movie_release_date/<name>")
def manager_schedule_movie_release_date(name):
    dates, error = db_query("select ReleaseDate from movie where MovieName = '{}'".format(checkQuote(name)), None)
    dates_array = []
    for date in dates:
        dateObj = {}
        dateObj['id'] = str(date[0])
        dateObj['name'] = str(date[0])
        dates_array.append(dateObj)
    return jsonify({'dates': dates_array})


@app.route("/user_explore_theater", methods=['GET', 'POST'])
@login_required
def user_explore_theater():
    form = UserExploreTheaterForm()
    # extract all company name
    compListResult, error = db_query("select CompanyName from Company", None)
    compList = [('ALL', 'ALL')]
    for cname in compListResult:
        compList.append((cname[0], cname[0]))
    form.company_name.choices = compList
    # extract all theater name
    thListResult, error = db_query("select TheaterName from theater", None)
    thList = [('ALL', 'ALL')]
    for cname in thListResult:
        thList.append((cname[0], cname[0]))
    form.theater_name.choices = thList
    data_details = None
    resultLength = 0
    filteredListResult = None
    if form.filter.data:
        result, error = db_query("call user_filter_th(%s, %s, %s, %s);",
                                 (form.theater_name.data, form.company_name.data, form.city.data, form.state.data))
        filteredListResult, error = db_query("select * from UserFilterTh", None)
        if len(filteredListResult) > 0:
            data_details = filteredListResult
            resultLength = len(data_details)
    if request.method == 'POST' and request.form.get('table_index') != None:
        info = request.form.get('table_index')
        info_arr = info.split('$$$')
        logVisitResult, logVisitError = db_query("call user_visit_th(%s, %s, %s, %s);",
                                                 (
                                                 info_arr[0], info_arr[1], form.visit_date.data, current_user.username))
    return render_template("user-explore-theater.html", title='Explore Theater', form=form, data_details=data_details,
                           resultLength=resultLength)


@app.route("/customer_explore_movie", methods=['GET', 'POST'])
@login_required
def customer_explore_movie():
    if current_user.usertype == 'CustomerAdmin' or current_user.usertype == 'CustomerManager' or current_user.usertype == 'Customer':
        form = CustomerExploreMovieForm()
        compListResult, error = db_query("select CompanyName from Company", None)  # extract all company name
        compList = []
        compList.append(('ALL', 'ALL'))
        for cname in compListResult:
            compList.append((cname[0], cname[0]))
        form.company_name.choices = compList

        movieListResult, error = db_query("select MovieName from movie", None)  # extract all movie name
        movieList = []
        movieList.append(('ALL', 'ALL'))
        for cname in movieListResult:
            movieList.append((cname[0], cname[0]))
        form.movie_name.choices = movieList

        cardListResult, error = db_query(
            "select CreditCardNum from credit_card where Owner = '{}';".format(current_user.username), None)
        cardList = []
        for cname in cardListResult:
            cardList.append((cname[0], cname[0]))
        form.card_number.choices = cardList

        data_details = None
        resultLength = 0
        filteredListResult = None
        if form.filter.data:
            result, error = db_query("call customer_filer_mov(%s, %s, %s, %s, %s, %s);",
                                     (form.movie_name.data, form.company_name.data, form.city.data, form.state.data,
                                      form.movie_play_date_start.data, form.movie_play_date_end.data))
            filteredListResult, error = db_query("select * from CosFilterMovie", None)
            if len(filteredListResult) > 0:
                data_details = filteredListResult
                resultLength = len(data_details)

        if request.method == 'POST' and request.form.get('table_index') != None:
            info = request.form.get('table_index')
            info_arr = info.split('$$$')
            instruction = "select movReleaseDate, movPlayDate from CosFilterMovie where movName = '{}' and thName = '{}' and comName = '{}';".format(
                checkQuote(info_arr[0]), checkQuote(info_arr[1]), checkQuote(info_arr[2]))
            viewListResult, error = db_query(instruction, None)
            movReleaseDate = viewListResult[0][0]
            movPlayDate = viewListResult[0][1]
            cusViewMovResult, cusViewMovError = db_query("call customer_view_mov(%s, %s, %s, %s, %s, %s);",
                                                         (form.card_number.data, info_arr[0], movReleaseDate,
                                                          info_arr[1], info_arr[2], movPlayDate))
            print(form.card_number.data, info_arr[0], movReleaseDate, info_arr[1], info_arr[2], movPlayDate)
            if cusViewMovError:
                flash(cusViewMovError, 'danger')

        return render_template("customer-explore-movie.html", title='Explore Theater', form=form,
                               data_details=data_details, resultLength=resultLength)
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/company_detail", methods=['POST'])
@login_required
def company_detail():
    if current_user.usertype == 'Admin' or current_user.usertype == 'CustomerAdmin':
        company_name = request.form.get('company_name')
        db_query("call admin_view_comDetail_emp('{}');".format(company_name), None)
        db_query("call admin_view_comDetail_th('{}');".format(company_name), None)
        emplyee_names, error = db_query("SELECT * FROM adcomdetailemp;", None)
        theaters, error = db_query("SELECT * FROM adcomdetailth;", None)
        return render_template('company-detail.html', company_name=company_name, employee_names=emplyee_names,
                               theaters=theaters)
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/customer_view_history", methods=['GET', 'POST'])
@login_required
def customer_view_history():
    if current_user.usertype == 'CustomerAdmin' or current_user.usertype == 'CustomerManager' or current_user.usertype == 'Customer':
        db_query("call customer_view_history('{}')".format(current_user.username), None)
        table, error = db_query('select * from CosViewHistory', None)
        return render_template("customer-view-history.html", table=table)
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/admin_manage_user", methods=['GET', 'POST'])
@login_required
def admin_manage_user():
    if current_user.usertype == 'Admin' or current_user.usertype == 'CustomerAdmin':
        form = AdminManageUserForm()
        data_details = None
        resultLength = 0
        if form.filter.data:
            filteredResult, error = db_query("call phase4_admin_filter_user(%s, %s);", (form.username.data, 'ALL'))
            print(filteredResult)
            if form.status.data == 'ALL':
                if form.username.data == '':
                    filteredListResult, error = db_query("select * from phase4_largeTable", None)
                else:
                    filteredListResult, error = db_query(
                        "select * from phase4_largeTable where username = '{}';".format(form.username.data), None)
            else:
                if form.username.data == '':
                    filteredListResult, error = db_query(
                        "select * from phase4_largeTable where status = '{}';".format(form.status.data), None)
                else:
                    filteredListResult, error = db_query(
                        "select * from phase4_largeTable where status = '{}' and username = '{}';".format(
                            form.status.data, form.username.data), None)

            print(filteredListResult)
            if form.filter.data:
                if len(filteredListResult) > 0:
                    data_details = filteredListResult
                    resultLength = len(data_details)
        if request.method == 'POST' and request.form.get('table_index') is not None:
            username = request.form.get('table_index')
            if request.form.get('approve') is not None:
                db_query("call admin_approve_user('{}')".format(username), None)
            elif request.form.get('decline') is not None:
                declineResult, declineError = db_query("call admin_decline_user('{}')".format(username), None)
                if declineError:
                    flash(declineError, 'danger')
        return render_template('manage-user.html', title='Manage User', form=form, data_details=data_details,
                               resultLength=resultLength)
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)


@app.route("/admin_manage_company", methods=['GET', 'POST'])
@login_required
def admin_manage_company():
    if current_user.usertype == 'Admin' or current_user.usertype == 'CustomerAdmin':
        form = AdminManageCompanyForm()
        # extract all company name
        compListResult, error = db_query("select CompanyName from Company", None)
        compList = []
        compList.append(('ALL', 'ALL'))
        for cname in compListResult:
            compList.append((cname[0], cname[0]))
        form.companyName.choices = compList
        data_details = None
        resultLength = 0
        if form.filter.data:
            result, error = db_query("call admin_filter_company(%s, %s, %s, %s, %s, %s, %s, %s, %s);",
                                     (form.companyName.data, form.cityNumberFrom.data, form.cityNumberTo.data,
                                      form.TheatersNumberFrom.data, form.TheatersNumberTo.data,
                                      form.EmployeeNumberFrom.data,
                                      form.EmployeeNumberTo.data, form.sortBy.data, form.sortDirection.data))

            filteredListResult, error = db_query("select * from AdFilterCom", None)
            if len(filteredListResult) > 0:
                data_details = filteredListResult
                resultLength = len(data_details)
        return render_template('manage-company.html', title='Manage Company', form=form, data_details=data_details,
                               resultLength=resultLength)
    else:
        flash('Identity error. You cannot access to this page.', 'danger')
        return redirect_login_user(current_user)
