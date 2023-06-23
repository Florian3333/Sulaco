import datetime
import calendar
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF


def time_life():
    current_month = datetime.datetime.now().month
    name_current_month = calendar.month_name[current_month]
    current_date = datetime.date.today()
    current_year = datetime.datetime.now().year
    current_time = datetime.datetime.now().time()

    return name_current_month, current_date, current_year, current_time

def read_data1(file):
    config_file_path = os.path.join(os.path.dirname(__file__), file)
    # Json file configuration reading
    with open(config_file_path) as config_file:
        config_data = json.load(config_file)
    return config_data


def read_data(liste):
    omega = True
    while omega:
        which_file = input('which file you would like to read data?')
        if not which_file.isdigit():
            print('only numbers please !!')
            continue
        config = read_data1('configbudget.json')
        chosing_month = config['chosing_file_month']
        # Pathway to the XML file 
        try:
            fichier_xml = str(chosing_month) + str(liste[int(which_file)-1])
            omega = False
            return fichier_xml
        except:
            print('there is no file number: ' + str(which_file) + '!')





def pdf_report(current_date, modeles, nombres, aa, current_time):
    # Creation of the personalised PDF class
    class PDF(FPDF):
        def header(self):
            pass

        def footer(self):
            pass

    # Creation of the PDF objet 
    pdf = PDF()

    # Add a page
    pdf.add_page()

    # Definition of the cell board's dimension 
    cell_width = 40
    cell_height = 10

    # Title's definition

    titre = f"Budget {aa} issued the {str(current_date)} at {str(current_time)}" 

    # cration of the bold title
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(0, cell_height, txt=titre, ln=True, align="C")
    pdf.ln()

    # Creating the table header 
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(cell_width, cell_height, txt="Budgets", border=1)
    pdf.cell(cell_width, cell_height, txt="Budget quantification", border=1)
    pdf.ln()

    # Filling the table with data
    pdf.set_font("Arial", size=12)
    for i in range(len(modeles)):
        modele = modeles[i]
        nombre = nombres[i]
        pdf.cell(cell_width, cell_height, txt=modele, border="LBR")
        pdf.cell(cell_width, cell_height, txt=str(nombre), border="LBR")
        pdf.ln()

    # save the pdf file 
    pdf.output(f"budget{aa} issued the {str(current_date)} at {str(current_time)}.pdf") 

def report():
    ll = []
    kk = []
    list_histo = read()
    for i in list_histo[2:]:
        name_eco, value = i.split(':')
        ll.append(name_eco)
        kk.append(value)
    x = np.array(ll)
    y = np.array(kk)
    plt.bar(x,y)
    plt.show()
    pdf = input('would you like get a pdf as report for this month ?')
    if pdf == 'yes':
        print(list_histo)
        aa = list_histo[1]
        tt = ''
        for i in aa:
            if not i in ':\t':
                tt += i
        name_current_month, current_date, current_year, current_time = time_life()
        nn =''
        for i in str(current_time):
            if i in ':':
                nn += 'h'
            else:
                nn += i
        pdf_report(current_date, ll, kk, tt, nn)

def change_element(liste):
    fichier_xml = read_data(liste)
    # Parse the XML file
    tree = ET.parse(fichier_xml)
    # Get the root of the XML tree
    root = tree.getroot()
    #nb_modif = 0
    nb_modif = int(input('number of elements to change (max between 1 to 9) ? put 0 to exit'))
    while nb_modif != 0:
        nb_modif -= 1
        month_year = input('''give the month and the year concerned (must be sticked together) 
        ex :June2023 and the element name you 'd like to change both have to be separated by a space''').split()
        try:
            element_modif = root.find(f"./{month_year[0]}/{month_year[1]}")
            if element_modif is not None:
                # Modify the element's value
                while True:
                    mod_value = input('which value to modify ? only digits please!')
                    if not mod_value.isdigit():
                        print('you did not put digits only do it again !')
                        continue
                    element_modif.text = mod_value
                    # record modifications in the XML file
                    tree.write(fichier_xml)
                    print("La valeur a été modifiée avec succès.")
                    break
            else:
                print("L'élément à modifier n'a pas été trouvé.")
        except:
            print('you should tape like this = ex :June2023 and the element name you \'d like to change both have to be separated by a space ')

