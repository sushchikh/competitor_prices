def price_cutter_try(text):
    output_message = ''
    for i in text:
        if i.isdigit() or i == '.' or i == ',':
            output_message += i
        else:
            pass
    return str(output_message)


x = price_cutter_try('123руб4,56 руб')
print(x)
