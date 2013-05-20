from pprint import pprint
import smtplib, json, urllib2, time, socket

def internet_on():
    try:
        response1 = urllib2.urlopen('http://74.125.140.99', timeout = 1)
        return True
    except urllib2.URLError as err: pass
    return False

def sendGroupMail(msg, emails):
    gmail_user = 'thejohnklab@gmail.com'
    gmail_pwd = 'room3042'
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + ', '.join(emails) + '\n' + 'From: JK Lab <' + gmail_user + '>\n' + 'Subject:Group Meeting and Journal Club Reminder\n'
    msg = header + msg
    smtpserver.sendmail(gmail_user, emails, msg)
    smtpserver.close()

def genCurrentWeekMsg(gmName, jcName):
    msg = "Hi all,\n\nThis is a reminder that we "
    
    if gmName != 'No' and jcName != 'No':
        if gmName != jcName:
            msg = msg + "have %s for group meeting and %s for journal club starting at 12 PM on Thursday" % (gmName, jcName)
        else:
            msg = msg + "have %s for both group meeting and journal club starting at 12 PM on Thursday" % (gmName)
    elif gmName == 'No' and jcName == 'No':
        msg = msg + "don't have group meeting nor journal club"
    elif gmName == 'No':
        msg = msg + "have %s for journal club but no group meeting" % (jcName)
    elif jcName == 'No':
        msg = msg + "have %s for group meeting but no journal club" % (gmName)

    msg = msg + " this week.\n\n"
    return msg

def genNextWeekMsg(gmName, jcName):
    msg = 'Next time, '
    if gmName != 'No' and jcName != 'No':
        if gmName != jcName:
            msg = msg + "%s is up for group meeting and %s is up for journal club." % (gmName, jcName)
        else:
            msg = msg + "%s is up for both group meeting and journal club." % (gmName)
    elif gmName == 'No' and jcName == 'No':
        msg = msg + 'we have no group meeting nor journal club.'
    elif gmName == 'No':
        msg = msg + "%s is up for journal club but we have no group meeting." % (jcName)
    elif jcName == 'No':
        msg = msg + "%s is up for group meeting but we have no journal club." % (gmName)
    
    msg = msg + "\n\nThanks,\n\nThe JK Lab\n"
    return msg

def getNames(json_data):
    gmIndex = json_data['rotation']['current_index']['g']
    jcIndex = json_data['rotation']['current_index']['j']
    gmCName = json_data['rotation']['group_meeting'][gmIndex]
    jcCName = json_data['rotation']['journal_club'][jcIndex]

    gmIndex = json_data['rotation']['next_index']['g']
    jcIndex = json_data['rotation']['next_index']['j']
    gmNName = json_data['rotation']['group_meeting'][gmIndex]
    jcNName = json_data['rotation']['journal_club'][jcIndex]

    return gmCName, jcCName, gmNName, jcNName

def updateRotation(json_data):
    c_g_index = json_data['rotation']['current_index']['g']
    c_j_index = json_data['rotation']['current_index']['j']
    n_g_index = json_data['rotation']['next_index']['g']
    n_j_index = json_data['rotation']['next_index']['j']

    json_data['rotation']['current_index']['g'] = n_g_index
    json_data['rotation']['current_index']['j'] = n_j_index

    gm_total = len(json_data['rotation']['group_meeting']) - 1
    jc_total = len(json_data['rotation']['journal_club']) - 1
    
    if n_g_index == gm_total:
        n_g_index = (c_g_index + 1) % gm_total
    else:
        n_g_index = (n_g_index + 1) % gm_total
    json_data['rotation']['next_index']['g'] = n_g_index

    if n_j_index == jc_total:
        n_j_index = (c_j_index + 1) % jc_total
    else:
        n_j_index = (n_j_index + 1) % jc_total
    json_data['rotation']['next_index']['j'] = n_j_index
        
def main():
    #connected = False
    # wait for internet connection. Test 3 time, wait for 10 secs in between
    #file = open("/Users/yanxia/Desktop/log.txt", 'w')
    #for i in range(3):
    #    connected = internet_on()
    #    if connected: break
    #    file.write("internet: " + str(i) + '\n')
    #    time.sleep(10)
    #file.close()
    #if not connected: return

    fname = '/Users/yanxia/Google Drive/group_rotation.json'
    input = open(fname, 'r')
    json_data = json.load(input)
    input.close()

    gmCName, jcCName, gmNName, jcNName = getNames(json_data)
    
    msg = genCurrentWeekMsg(gmCName, jcCName)
    msg = msg + genNextWeekMsg(gmNName, jcNName)
    emails = json_data['rotation']['emails']
    #emails = ['drseanxy@mac.com']
    #emails = ['KARANICOLAS-LAB@listproc.cc.ku.edu']
    #emails = ['karanicolas-lab@ku.edu']
    
    sent = False
    for i in range(3):
        try: 
            sendGroupMail(msg, emails)
        except Exception as err:
            with open("/Users/yanxia/Desktop/log.txt", 'a') as logfile:
                logfile.write("try: " + str(i + 1) + '\n')
                logfile.write(err[1])
            time.sleep(5)
        else:
            sent = True
            break
    
    if not sent: return

    updateRotation(json_data)
    with open(fname, 'w') as outfile:
        json.dump(json_data, outfile, indent = 4, separators = [',', ": "], sort_keys = True)

if __name__ == '__main__' : main()
