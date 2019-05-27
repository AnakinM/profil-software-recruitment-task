import csv
import os
import sqlite3
import json
import urllib.request
import math

class DataProcessing():
    __conn = None
    __c = None
    __voivodeships = []

    def __init__(self):
        # Set filename to work on.
        file_name = 'Liczba_osób_które_przystapiły_lub_zdały_egzamin_maturalny.csv'

        # Connect to database or create one if not exist in relative path. Also, create a table with columns specified in
        # csv file.
        self.conn = sqlite3.connect('wyniki-matury.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS wyniki
                    (terytorium text, status text, plec text, rok num, osoby num)''')

        # Check relative path to file to check if it exists. If not, connect to api, read json file and download the file.
        if not os.path.isfile(file_name):
            with urllib.request.urlopen("https://api.dane.gov.pl/resources/17363") as response:
                json_response = json.loads(response.read().decode())
                file_url = json_response["data"]["attributes"]["file_url"]
                urllib.request.urlretrieve(file_url, file_name)

        # Open a csv file and export content to database.
        with open(file_name) as csvfile:
            data = csv.reader(csvfile, delimiter=';')
            for row in data:
                if row[0] == "Terytorium": continue
                elif self.exists_in_database(row): continue
                self.c.execute('INSERT INTO wyniki VALUES (?,?,?,?,?)', row)
        
        # List of all voivodeships for future validation
        for voivode in self.c.execute('SELECT terytorium FROM wyniki WHERE status="zdało" and rok="2010" and plec="kobiety"'):
                self.__voivodeships.append(voivode[0])

    def __del__(self):
        self.conn.close()

    # Check if given records are already in database to avoid duplications.
    def exists_in_database(self, data):
        self.c.execute('SELECT * FROM wyniki WHERE terytorium=? and status=? and plec=? and rok=? and osoby=?', data)
        if self.c.fetchone():
            return True
        else:
            return False

    # Split command arguments into a list. Then check whether first item of list, a command itself, matches any
    # of definitions. If not, print error "Unknown command". If command finds it's match, then invoke a function
    # based on number of arguments passed.
    def setCommand(self, command):
        command_list = command.split(" ")
        if(command_list[0] == "avg"):
            if len(command_list) == 3:
                print(self.avg(command_list[1], command_list[2]))
            elif len(command_list) == 4:
                print(self.avg(command_list[1], command_list[2], command_list[3]))
            else:
                print("Invalid number of arguments")
            return

        if command_list[0] == "passed":
            if len(command_list) == 2:
                self.passed(command_list[1])
            elif len(command_list) == 3:
                self.passed(command_list[1], command_list[2])
            else:
                print("Invalid number of arguments")
            return
        
        if command_list[0] == "best":
            if len(command_list) == 2:
                print(self.best(command_list[1]))
            elif len(command_list) == 3:
                print(self.best(command_list[1], command_list[2]))
            else:
                print("Invalid number of arguments")
            return

        if command_list[0] == "regress":
            if len(command_list) == 1:
                self.regress()
            elif len(command_list) == 2:
                self.regress(command_list[1])
            else:
                print("Invalid number of arguments")
            return

        if command_list[0] == "compare":
            if len(command_list) == 3:
                self.compare(command_list[1], command_list[2])
            elif len(command_list) == 4:
                self.compare(command_list[1], command_list[2], command_list[3])
            else:
                print("Invalid number of arguments")
            return
        else:
            print("Unknown command")
            return
    
    # Calculate average number of people who took part in exam for each year up to given one for a given voivodeship.
    def avg(self, voivode, year, gender=None):
        list_of_participants = []
        iyear = int(year)
        voivode = voivode.capitalize()

        if voivode not in self.__voivodeships:
            return "Voivodeship not recognized"

        if iyear<2010 or iyear>2018:
            return "Year should be between 2010 and 2018"

        if gender is None:
            while iyear >= 2010:
                participants = 0
                for row in self.c.execute('SELECT osoby FROM wyniki WHERE terytorium=:voivode and status=:status and rok=:year',
                                    {"voivode":voivode, "status": "przystąpiło", "year":iyear}):
                    participants += row[0]
                iyear -= 1
                list_of_participants.append(participants)
            return sum(list_of_participants)/len(list_of_participants)

        elif gender == 'm':
            while iyear >= 2010:
                for row in self.c.execute('SELECT osoby FROM wyniki WHERE terytorium=:voivode and status=:status and plec=:gender and rok=:year',
                                        {"voivode":voivode, "status": "przystąpiło", "gender":"mężczyźni", "year":iyear}):
                    list_of_participants.append(row[0])
                iyear -= 1
            return sum(list_of_participants)/len(list_of_participants)
        
        elif gender =='f':
            while iyear >= 2010:
                for row in self.c.execute('SELECT osoby FROM wyniki WHERE terytorium=:voivode and status=:status and plec=:gender and rok=:year',
                                        {"voivode":voivode, "status": "przystąpiło", "gender":"kobiety", "year":iyear}):
                    list_of_participants.append(row[0])
                iyear -= 1
            return sum(list_of_participants)/len(list_of_participants)
        else:
            return "Gender should be 'm' or 'f'"
    
    # Calculate number of people who passed the exam for for a given voivodeship throughout all years.
    def passed(self, voivode, gender=None):
        iyear=2010

        if voivode not in self.__voivodeships:
            return "Voivodeship not recognized"

        if gender is None:
            while iyear<=2018:
                participated = 0
                passed = 0
                for row in self.c.execute('SELECT osoby FROM wyniki WHERE terytorium=:voivode and status=:status and rok=:year',
                                    {"voivode":voivode, "status": "przystąpiło", "year":iyear}):
                    participated += row[0]
                for second_row in self.c.execute('SELECT osoby FROM wyniki WHERE terytorium=:voivode and status=:status and rok=:year',
                                            {"voivode":voivode, "status": "zdało", "year":iyear}):
                    passed += second_row[0]
                print(iyear, " - ", math.floor((passed/participated)*100+.5), "%")  
                iyear += 1  
        
        elif gender is 'm':
            while iyear<=2018:
                participated = 0
                passed = 0
                for row in self.c.execute('SELECT osoby FROM wyniki WHERE terytorium=:voivode and status=:status and plec=:gender and rok=:year',
                                        {"voivode":voivode, "status": "przystąpiło", "gender":"mężczyźni", "year":iyear}):
                    participated = row[0]
                for second_row in self.c.execute('SELECT osoby FROM wyniki WHERE terytorium=:voivode and status=:status and plec=:gender and rok=:year',
                                        {"voivode":voivode, "status": "zdało", "gender":"mężczyźni", "year":iyear}):
                    passed = second_row[0]
                print(iyear, " - ", math.floor((passed/participated)*100+.5), "%")  
                iyear += 1

        elif gender is 'f':
            while iyear<=2018:
                participated = 0
                passed = 0
                for row in self.c.execute('SELECT osoby FROM wyniki WHERE terytorium=:voivode and status=:status and plec=:gender and rok=:year',
                                        {"voivode":voivode, "status": "przystąpiło", "gender":"kobiety", "year":iyear}):
                    participated = row[0]
                for second_row in self.c.execute('SELECT osoby FROM wyniki WHERE terytorium=:voivode and status=:status and plec=:gender and rok=:year',
                                        {"voivode":voivode, "status": "zdało", "gender":"kobiety", "year":iyear}):
                    passed = second_row[0]
                print(iyear, " - ", math.floor((passed/participated)*100+.5), "%")
                iyear += 1
        else:
            return "Gender should be 'm' or 'f'"

    # Print voivodeship with the highest pass rate for a given year.
    def best(self, year, gender=None):

        iyear = int(year)
        if iyear<2010 or iyear>2018:
            return "Year should be between 2010 and 2018"

        if gender is None:
            summ = 0
            count = 0
            d = {}
            for row in self.c.execute('SELECT terytorium, osoby FROM wyniki WHERE rok=:year and status=:status and terytorium!="Polska" ORDER BY terytorium DESC',
                                {"year": year, "status": "zdało"}):
                summ += row[1]
                count +=1
                if count == 2:
                    count = 0
                    d[row[0]] = summ
                    summ = 0
            return max(d, key=d.get)
        
        elif gender is 'm':
            for row in self.c.execute('SELECT terytorium FROM wyniki WHERE rok=:year and status=:status and plec=:gender and terytorium!="Polska" ORDER BY osoby DESC LIMIT 1',
                                {"year": year, "status": "zdało", "gender":"mężczyźni"}):
                return row[0]

        elif gender is 'f':
            for row in self.c.execute('SELECT terytorium FROM wyniki WHERE rok=:year and status=:status and plec=:gender and terytorium!="Polska" ORDER BY osoby DESC LIMIT 1',
                                {"year": year, "status": "zdało", "gender":"kobiety"}):
                return row[0]
        else:
            return "Gender should be 'm' or 'f'"

    # print all voivodeships which noted a regression in relation to previous years.
    def regress(self, gender=None):

        voivodes = []
        for voivode in self.c.execute('SELECT terytorium FROM wyniki WHERE status="zdało" and rok="2010" and plec="kobiety" and terytorium!="Polska"'):
                voivodes.append(voivode[0])
            
        if gender is None:
            summ = 0
            count = 0
            d = {}

            i=len(voivodes) -1
            while i>=0:
                for row in self.c.execute('SELECT rok, osoby FROM wyniki WHERE status=:status and terytorium=:voiv ORDER BY rok ASC',
                                    {"status": "zdało", "voiv": voivodes[i]}):
                    summ += row[1]
                    count +=1
                    if count == 2:
                        count = 0
                        d[row[0]] = summ
                        summ = 0

                prev_year_people = 0
                for year, people in d.items():
                    if prev_year_people>people:
                        print(voivodes[i], ": ", year-1, " -> ", year)
                        prev_year_people = people
                    else:
                        prev_year_people = people
                i -= 1

        elif gender is 'm':
            d = {}

            i=len(voivodes) -1
            while i>=0:
                for row in self.c.execute('SELECT rok, osoby FROM wyniki WHERE status=:status and plec=:gender and terytorium=:voiv ORDER BY rok ASC',
                                    {"status": "zdało", "gender": "mężczyźni", "voiv": voivodes[i]}):
                    d[row[0]] = row[1]

                prev_year_people = 0
                for year, people in d.items():
                    if prev_year_people>people:
                        print(voivodes[i], ": ", year-1, " -> ", year)
                        prev_year_people = people
                    else:
                        prev_year_people = people
                i -= 1
        
        elif gender is 'f':
            d = {}

            i=len(voivodes) -1
            while i>=0:
                for row in self.c.execute('SELECT rok, osoby FROM wyniki WHERE status=:status and plec=:gender and terytorium=:voiv ORDER BY rok ASC',
                                    {"status": "zdało", "gender": "kobiety", "voiv": voivodes[i]}):
                    d[row[0]] = row[1]

                prev_year_people = 0
                for year, people in d.items():
                    if prev_year_people>people:
                        print(voivodes[i], ": ", year-1, " -> ", year)
                        prev_year_people = people
                    else:
                        prev_year_people = people
                i -= 1
        else:
            return "Gender should be 'm' or 'f'"

    # Compare two voivodeships according to their pass rates throughout all years.
    def compare(self, voivode_1, voivode_2, gender=None):

        if voivode_1 not in self.__voivodeships:
            return "Voivodeship 1 not recognized"

        if voivode_2 not in self.__voivodeships:
            return "Voivodeship 2 not recognized"

        if gender is None:
            l_1 = []
            l_2 = []

            summ = 0
            count = 0
            for row in self.c.execute('SELECT osoby FROM wyniki WHERE status=:status and terytorium=:voiv ORDER BY rok ASC',
                                    {"status": "zdało", "voiv": voivode_1}):
                summ += row[0]
                count +=1
                if count == 2:
                    count = 0
                    l_1.append(summ)
                    summ = 0
            
            summ = 0
            count = 0
            for row in self.c.execute('SELECT osoby FROM wyniki WHERE status=:status and terytorium=:voiv ORDER BY rok ASC',
                                    {"status": "zdało", "voiv": voivode_2}):
                summ += row[0]
                count +=1
                if count == 2:
                    count = 0
                    l_2.append(summ)
                    summ = 0

            year=2010
            for i in range(9):
                if l_1[i]>l_2[i]:
                    print(year, " - ", voivode_1)
                elif l_2[i]>l_1[i]:
                    print(year, " - ", voivode_2)
                year += 1

        elif gender is 'm':
            l_1 = []
            l_2 = []

            for row in self.c.execute('SELECT osoby FROM wyniki WHERE status=:status and plec=:gender and terytorium=:voiv ORDER BY rok ASC',
                                    {"status": "zdało", "gender": "mężczyźni", "voiv": voivode_1}):
                l_1.append(row[0])

            for row in self.c.execute('SELECT osoby FROM wyniki WHERE status=:status and plec=:gender and terytorium=:voiv ORDER BY rok ASC',
                                    {"status": "zdało", "gender": "mężczyźni", "voiv": voivode_2}):
                l_2.append(row[0])

            year=2010
            for i in range(9):
                if l_1[i]>l_2[i]:
                    print(year, " - ", voivode_1)
                elif l_2[i]>l_1[i]:
                    print(year, " - ", voivode_2)
                year += 1
            
        elif gender is 'f':
            l_1 = []
            l_2 = []

            for row in self.c.execute('SELECT osoby FROM wyniki WHERE status=:status and plec=:gender and terytorium=:voiv ORDER BY rok ASC',
                                    {"status": "zdało", "gender": "mężczyźni", "voiv": voivode_1}):
                l_1.append(row[0])

            for row in self.c.execute('SELECT osoby FROM wyniki WHERE status=:status and plec=:gender and terytorium=:voiv ORDER BY rok ASC',
                                    {"status": "zdało", "gender": "kobiety", "voiv": voivode_2}):
                l_2.append(row[0])

            year=2010
            for i in range(9):
                if l_1[i]>l_2[i]:
                    print(year, " - ", voivode_1)
                elif l_2[i]>l_1[i]:
                    print(year, " - ", voivode_2)
                year += 1
        else:
            return "Gender should be 'm' or 'f'"

# Create object.
dp = DataProcessing()

if __name__ == '__main__':

    # Main loop
    is_exit = False
    while not is_exit:
        command = input(": ")
        if command == "exit":
            is_exit = True
        else:
            dp.setCommand(command)

# Destroy object to close connection with database.
del dp