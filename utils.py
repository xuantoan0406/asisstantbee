def read_file_txt(filename):

    with open(filename, 'r') as file:
        content = file.read()
    print(content)
    return content
