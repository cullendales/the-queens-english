import os
import sys
import re
import tempfile
import subprocess
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

canadian_english = {
    # ou words
    'colour' : 'color',
    'neighbour' : 'neighbor',
    'favour' : 'favor',
    'labour' : 'labor',
    'behaviour' : 'behavior',
    
    # ise instead of ize & yse instead of yze
    'realise' : 'realize',
    'analyse' : 'analyze',
    'initialise' : 'initialize',
    'normalise' : 'normalize',
    'customise' : 'customize',
    
    # re opposed to er
    'centre' : 'center', 
    'fibre' : 'fiber',
    'theatre': 'theater',
    'metre': 'meter',
    'fibre': 'fiber',
    'calibre': 'caliber',

    # l's
    'travelled' : 'traveled',
    'traveller' : 'traveler',
    'labelling' : 'labeling',
    'modelling' : 'modeling',
    'modelled' : 'modeled',
    'cancelled' : 'canceled',

    # ce opposed to se
    'defence' : 'defense',
    'licence' : 'license',

    # words that didnt really fit in the categories above
    'cheque' : 'check',
    'catalogue' : 'catalog',
    'grey' : 'gray',

    # longer phrases
    'background-colour' : 'background-color',
    'border-colour' : 'border-color',
    'outline-colour' : 'outline-color',
    'text-decoration-colour' : 'text-decoration-color',
    'column-rule-colour' : 'column-rule-color',
}


# uses regex to check spelling and change to american form for running program
def convert_spelling(text):
    pattern = r'\b(' + '|'.join(re.escape(word) for word in canadian_english.keys()) + r')\b'

    def conversion(match):
            word = match.group(1)

            if word.isupper():
                return canadian_english[word.lower()].upper()
            elif word.istitle():
                return canadian_english[word.lower()].capitalize()
            else:
                return canadian_english[word.lower()]

    res = re.sub(pattern, conversion, text, flags = re.IGNORECASE)

    return res
        

def process_file(file):

    try:
        with open(file, 'r') as f:
            code_text = f.read()

            converted_text = convert_spelling(code_text)
            return converted_text
    
    
    except FileNotFoundError:
        print(f"Error: The program {file} could not be found")
        return None
    

def main():

    file = sys.argv[1]

    with open(file, 'r', encoding='utf-8') as f:
        proper_english = f.read()

    incorrect_english = convert_spelling(proper_english)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp:
        temp.write(incorrect_english)
        temp_path = temp.name

    try:
        subprocess.run(['python', temp_path])
    finally:
        os.remove(temp_path)

if __name__ == "__main__":
    main()