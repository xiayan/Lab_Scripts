#!/usr/bin/env python

import time, datetime, re, urllib2

month = {'january': 1, 'feburary': 2, 'march': 3, \
        'april': 4, 'may': 5, 'june': 6, 'july': 7, \
        'august': 8, 'september': 9, 'october': 10, \
        'november': 11, 'december': 12}

week = {'monday': 1, 'tuesday': 2, 'wednesday': 3, \
        'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7}

#prog = re.compile('>([^<]\s*\w.*[^>])<')
prog = re.compile('>([^<].*\w.*[^>])<')

def getTable(s, start):
    startIndex = s.find('<table>', start)
    endIndex   = s.find('</table>', startIndex)
    return startIndex, endIndex

def getCaption(s):
    startIndex = s.find('<caption>')
    endIndex   = s.find('</caption>', startIndex)
    return s[startIndex : endIndex + len('</caption>')]

def getEntry(s, start):
    startIndex = s.find('<tr>', start)
    endIndex   = s.find('</tr>', startIndex)
    return startIndex, endIndex

def getTd(s, start):
    startIndex = s.find('<td', start)
    endIndex   = s.find('</td>', startIndex)
    return startIndex, endIndex

def getMessage(s, today):
    count = s.count('<td')
    if count == 1:
        b, e = getTd(s, 0)
        info = s[b:e + len('<td')]
        #print info

        dtCount = info.count('<dt')

        start, end = 0, 0
        for i in range(dtCount):
            start = info.find('<dt', start)
            end   = info.find('</dt>', start)
            localInfo = info[start:end+len('</dt>')]
            # print localInfo
            start = end

            m = prog.search(localInfo)
            if m == None: return -1, -1, None
            message = m.group(1).split()
            for i in range(len(message)):
                word = message[i]
                if word.lower() in month.keys() and i != len(message)-1:
                    localDay = month[word.lower()] * 100 + eval(message[i+1])
                    if localDay == today:
                        return -1, month[word.lower()] * 100 + eval(message[i+1]), \
                                m.group(1)
        return -1, -1, None

    if count == 2:
        b1, e1 = getTd(s, 0)
        info1 = s[b1:e1 + len('<td>')]

        b2, e2 = getTd(s, e1)
        message = s[b2:e2 + len('<td>')]

        m1 = prog.search(info1)
        m2 = prog.search(message)
        if m1 == None or m2 == None:
            print "Here"
            print info1
            print message
            return -1, -1, None

        info1 = m1.group(1)
        message = m2.group(1)

        dates = info1.split('-')
        if len(dates) == 1:
            if dates[0].lower().strip() not in week.keys():
                print "funny weekday, check website"
                print dates[0]
                return -1, -1, None
            d = week[dates[0].lower().strip()]
            return d, d, message
        elif len(dates) == 2:
            d1, d2 = dates[0].lower().strip(), dates[1].lower().strip()
            if d1 not in week.keys() or d2 not in week.keys():
                print "funny weekdays, check website"
                print info1
                return -1, -1, None
            return week[d1], week[d2], message

    return -1, -1, None


def main():
    time_struct = time.localtime(time.time())
    today = time_struct.tm_mon * 100 + time_struct.tm_mday
    date  = time_struct.tm_wday + 1
    #print time_struct
    #print date
    #today = 517
    #date = 5

    infile = urllib2.urlopen('http://www.recreation.ku.edu/~recserv/hours.shtml')
    #inp = open('sample.html', 'r')
    info = '\n'.join(infile.readlines())

    start = info.find('<h2>Ambler')
    end   = info.find('<h2>', start + 5)

    info = info[start:end]

    #prog = re.compile('(>)(.+)(<)')
    s, e = 0, 0
    while s != -1 and e != -1:
        s, e = getTable(info, s);
        block = info[s:e + len('</table>')]
        s = e
        caption = getCaption(block)
        m = prog.search(caption)
        if m == None: continue

        dateInfo = m.group(1).split()
        beginning, ending = 0, 0
        for i in range(len(dateInfo)):
            if dateInfo[i].lower() in month.keys():
                beginning = month[dateInfo[i].lower()] * 100 + eval(dateInfo[i+1])
                if (dateInfo[i+2] != '-' or\
                    dateInfo[i+3].lower() not in month.keys()):
                    ending = beginning
                else:
                    ending = month[dateInfo[i+3].lower()] * 100 + \
                             eval(dateInfo[i+4])
                break

        if beginning == 0 or ending == 0:
            print "debug: " + m.group(2)
        if today >= beginning and today <= ending:
            # print block
            s2, e2 = 0, 0
            flag = False
            message = "Can't find today"
            while s2 != -1 and e2 != -1:
                s2, e2 = getEntry(block, s2)
                entry = block[s2:e2 + len('</tr>')]
                s2 = e2
                #print entry
                day1, day2, m = getMessage(entry, today)
                #print day1, day2, m

                if (day1 == -1 and day2 == today and m != None) or \
                    (day1 != -1 and date >= day1 and date <= day2 and m != None):
                        #print "today: ", today, date, day1, day2
                        message = m

            print datetime.datetime(*time_struct[0:6]).strftime('%b %d %Y, %A')
            print message
            break

    infile.close()

main()
