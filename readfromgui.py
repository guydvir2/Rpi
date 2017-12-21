
def xtrct_nums(lista):
    new_list = []
    def xtrct_str(listb):
        new_lst = []
        temp = ''

        for i in range(len(listb)):
            try:
                int(listb[i])  # try in int
                temp = temp + listb[i]  # use is as char !
            except ValueError:
                if not temp == '':
                    new_lst.append(int(temp))
                    temp = ''
            # for last number in str
            if i == len(listb) - 1 and not temp == '':
                new_lst.append(int(temp))

        return new_lst

    if type(lista) is str:
        new_list = xtrct_str(lista)

    elif type(lista) is list:
        for item in lista:
            if type(item) is int:
                new_list.append(item)
            elif type(item).__name__ == 'str':
                z = xtrct_str(item)
                if not z == []: new_list.append(xtrct_str(item)[0])

    return new_list
