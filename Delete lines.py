import os
def delete_multiple_lines(original_file, line_numbers):
    """In a file, delete the lines at line number in given list"""
    is_skipped = False
    counter = 0
    # Create name of dummy / temporary file
    dummy_file = original_file + '.bak'
    # Open original file in read only mode and dummy file in write mode
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Line by line copy data from original file to dummy file
        for line in read_obj:
            # If current line number exist in list then skip copying that line
            if counter not in line_numbers:
                write_obj.write(line)
            else:
                is_skipped = True
            counter += 1

    # If any line is skipped then rename dummy file as original file
    if is_skipped:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)

L=["A001","A002","A003","A004","A005","G001","G002","G003","G004","G006","G007","H001","H002","H003","H004","H005"]#Replace the values of the list with the names of your files
for i in L:        
    url="../Desktop/Data/"+i+"/"+i+".txt"
    delete_multiple_lines(url, [0,1,2,3])