def simple_reading():
    try:
        contents = os.listdir('dossierxml')
        x = 0
        print('here is the budjet month list : ')
        liste = []
        for i in contents:
            x += 1
            print('Num:', x, ':', i)
            liste.append(i)
        if x == 1:
            print()
            print('there is just ' + str(x) + ' existing file')
        else:
            print()
            print('there are ' + str(x)+' existing files')
    except FileNotFoundError:
        print('Sorry no existing file')
    except Exception as e:
        print('a mistake happened here ' + str(e))
    return liste



def read():
    list_histo = []
    liste = simple_reading()
    fichier_xml = read_data(liste)
    # Parse the xml file
    tree = ET.parse(fichier_xml)
    # Get the root of the XML tree
    root = tree.getroot()
    # iteration of the path of child elements of the root
    for element in root.iter():
        # display the name of the element and its content
        print(element.tag, ":", element.text)
        list_histo.append(element.tag + ":" + str(element.text))
    return list_histo  



def create_budget_month():
    while True:
        try:
            paycheck = int(input('What is your paycheck? please only numbers'))
            renting_location = int(input('What are your renting location incomes?please only numbers'))
            renting_fees = int(input('What are your renting fees? please only numbers'))
            food_expenses = int(input('What are your food expenses? please only numbers'))
            electricity_invoice = int(input('What is your electricity invoice for the month? please only numbers'))
            transport_expenses = int(input('What are your transport expenses? please only numbers'))
            break
        except:
            print('put only numbers !!')

    sum1 = sum([paycheck, renting_location])
    sum2 = sum([renting_fees, food_expenses, electricity_invoice, transport_expenses])
    balance = sum1 - sum2
    pp = [
        ('paycheck', paycheck),
        ('renting_location', renting_location),
        ('renting_fees', renting_fees),
        ('food_expenses', food_expenses),
        ('electricity_invoice', electricity_invoice),
        ('transport_expenses', transport_expenses),
        ('total_incomes', sum1),
        ('total_expenses', sum2),
        ('balance', balance)
    ]

    name_current_month, current_date, current_year, current_time = time_life()
    # xml document's creation
    doc = minidom.Document()
    # creation of the root element
    root = doc.createElement(f"budget{current_date}")
    doc.appendChild(root)
    # first book creation
    livre = doc.createElement(name_current_month + str(current_year))
    livre.setAttribute("id", '1')
    root.appendChild(livre)

    # elements's adding in the book
    for name, value in pp:
        element = doc.createElement(name)
        element.appendChild(doc.createTextNode(str(value)))
        livre.appendChild(element)

    config = read_data1('configbudget.json')
    budget_month = config['budget_month_file']
    # Recording of the xml document in a file
    with open(str(budget_month) + str(current_date) + ".xml", "w", encoding="utf-8") as file:    
        doc.writexml(file, indent="\t")
    print("Fichier XML créé avec succès.")



def main():
    if not os.path.exists("dossierxml"):
        os.makedirs("dossierxml")
    bb = ''
    while bb != 'stop':
        bb = input("""you want to 'stop', 'create' a new month budget, 'get' pdf of all caracteristics for a
                    month, 'cancel' one month, 'change' a specific information inside an xml file, 'read' a specific xml file""")
        if bb == 'create':
            create_budget_month()
        if bb == 'read':
            read()
        if bb == 'stop':
            exit(0)
        if bb == 'change':
            liste = simple_reading()
            change_element(liste)
        if bb == 'report':
            report()
main()
