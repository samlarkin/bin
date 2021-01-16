#!/usr/bin/python3
import re

with open("raw_contacts.csv", "r") as f:
    raw_data=f.readlines()

contacts = []

for line in raw_data:
    contact = {}

    name = re.search(r"^[a-zA-Z ]+", line)
    if name != None:
        contact.update({"name":name.group()})
    else:
        contact.update({"name":None})

    email = re.findall(r"[A-Za-z0-9\.\-+_]+@[A-Za-z0-9\.\-+_]+\.[a-z]+", line)
    contact_email = []
    if email != []:
        for address in email:
            address = address.lower()
            contact_email.append(address)
        contact.update({"email":contact_email})
    else:
        contact.update({"email":None})

    phone = re.findall(r"[04 ]+\d+[0-9 ]+",line)
    contact_phone = []
    if phone != []:
        for number in phone:
            number = number.replace(" ","")
            if re.match(r"^44", number):
                number = number.replace("44","0",1)
            contact_phone.append(number)
        contact.update({"phone":contact_phone})
    else:
        contact.update({"phone":None})

    contacts.append(contact)

with open("contacts.csv", "w+") as f:
    f.write("name,email,phone"+"\n")
    csv_line = "{},{},{}"
    for contact in contacts:
        f.write(csv_line.format(contact["name"],contact["email"],contact["phone"])+"\n")
