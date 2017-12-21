def print_sorted_list(data, rows=0, columns=0, ljust=10):
    """
    Prints sorted item of the list data structure formated using
    the rows and columns parameters
    """
    if not data:
        return

    if rows:
        # column-wise sorting
        # we must know the number of rows to print on each column
        # before we print the next column. But since we cannot
        # move the cursor backwards (unless using ncurses library)
        # we have to know what each row with look like upfront
        # so we are basically printing the rows line by line instead
        # of printing column by column
        lines = {}
        for count, item in enumerate(sorted(data)):
            lines.setdefault(count % rows, []).append(item)
        for key, value in sorted(lines.items()):
            for item in value:
                print (item.ljust(ljust)),
                print()
    elif columns:
        # row-wise sorting
        # we just need to know how many columns should a row have
        # before we print the next row on the next line.
        for count, item in enumerate(sorted(data), 1):
            print (item.ljust(ljust)),
            if count % columns == 0:
                print()
    else:
        print (sorted(data))  # the default print behaviour


if __name__ == '__main__':
    the_list = [['apricot','banana','apple','car','coconut','baloon','bubble'],['guy','dvir']]
    print_sorted_list(the_list)
    print_sorted_list(the_list, rows=3)
    print_sorted_list(the_list, columns=3)
