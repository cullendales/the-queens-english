import os
import sys
import re
import tempfile
import subprocess
import webbrowser

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

    if not os.path.isfile(file):
        print(f"Error: File {file} not found.")
        return

    _, ext = os.path.splitext(file)

    if ext.lower() == ".html":
        with open(file, 'r', encoding='utf-8') as f:
            html_text = f.read()

        css_links = re.findall(r'href=["\'](.*?\.css)["\']', html_text)

        css_map = {}

        for css_file in css_links:
            if os.path.exists(css_file):
                with open(css_file, 'r', encoding='utf-8') as f:
                    css_text = f.read()
                css_converted = convert_spelling(css_text)

                css_temp = tempfile.NamedTemporaryFile(mode='w', suffix='.css', delete=False, encoding='utf-8')
                css_temp.write(css_converted)
                css_temp_path = css_temp.name
                css_temp.close()

                css_map[css_file] = css_temp_path
            else:
                print(f"Warning: linked CSS file {css_file} not found")

        for orig_css, temp_css in css_map.items():
            html_text = html_text.replace(orig_css, temp_css)

        html_temp = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        html_temp.write(html_text)
        html_temp_path = html_temp.name
        html_temp.close()

        webbrowser.open(f"file://{html_temp_path}")

    else:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        converted = convert_spelling(content)
        with tempfile.NamedTemporaryFile(mode='w', suffix=ext, delete=False, encoding='utf-8') as temp:
            temp.write(converted)
            temp_path = temp.name

        if ext.lower() == ".py":
            try:
                subprocess.run(['python', temp_path])
            finally:
                os.remove(temp_path)
        elif ext.lower() == ".css":
            subprocess.run(["open", temp_path])
        else:
            print("Sorry, file type unsupported currently.")

if __name__ == "__main__":
    main()