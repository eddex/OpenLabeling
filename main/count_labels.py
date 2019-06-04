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


def print_classes():
    for i in CLASS_MAPPING:
        print("{}: {}".format(CLASS_MAPPING[i], CLASS_COUNT[i]))


def start():
    for filename in os.listdir(SEARCH_DIR):
        if filename.endswith('txt'):
            read_file(filename)
        else:
            print("Skipping file: {}".format(filename))
    print_classes()

if __name__ == "__main__":
    start()