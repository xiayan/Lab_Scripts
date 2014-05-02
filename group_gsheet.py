"""parse group meeting scheduling from google spreadsheet"""
import gspread
import datetime
import urllib2, smtplib
import json
import time
import argparse

def thu_date():
    """
    return year, month and date of the thusday this week
    t_mon is the date of monday this week
    t_thu is the date of thursday this week
    """
    # tdate = datetime.datetime.strptime('5/5/2014', '%m/%d/%Y')
    tdate = datetime.date.today()
    t_mon = tdate + datetime.timedelta(days = -tdate.weekday())
    t_thu = t_mon + datetime.timedelta(days = 3)
    return t_thu.year, t_thu.month, t_thu.day

def parse_date(d_string):
    """
    parse date string of format:
    'decimal_month_number/decimal_day_number/year_wo_century'
    such as '5/1/12', '11/2/13', '12/25/14'
    """
    sday = datetime.datetime.strptime(d_string, '%m/%d/%Y')
    return sday.month, sday.day

def internet_on(num_try):
    """test if there is internet connection"""
    for _ in range(num_try):
        try:
            urllib2.urlopen('http://www.google.com', timeout = 1)
            return True
        except urllib2.URLError:
            time.sleep(5)

    return False

def gen_curr_week_msg(g_name, j_name):
    """generate the message using this weeks name"""
    mtime = '1:00 PM'
    day   = 'Thursday'
    place = '8024 Haworth'

    msg = "Hi all,\n\nThis is a reminder that we "

    if g_name != None and j_name != None:
        msg = msg + "have %s for group meeting and %s for journal club" \
                " starting at %s on %s in %s" \
                % (g_name, j_name, mtime, day, place)
    elif g_name == None and j_name == None:
        msg = msg + "don't have group meeting nor journal club"
    elif g_name == None:
        msg = msg + "have %s for journal club but no group meeting starting" \
                " at %s on %s at %s" % (j_name, mtime, day, place)
    elif j_name == None:
        msg = msg + "have %s for group meeting but no journal club starting" \
                " at %s on %s at %s" % (g_name, mtime, day, place)

    msg = msg + " this week.\n\n"
    return msg

def gen_next_week_msg(n_date, g_name, j_name):
    """generate the message for next week"""
    msg = 'On ' + n_date + ', '
    if g_name != None and j_name != None:
        msg = msg + "%s is up for group meeting and %s is up for journal club."\
                % (g_name, j_name)
    elif g_name == None and j_name == None:
        msg = msg + 'we have no group meeting nor journal club.'
    elif g_name == None:
        msg = msg + "%s is up for journal club but we have no group meeting." \
                % (j_name)
    elif j_name == None:
        msg = msg + "%s is up for group meeting but we have no journal club." \
                % (g_name)

    msg = msg + "\n\nThis is an automated message. Please do not reply to" \
            " this email. If you have any comments or questions, please email" \
            " karanicolas-lab@ku.edu"

    msg = msg + "\n\nThanks,\n\nThe JK Lab\n"
    return msg

def send_group_mail(msg, emails):
    """
    send out group emails using JK-lab's account
    """
    gmail_user = 'thejohnklab@gmail.com'
    gmail_pwd = 'room3042'
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + ', '.join(emails) + '\n' + 'From: JK Lab <' + \
            gmail_user + '>\n' + \
            'Subject:Group Meeting and Journal Club Reminder\n'
    msg = header + msg
    smtpserver.sendmail(gmail_user, emails, msg)
    smtpserver.close()

def main():
    """main function"""

    # test if has internet connection
    if not internet_on(3):
        with open("/Users/yanxia/Desktop/log.txt", 'a') as logfile:
            logfile.write("No interent connection" + '\n')
        return

    parser = argparse.ArgumentParser("description: Fetch information from lab "\
            "gmail spreadsheet and send out group email")
    parser.add_argument('-t', '--test', dest='testing', \
            help='choose to use testing emails or group emails', \
            type=int, default=1)
    parser.add_argument('-p', '--print', dest='printing', \
            help='choose to print message only or send email', \
            type=int, default=1)
    args = parser.parse_args()
    use_test   =  bool(args.testing)
    print_only =  bool(args.printing)

    gsheet_key = '0AvJ5v54JQEcldDV0Z1BVSXV2QURERThEYjMyWW9rb3c'
    usr        = 'thejohnklab@gmail.com'
    pwd        = 'room3042'
    glogin     = gspread.login(usr, pwd)
    gsheets    = glogin.open_by_key(gsheet_key)

    thu_year, thu_month, thu_day = thu_date()
    worksheet  = gsheets.worksheet(str(thu_year))

    value_list = worksheet.col_values(1)
    for i in range(1, len(value_list)):
        s_month, s_day = parse_date(value_list[i])
        if s_month == thu_month and s_day == thu_day:
            c_idx = str(i+1)
            n_idx = str(i+2)
            cg_name = worksheet.acell('B'+c_idx).value
            cj_name = worksheet.acell('C'+c_idx).value
            ng_name = worksheet.acell('B'+n_idx).value
            nj_name = worksheet.acell('C'+n_idx).value
            nw_date = datetime.datetime.strptime(value_list[i+1], '%m/%d/%Y')
            break

    curr_msg = gen_curr_week_msg(cg_name, cj_name)
    next_msg = gen_next_week_msg(nw_date.strftime('%b %d'), ng_name, nj_name)

    # Get email list from the json file
    f_input = open('/Users/yanxia/Google Drive/lab_emails.json', 'r')
    json_data = json.load(f_input)
    f_input.close()
    if use_test:
        emails = json_data['test_emails']
    else:
        emails = json_data['emails']

    if print_only:
        print cg_name, cj_name
        print ng_name, nj_name
        print nw_date.strftime('%b %d'), '\n'
        print curr_msg + next_msg
        print emails
        return
    else:
        # print "sending email to\n"
        # print emails
        send_group_mail(curr_msg+next_msg, emails)

main()

