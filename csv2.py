# import csv
#
#
# # Do the reading
# def read_csv(file):
#     file1 = open(file, 'rb')
#     reader = csv.reader(file1)
#     new_rows_list = []
#     for row in reader:
#        if row[2] == 'Test':
#           new_row = [row[0], row[1], 'Somevalue']
#           new_rows_list.append(new_row)
#     file1.close()   # <---IMPORTANT
#
# # Do the writing
# def write_csv(file):
#     file2 = open(file, 'wb')
#     writer = csv.writer(file2)
#     writer.writerows(new_rows_list)
#     file2.close()
#
#


import csv
import sys
file = "d:\\guy.csv"
f = open(file, 'wt')
try:
    writer = csv.writer(f)
    writer.writerow( ('Title 1', 'Title 2', 'Title 3') )
    for i in range(10):
        writer.writerow( (i+1, chr(ord('a') + i), '08/%02d/07' % (i+1)) )
finally:
    f.close()

print (open(sys.argv[1], 'rt').read())