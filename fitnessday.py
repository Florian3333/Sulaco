import sqlite3
import os
import datetime
import matplotlib.pyplot as plt
import numpy as np


def read_database(pathway, name_table):
    conn = sqlite3.connect(pathway)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {name_table}')
    results = cursor.fetchall()
    for row in results:
        print(row)
    conn.close()
    return results

def get_date_hour():
    maintenant = datetime.datetime.now()
    date = maintenant.strftime("%Y-%m-%d")
    heure = maintenant.strftime("%H:%M:%S")
    return date, heure, maintenant

def acces_authorized():
    if input("professionnal part need a password") in ('superman'):
        return True 

def calculation_calories_a_day(time):
    read_database('poids.db', 'poids_calories')
    hh = ''
    total = 0
    while hh != 'stop':   
        hh = input(f'what you\'d like to add in your menu {time}?')
        if hh != 'stop':
            cc = int(input(f'how many in grammes you consumed of that for this {time}?'))
            conn = sqlite3.connect('poids.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM poids_calories WHERE id = ?", (int(hh),))
            result = cursor.fetchone()
            if result is not None:
                total += result[2]*cc
                print('resul ='+ str(total))
                c = input('are you sure to add it?')
                if c in ('no'):
                    total -= result[2]*cc
                    print('resul ='+ str(total))
            else:
                print('invalid key in database!!')
    return total

def won_lost_calories():
    lostcalories_days = 2000
    balance = (total_calories_absorbed - lostcalories_days)
    return balance

def Body_Mass_Index(weight, size):
    BMI = weight / (size*size) 
    print('your BMI is ' + str(BMI))
    if BMI < 18.5:
        print('you are in underweight situation !')
    elif 18.5 < BMI < 24.9:
        print('you are in a normal weight situation')
    elif 25 < BMI < 29.9:
        print('you are considered as overweighted')
    elif 30 < BMI < 34.9:
        print('you are considered as obese of class I')
    elif 35 < BMI < 39.9:
        print('you are considered as obese of class II')
    else:
        print('you are considered as obese of class III(morbid)')

def weight_target(): 
    project = weight - losing_weight_target
    print(f"you project is to weight {losing_weight_target} kg and to lose {project} kg.")
    return project

def histogram(data, xlabel, ylabel, title, project = 0):
    x_positive = [i for i, val in enumerate(data) if val >= 0]
    x_negative = [i for i, val in enumerate(data) if val < 0]
    y_positive = [val for val in data if val >= 0]
    y_negative = [-val for val in data if val < 0]
    plt.bar(x_positive, y_positive, color='blue')
    plt.bar(x_negative, y_negative, color='red')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(np.arange(len(data)), np.arange(1, len(data) + 1))
    plt.show()

def coordinates_patient():
    #name = input('your name ?')
    #surname = input('your surname ?')
    weight = float(input('what is your current weight ?'))
    size = float(input('what is your size ?'))
    return weight, size

def calculation_loop(calories, b):
    while True:
        cc1 = calculation_calories_a_day(b)
        calories += cc1
        print(calories, f'consumed calories for {b}')
        break
    return calories

def insert_and_confirm():
    cursor.execute(f"INSERT INTO poids_client (date, loss_projet, abs_calories, grammes_fat, real_calculcal) VALUES ('{date}', {losing_weight_target} , {total_calories_absorbed} , {result_day} , {balance})")
    con.commit()
    print('included into database, thanks!')



if not os.path.exists('poids.db'):
    conn = sqlite3.connect('poids.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE poids_calories (
                        id INTEGER PRIMARY KEY,
                        nom TEXT,
                        calories INTEGER)''')
else:
    conn = sqlite3.connect('poids.db')

cursor = conn.cursor()

weight, size = coordinates_patient()
Body_Mass_Index(weight, size)
losing_weight_target = float(input('what is your weight target (say about the final result in Kg you desire to aim)?'))
weight_target()

faire = ''
while faire != 'stop':
    faire = input('lire or integrer(pro-part) or calculate or cancel or stop, situa?')
    if faire == 'integrer':
        if acces_authorized():
            items = ''
            while items != 'stop':
                items = input('ajouter les elements')
                aa = items.split()
                if len(aa) == 2:
                    cursor.execute(f"INSERT INTO poids_calories (nom, calories) VALUES ('{aa[0]}', {aa[1]})")
                    conn.commit()
                    print('included into database, thanks!')

    if faire == 'lire':
        read_database('poids.db', 'poids_calories')

    if faire == "cancel":
        while True:
            read_database('poids.db', 'poids_calories')
            cancelation = input('which one you\'d like to cancel?')
            if cancelation == 'stop':
                break
            cursor.execute("DELETE FROM poids_calories WHERE id = ?", (int(cancelation),))
            conn.commit()

    if faire == 'calculate':
        while True:
            if input('u wish add a meal in the day yes or no?') in ('no'):
                continue
            date, heure, date_hour = get_date_hour()
            current_hour = tuple(heure)
            calories1 = 0
            calories2 = 0
            calories3 = 0

            if 5 <= int(current_hour[1]) <= 10:
                calories1 += calculation_loop(calories1, 'for morning')

            if 11 <= int(current_hour[1]) <= 13:
                calories2 += calculation_loop(calories2, 'for noon')

            if 18 <= int(current_hour[1]) <= 21:
                calories3 += calculation_loop(calories3, 'for the evening')

            # print(str(calories1), str(calories2), str(calories3))
            total_calories_absorbed = calories1 + calories2 + calories3
            print('the number of absorbed kilocalories is ' + str(total_calories_absorbed))
            balance = won_lost_calories() 
            if balance > 0:
                result_day = balance/9
                print('you won '+ str(result_day) + 'grammes of fat today.')
            else:
                result_day = balance/9
                print('you lost '+ str(result_day) + 'grammes of fat today.')

            if not os.path.exists('poids_patient.db'):
                con = sqlite3.connect('poids_patient.db')
                cursor = con.cursor()
                cursor.execute('''CREATE TABLE poids_client (
                                    id INTEGER PRIMARY KEY,
                                    date TEXT,
                                    loss_projet INTEGER,
                                    abs_calories INTEGER,
                                    grammes_fat INTEGER,
                                    real_calculcal INTEGER
                                    )''')
                insert_and_confirm()
            else:
                con = sqlite3.connect('poids_patient.db')
                cursor = con.cursor()
                insert_and_confirm()
            cursor.execute("SELECT * FROM poids_client")
            results = cursor.fetchall()
            for row in results:
                print(row)
            con.close()
            break

    if faire == 'situa':
        all_data = read_database('poids_patient.db', 'poids_client')
        li = []
        la =[]
        for i in all_data:
            li.append(i[3])
            la.append(i[5])
        histogram(li, 'Days', 'rate of Kcal before sport', 'how much I consumed in Kcal')
        histogram(la, 'Days', 'rate of Kcal after sport', 'how much I consumed in Kcal')

        liste_nombres = la
        somme = sum(liste_nombres)
        percentage1 = (losing_weight_target*1000 - somme)/(losing_weight_target*1000)*100
        percentage2 = 100 - percentage1
        if percentage2 > 0:
            print(f'the pourcentage of your losing weight project is {round(percentage2, 2)} % of fatty mater won unfortunatly')
        else:
            print(f'the pourcentage of your losing weight project is {round(percentage2, 2)} % of fatty mater lost')
