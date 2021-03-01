import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "renter.settings")
import django
django.setup()

import random
from rentacar.models import CustomUser

with open("populate_db/words.txt", "r") as f:
    unContent = f.read()

with open("populate_db/fnames.txt", "r") as f:
    fnContent = f.read()

with open("populate_db/lnames.txt", "r") as f:
    lnContent = f.read()

with open("populate_db/kadut.txt", "r") as f:
    knContent = f.read()

with open("populate_db/kunnat.txt", "r") as f:
    kContent = f.read()

emailEndings = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@icloud.com", "@microsoft.com"]
phoneBeginnings = ["040", "045", "050", "044", ]

words = unContent.split(',')
fnames = fnContent.split(',')
lnames = lnContent.split(',')
knimet = knContent.split(',')
kunimet = kContent.split(',')

for i in range(100):
    vusername = words[random.randint(1, len(words)-1)] + words[random.randint(1, len(words)-1)]
    vfirst_name = fnames[random.randint(0,len(fnames)-1)]
    vlast_name = lnames[random.randint(0,len(lnames)-1)]
    vemail = f"{vfirst_name}.{vlast_name}{emailEndings[random.randint(0,len(emailEndings)-1)]}"
    vphonenum = f"{phoneBeginnings[random.randint(0,len(phoneBeginnings)-1)]}{random.randint(1000000, 9999999)}"
    vaddress = f"{knimet[random.randint(0,len(knimet)-1)]} {random.randint(1, 25)}"
    vcity = f"{kunimet[random.randint(0,len(kunimet)-1)]}"

    print(f"Username: \t{vusername}\nFirstname: \t{vfirst_name}\nLastname: \t{vlast_name}\n"
            f"Email: \t\t{vemail}\nPhone: \t\t{vphonenum}\nStreet: \t{vaddress}\n"
            f"City: \t\t{vcity}\nCountry: \tFinland\n")

    CustomUser.objects.bulk_create([
        CustomUser(username=vusername, first_name=vfirst_name, last_name=vlast_name, email=vemail, 
            phonenum=vphonenum, address=vaddress, postcode=random.randint(10000, 99999),
            city=vcity, country="Finland", paymentMethod=0),
    ])