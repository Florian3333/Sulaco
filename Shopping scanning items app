# To use this application you'll need to use the 'config.json' file that you can find in the same repository(Sulaco).

import json
import os
import random
import qrcode


def authorize():
    if input('Tape your professional ID please: ') in ('aquaman','superman'):
        print('Your professional ID is correct!')
        return True
    print('Your professional ID is not correct!')
    return False


def general_list(list_pro):
    for idx, x in enumerate(list_pro,start=1):
        print('Number: ',idx,x)


def read_data(file):
    with open(file, 'r') as f:
        return json.load(f)


def write_data(file,data):
    with open(file, 'w') as f:
        json.dump(data, f)


def remove_item(list,idx):
    if idx in range(len(list)):
        return list.pop(idx)  
    else:
        print('You selected non existing item.')


def qrcode_creation(total_price, list_client, image_file):
    data = '\n'.join(f'Item : %s , Price : %s' % (item,price) for item, price in list_client)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data + str('\nTotal = ' + str(total_price)))

    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.show()
    img.save(image_file)
    print('Operation finished')


def pro(list_pro):
    pro_command = ''

    while pro_command != 'stop':

        pro_command = input('To add the item name plus its price add name in first separated by a space'
                            ' for the price: (to stop tape the code (stop)), to cancel one item put (cancel): ')

        if pro_command == 'cancel':
            general_list(list_pro)
            idx = int(input('Which number you\'ll change ? : ')) - 1
            remove_item(list_pro, idx)
        elif pro_command == 'list':
            general_list(list_pro)
        elif pro_command != 'stop':
            product = pro_command.split()
            if len(product) >= 2:  
                product[1] = int(product[1])
                list_pro.append(product)

    return list_pro


def client(list_pro, client_file):
    list_client = []
    client_command = ''
    general_list(list_pro)
    while client_command != 'finish':

        client_command = input('To add on the basket put the number associated to the list '
                               '(put finish to stop the listing),if cancel one article (press cancel,'
                               ' for list your choice (make list)): ')

        if client_command.isdigit():
            add_idx = int(client_command) - 1
            if add_idx in range(len(list_pro)):
                list_client.append(list_pro[add_idx])

        elif client_command == 'cancel':
            del_idx = int(input('ID= of the item you wish to cancel from the list (just put number) '
                                'finish to leave the cancellation? : ')) - 1
            remove_item(list_client, del_idx)

        elif client_command == 'list':
            general_list(list_client)

        elif client_command != 'finish':
            print('You have to add just one number non separated by a space or finish, cancel,'
                  ' list commands if not it doesn\'t work')

    write_data(client_file, list_client)

    total_price = sum([price for product, price in list_client])  

    print('Your shopPinG list if the following one:', end='\n')
    general_list(list_client)
    print('For a total of ' + str(total_price) + ' Euros')

    return list_client, total_price


def main():
    config = read_data('config.json')
    pro_file = config['pro_file']
    if not os.path.exists(pro_file):
        write_data(pro_file, [])
    list_pro = read_data(pro_file)

    main_command = ''

    while main_command != 'stop':
        main_command = input('Pro space (put pro) or client space (put client) and if exit from app (put stop): ')
        if main_command == 'pro':
            if authorize():
                list_pro = pro(list_pro)

        if main_command == 'client':
            client_id = str(random.randint(1, 1000))
            client_file = config['client_file'] + client_id + '.json'
            image_file = config['image_path'] + '//qrcode' + client_id + '.png'
            list_client, total_price = client(list_pro, client_file)
            qrcode_creation(total_price, list_client, image_file)

    write_data(pro_file, list_pro)


main()
