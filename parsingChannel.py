import csv
with open('OpenBCI-Raw-2017-04-12_20-55-16_Nicks_heart_001.txt', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        print ', '.join(row)
