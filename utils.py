from typing import Dict, Final
def to_translit(raw_text: str):
    LETTERS_MAP: Final[Dict[str, str]]= {
    'А': 'A',
    'Б': 'B',
    'В': 'V',
    'Г': 'G',
    'Д': 'D',
    'Е': 'E',
    'Ё': 'Yo',
    'Ж': 'Zh',
    'З': 'Z',
    'И': 'I',
    'Й': 'Y',
    'К': 'K',
    'Л': 'L',
    'М': 'M',
    'Н': 'N',
    'О': 'O',
    'П': 'P',
    'Р': 'R',
    'С': 'S',
    'Т': 'T',
    'У': 'U',
    'Ф': 'F',
    'Х': 'Kh',
    'Ц': 'Ts',
    'Ч': 'Ch',
    'Ш': 'Sh',
    'Щ': 'Shch',
    'Ы': 'Y',
    'Э': 'E',
    'Ю': 'Yu',
    'Я': 'Ya'
}
    processed_text = ''
    for i in range(len(raw_text)):
        letter = raw_text[i].upper()
        if letter in LETTERS_MAP.keys():
            if raw_text[i].islower():
                processed_text += LETTERS_MAP[letter].lower()
            else:
                processed_text += LETTERS_MAP[letter]
        else:
            processed_text += raw_text[i]
    

    return processed_text

if __name__ == "__main__":
    text = 'Привет, как дела?'
    print(to_translit(text))