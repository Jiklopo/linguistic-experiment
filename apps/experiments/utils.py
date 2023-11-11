def extract_file_name(file):
    file_name = file.name.split('/')[-1]
    no_extension = file_name.split('.')[0]
    no_label = no_extension.split('_')[0]
    return no_label
