import csv


header = ['Time', 'Distance', 'Motor-1', 'Motor-2']
#data = ['Afghanistan', 652090, 'AF', 'AFG']


with open("MotionControl.csv", "a", newline='', encoding='UTF8') as file:
    writer = csv.writer(file)
    writer.writerow(header)
