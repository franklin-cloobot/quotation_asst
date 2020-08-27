
# import xlsxwriter
# import pandas as pd
# import json
# quatation = pd.DataFrame({'product':product,"client":dealer,"Quantity":quantity,"data":['today']})
# quatation.to_excel("quatation.xlsx")
# # creating attachment from the metric_stored inital path
# with open("quatation.xlsx", "rb") as attachment:
#     encoded_string = base64.b64encode(attachment.read()).decode('utf-8')


###############################################################################

import xlsxwriter
import shelve
from Monolithic.assist_multi_drc.constants import *
# shelve_db = shelve.open("botdata")

def generate_price_quotation_anex1(filename,path, multi_quote_list):
    import os
    here = os.path.dirname(__file__)
    print('In gpqa, mql::'+str(multi_quote_list))

    workbook = xlsxwriter.Workbook(path + filename)

    worksheet = workbook.add_worksheet()
    # worksheet2 = workbook.add_worksheet()
    # worksheet3 = workbook.add_worksheet()
    # worksheet4 = workbook.add_worksheet()
    # worksheet5 = workbook.add_worksheet()

    currency_format = workbook.add_format({'num_format': '$#,##0'})

    # Some sample data for the table.
    # data = [
    #     [1,'samsung','qr34e','modem', 50, 1000,50000],
    #     [1,'samsung','qr34e','modem', 50, 1000,50000],
    #     [1,'samsung','qr34e','modem', 50, 1000,50000],
    #     [1,'samsung','qr34e','modem', 50, 1000,50000],
    # ]

    data = []
    total_sum = 0
    for i, quote in enumerate(multi_quote_list):
        print(i,':q:',quote)
        total_sum += quote[HEADER_QUANTITY]*quote[HEADER_PRICE]
        data.append([i,quote[HEADER_DEALERS],quote[HEADER_PRODUCTS],quote[HEADER_QUANTITY],quote[HEADER_PRICE],quote[HEADER_QUANTITY]*quote[HEADER_PRICE]])
    
    print('In gpqa, data::'+str(data))


    data2 = [
        ['Total',total_sum],
        ['Tax','As applicable'],
        ['Delivery' , "Exwarehouse pickup"],
        ['Credit days',10],
    ]

    ####################################################################################
    #
    # Anexure 1.
    #
    caption = 'Anexure 1'

    # Set the columns widths.
    worksheet.set_column('B:H', 20)

    # Write the caption.
    worksheet.write('B1', caption)

    # Options to use in the table.
    options = {'data': data,
            'total_row': 1,
            'style': 'Table Style Light 11',
            'columns': [{'header': 'S.no','total_string': ' '},
                        {'header': 'Client', 'total_string': ' '},
                        {'header': 'Description','total_string': ' ' },
                        {'header': 'Quantity','total_string': ' ' },
                        {'header': 'Price', 'total_string': ' '},
                        {'header': 'Total price','total_string': ' '},
                        ]}

    # Add a table to the worksheet.
    table_length = len(data)+12

    worksheet.add_table('B2:H'+str(table_length),options)

    worksheet.write_row('B'+str(table_length-4), data2[0])
    worksheet.write_row('B'+str(table_length-3), data2[1])
    worksheet.write_row('B'+str(table_length-2), data2[2])
    worksheet.write_row('B'+str(table_length-1), data2[3])

    # Insert an image with scaling.

    worksheet.insert_image('F'+str(table_length-6), 'cloobot1.png', {'x_scale': 0.1, 'y_scale': 0.1})

    #################################################################################################

    workbook.close()