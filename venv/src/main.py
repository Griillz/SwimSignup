import selenium
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import sys
import smtplib
import ssl
import datetime
import imaplib
from gmail import EmailParser

class Main:
    emailparser = ''
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "swimsignup200@gmail.com"
    receiver_email = "anthonydeangelis7877@gmail.com"
    password = input("Type your password and press enter:")

    days = ['Tuesday','Thursday','Friday']
    times = ['7:00 AM', '8:00 AM','9:00 AM','10:00 AM','11:00 AM','12:00 PM','1:00 PM','2:00 PM','3:00 PM','4:00 PM']
    driver = webdriver.Chrome()

    def __init__(self):
        self.emailparser = EmailParser()
    def main_function(self):
        while True:
            send = False
            good_day_times, already_sent = self.getAvailable()
            with open("already_sent_times.txt", 'r') as infile:
                already_sent = infile.read().splitlines()

            if len(good_day_times) != len(already_sent):
                send = True
            else:
                for item in good_day_times:
                    if item[0] not in already_sent:
                        send = True
            if send:
                print("sent")
                self.sendListAvailable(good_day_times)


            for i in range(60):
                chosen = self.emailparser.get_value_chosen()
                if chosen != 'none':
                    print(chosen)
                    self.signMeUp(good_day_times,chosen)
                time.sleep(60)

    def signMeUp(self,good_day_times,value_sent):
        day_time_needed = ''
        for time in good_day_times:
            if time[2] == value_sent:
                day_time_needed = time[0]
        if day_time_needed == '':
            self.signUpFailed()
        else:
            self.checkIfAvail(day_time_needed)

    def checkIfAvail(self,day_time_needed):
        good_day_times, already_sent = self.getAvailable()
        current_day = []
        for day in good_day_times:
            if day[0] == day_time_needed:
                current_day = day
                xpath = day[1]
                print(xpath)
                testinglist = xpath.split('/')
                testinglist = testinglist[0:-1]
                newxpath = ''
                for item in testinglist:
                    newxpath+=item+'/'
                newxpath = newxpath[0:-1]
                print(newxpath)
                get_xpath = self.driver.find_element_by_xpath(newxpath)
                select = Select(get_xpath)
            for i in range(1,12):
                time.sleep(.06)
                try:
                    day_xpath = current_day[3].find_element_by_xpath(f"{newxpath}/option[{i}]")
                    print(day_xpath.text)
                    # if day_xpath.text == self.times:
                    #     good_day_times.append([f'{day[0]} {day_xpath.text}',f"{day[2]}/table/tbody/tr[4]/td[2]/select/option[{i}]",counter])
                except:
                    pass
            sys.exit()


    def signUpFailed(self):
        good_days, already_sent = self.getAvailable()
        self.sendListAvailable(good_days,'Subject: Signup Failed\n\nSomeone took that spot! Try again.\n')

    def sendListAvailable(self, good_day_times, message_to_add='Subject: Brooks YMCA Swim Times\n\nHave fun getting wet with old men!\n'):
        with open("already_sent_times.txt",'w') as outfile:
            messages = []
            for item in good_day_times:
                messages.append(f'\n\t{item[0]} \n\tSend New Email with {item[2]}')
                outfile.write(f'{item[0]}\n')
            for item in messages:
                message_to_add+=f'{item}\n'
            current_time = str(datetime.datetime.now())
            message_to_add+=f'\n\n{current_time.split(".")[0]}'
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(self.sender_email,self.password)
                server.sendmail(self.sender_email, self.receiver_email, message_to_add)

    def getAvailable(self):
        already_sent = []
        with open("already_sent_times.txt", 'r') as infile:
            for line in infile:
                already_sent.append(line)
        send = False
        self.driver.get('https://fcymca.org/swim-reservations/')
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight/3)")
        time.sleep(5)
        frame = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/article/div/p[6]/iframe')

        self.driver.switch_to.frame(frame)
        location = self.driver.find_element_by_id('location')
        select = Select(location)
        select.select_by_value('760')

        first_name = self.driver.find_element_by_name('first_name')
        first_name.send_keys('Joshua')

        last_name = self.driver.find_element_by_name('last_name')
        last_name.send_keys('Paskert')

        dob_month = self.driver.find_element_by_name('dob_month')
        select = Select(dob_month)
        select.select_by_value('11')

        dob_day = self.driver.find_element_by_name('dob_day')
        dob_day.send_keys('30')

        dob_year = self.driver.find_element_by_name('dob_year')
        dob_year.send_keys('1998')

        email = self.driver.find_element_by_name('email')
        email.send_keys('e.paskert@gmail.com')

        phone = self.driver.find_element_by_name('phone')
        phone.send_keys('(813) 410-7500')

        time.sleep(2)

        submit = self.driver.find_element_by_name('submitbtn_login')
        self.driver.execute_script("arguments[0].click();", submit)

        time.sleep(2)

        self.driver.switch_to.parent_frame()
        frame = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/article/div/p[6]/iframe')
        self.driver.switch_to.frame(frame)

        appointment = self.driver.find_element_by_name('appointment-type-filter')
        select = Select(appointment)
        select.select_by_value('27129')

        time.sleep(1)

        find_times = self.driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/input[1]')
        self.driver.execute_script("arguments[0].click();", find_times)

        time.sleep(3)


        children = []
        for i in range(0,9):
            try:
                child = self.driver.find_element_by_xpath(f'/html/body/div/div/div[1]/div[3]/fieldset[{i}]')
                if child:
                    xpath = f'/html/body/div/div/div[1]/div[3]/fieldset[{i}]'
                    children.append([child,xpath])
            except:
                pass
        available_days = []
        for item in children:
            available_days.append([(item[0].find_element_by_class_name("date-legend").text),item[0].find_element_by_class_name("date-legend"),item[1]])

        good_days = []
        for item in available_days:
            if item[0].strip().split(",")[0] in self.days:
                good_days.append(item)
        good_day_times = []
        time.sleep(1)
        counter = 0
        for day in good_days:
            for i in range(1,12):
                time.sleep(.06)
                try:
                    day_xpath = day[1].find_element_by_xpath(f"{day[2]}/table/tbody/tr[4]/td[2]/select/option[{i}]")
                    if day_xpath.text in self.times:
                        good_day_times.append([f'{day[0]} {day_xpath.text}',f"{day[2]}/table/tbody/tr[4]/td[2]/select/option[{i}]",counter,day[1]])
                        counter+=1
                except:
                    pass
        return good_day_times, already_sent

if __name__ == "__main__":
    testing = Main()
    testing.main_function()
