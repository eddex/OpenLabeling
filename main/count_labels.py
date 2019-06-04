import os

SEARCH_DIR = "output/YOLO_darknet/"

CLASS_MAPPING = {
    '0': '1',
    '1': '2',
    '2': '3',
    '3': '4',
    '4': '5',
    '5': '6',
    '6': '7',
    '7': '8',
    '8': '9',
    '9': 'start'
}

CLASS_COUNT = {
    '0': 0,
    '1': 0, 
    '2': 0, 
    '3': 0, 
    '4': 0, 
    '5': 0, 
    '6': 0, 
    '7': 0, 
    '8': 0, 
    '9': 0 
}


def read_file(file_name):
    file_path = '{}{}'.format(SEARCH_DIR, file_name)
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            class_index = line.split()[0]
            if CLASS_MAPPING.get(class_index) == None:
                print ("Error class {} doesn't exist!".format(class_index))
            else:
                CLASS_COUNT[class_index] += 1


def print_classes_md_table():
    total = 0
    for i in CLASS_MAPPING:
        total += CLASS_COUNT[i]

    header_row = "class       "
    header_sep = "-------------"
    annotations_row = "annotations "
    distribution_row = "distribution"
    for i in CLASS_MAPPING:
        header_row = "{} | {}".format(header_row, CLASS_MAPPING[i])
        header_sep = "{}|---".format(header_sep)
        annotations_row = "{} | {}".format(annotations_row, CLASS_COUNT[i])
        distribution_row = "{} | {:.1f}%".format(distribution_row, CLASS_COUNT[i]/total*100)

    print("total: {}\n".format(total))
    print(header_row)
    print(header_sep)
    print(annotations_row)
    print(distribution_row)


def start():
    for filename in os.listdir(SEARCH_DIR):
        if filename.endswith('txt'):
            read_file(filename)
        else:
            print("Skipping file: {}".format(filename))
    print_classes_md_table()

if __name__ == "__main__":
    start()