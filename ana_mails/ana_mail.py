#! /usr/bin/python
# -*- coding: UTF-8 -*-
import mailbox
import sys
import json
sys.path.append("../nlp/")
import word_cut
import time

def getcharsets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    return charsets

def handleerror(errmsg, emailmsg,cs):
    print(errmsg)
    print("This error occurred while decoding with ",cs," charset.")
    print("These charsets were found in the one email.",getcharsets(emailmsg))
    print("This is the subject:",emailmsg['subject'])
    print("This is the sender:",emailmsg['From'])

def getbodyfromemail(msg):
    body = None
    if msg.is_multipart():    
        for part in msg.walk():
            if part.is_multipart(): 
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=True) 

            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)

    elif msg.get_content_type() == 'text/plain':
        body = msg.get_payload(decode=True) 
    if not body:
        return body

    for charset in getcharsets(msg):
        try:
            body = body.decode(charset)
        except UnicodeDecodeError:
            handleerror("UnicodeDecodeError: encountered.",msg,charset)
        except AttributeError:
            handleerror("AttributeError: encountered" ,msg,charset)
    return body    

def segments(content):
    return jieba.cut(content)  

def word_count(text):
    words = segments(text)
    cnt = {}
    for w in words:
        if w not in cnt:
            cnt[w] = 0
        cnt[w] += 1
    for w in cnt:
        print ('%s\t%s' % (w, cnt[w])).encode('utf-8')

def clean_str(s):
    return s.replace('\r','').replace('\n','').replace('|', '').replace('-', '')

def ana_mail(mboxfile):
    text = ''
    cnt = {}
    process = 0
    fseg = open('seg.txt', 'w')
    fseg.write('[')
    for thisemail in mailbox.mbox(mboxfile):
        process += 1
        sender = thisemail['from']
        body = getbodyfromemail(thisemail)
        try:
            s = body.encode('utf-8').strip()
            if s.find('houhuibin') > 0:
                continue
            s = clean_str(s)
            ret = word_cut.cut(s)
            if len(ret) == 0:
                print >> sys.stderr, 'return null'
                continue
            time.sleep(0.1)
            obj = json.loads(ret)
            fseg.write(ret)
            fseg.write(',\n')
            for i in obj:
                for j in i:
                    for k in j:
                        pos = k['pos']
                        word = k['cont']
                        if pos in ('wp', 'c', 'r', 'q', 'u', 'nt', 'd'): # 标点，节次，代词
                            continue
                        if word not in cnt:
                            cnt[word] = 0
                        cnt[word] += 1
        except:
            time.sleep(0.05)
            continue
        if process % 10 == 0:
            print >> sys.stderr, process, 'done'
    fseg.write(']')
    fseg.close()
    f = open('w.txt', 'w')
    for i in cnt:
        f.write( ('%s\t%s\n' % (i, cnt[i])).encode('utf-8'))
    f.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'input mbox'
        sys.exit(1)

    mboxfile = sys.argv[1]
    ana_mail(mboxfile)

