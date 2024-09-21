import csv
import re

def extract_participants(contents):
    half = contents.split('2. Uczestnicy')[-1]
    section = re.split(r'\d+\.\s', half)[0]

    return section.strip()

def parse_participants(section):
    lines = section.splitlines()
    data_lines = lines[1:]

    participants = []
    for line in data_lines:
        # print(line)
        fields = line.split("\t")

        if len(fields) >= 4:
            name = fields[0].strip()
            time = fields[3].strip()

            name_parts = name.split()
            if len(name_parts) >= 2:
                last_name = name_parts[1]
                first_name = name_parts[0]

                if last_name.startswith("("):
                    last_name = name_parts[0]
                    first_name = "NULL"
            else: 
                last_name = name
                first_name = "NULL"

            status = "Zaświadczenie udziału" if 'godz.' in time else "Brak zaświadczenia"

            participants.append({
                "Nazwisko": last_name,
                "Imię": first_name,
                "Czas_uczestnictwa": time,
                "Status_zaświadczenia": status
            })

    return participants

def save_file(participants, output):
    sorted_participants = sorted(participants, key=lambda x: x['Nazwisko'])

    with open(output, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Nazwisko", "Imię", "Czas_uczestnictwa", "Status_zaświadczenia"])
        writer.writeheader()
        writer.writerows(sorted_participants)


def process_file(input, output):
    with open(input, 'r', encoding='utf-16') as file:
        contents = file.read()

    section = extract_participants(contents)
    participants = parse_participants(section)

    save_file(participants, output)

input = '../include/obecnosci.csv'
output = '../include/przetworzone.csv'

process_file(input, output)
print(f"Przetwarzanie zakończone. Plik zapisany jako {output}")    