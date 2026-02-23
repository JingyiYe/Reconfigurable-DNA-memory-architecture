"""
Image to DNA Sequence Converter
================================

This module converts pixel data from an image into DNA sequence representations.
It processes RGB images and maps colors to binary codes, which are then converted
to DNA nucleotide sequences.

Author: [Ao Liu]
Date: [2026/02/22]
Version: 1.0
"""

from PIL import Image
import csv
import itertools
from typing import List, Tuple, Dict, Optional, Any


# Constants
# =========

# Color to binary mapping dictionary
# Format: (R, G, B) -> binary code
COLOR_ENCODING: Dict[Tuple[int, int, int], str] = {
    (255, 255, 255): '00',  # WHITE
    (0, 0, 0): '01',        # BLACK
    (255, 0, 0): '10',      # RED
    (14, 110, 184): '11'    # BLUE
}

# DNA nucleotide mappings
# 2-bit to nucleotide mapping
BINARY_TO_NUCLEOTIDE: Dict[str, str] = {
    '00': 'G',
    '01': 'C',
    '10': 'T',
    '11': 'A'
}

# 3-bit to dinucleotide mapping
THREEBITS_TO_DINUCLEOTIDE: Dict[str, str] = {
    '000': 'CA',
    '001': 'CT',
    '010': 'GA',
    '011': 'GT',
    '100': 'TC',
    '101': 'TG',
    '110': 'AC',
    '111': 'AG'
}

# Integer to nucleotide mapping
INT_TO_NUCLEOTIDE: Dict[int, str] = {
    0: 'G',
    1: 'C',
    2: 'T',
    3: 'A'
}

# Integer to dinucleotide mapping
INT_TO_DINUCLEOTIDE: Dict[int, str] = {
    0: 'CA',
    1: 'CT',
    2: 'GA',
    3: 'GT',
    4: 'TC',
    5: 'TG',
    6: 'AC',
    7: 'AG'
}


# Core Functions
# ==============

def get_mapping_value(x: int) -> Optional[str]:
    """
    Convert integer to nucleotide using mapping dictionary.
    
    Args:
        x: Integer value (0-3)
        
    Returns:
        Corresponding nucleotide character or None if not found
    """
    return INT_TO_NUCLEOTIDE.get(x, None)


def xuhao_binary(x: str) -> Optional[str]:
    """
    Convert binary string to nucleotide using mapping dictionary.
    
    Args:
        x: 2-bit binary string
        
    Returns:
        Corresponding nucleotide character or None if not found
    """
    return BINARY_TO_NUCLEOTIDE.get(x, None)


def xuhao_threebits(x: str) -> Optional[str]:
    """
    Convert 3-bit binary string to dinucleotide using mapping dictionary.
    
    Args:
        x: 3-bit binary string
        
    Returns:
        Corresponding dinucleotide pair or None if not found
    """
    return THREEBITS_TO_DINUCLEOTIDE.get(x, None)


def get_tri_mapping_value(x: int) -> Optional[str]:
    """
    Convert integer to dinucleotide using mapping dictionary.
    
    Args:
        x: Integer value (0-7)
        
    Returns:
        Corresponding dinucleotide pair or None if not found
    """
    return INT_TO_DINUCLEOTIDE.get(x, None)


def last_four_bits(input_string: str) -> Tuple[int, int]:
    """
    Split an 8-bit string into two 2-bit parts and convert to integers.
    
    Args:
        input_string: 8-bit binary string
        
    Returns:
        Tuple of two integers (first 2 bits, last 2 bits)
    """
    first_part = input_string[:2]
    second_part = input_string[2:]
    
    first_binary_number = int(first_part, 2)
    second_binary_number = int(second_part, 2)
    
    return first_binary_number, second_binary_number


def process_image(image_path: str) -> Tuple[List[List[str]], List[List[str]]]:
    """
    Process an image file and convert pixels to color codes and binary codes.
    
    Args:
        image_path: Path to the input image file
        
    Returns:
        Tuple containing:
        - pixel_matrix: Matrix of RGB color strings
        - binary_matrix: Matrix of binary color codes
        
    Raises:
        ValueError: If an unknown color is encountered in the image
        FileNotFoundError: If the image file doesn't exist
    """
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    
    pixel_matrix = []
    binary_matrix = []
    
    for y in range(height):
        pixel_row = []
        binary_row = []
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            pixel = (r, g, b)
            
            if pixel not in COLOR_ENCODING:
                raise ValueError(f"Color {pixel} not found in encoding at position ({x + 1}, {y + 1})")
            
            pixel_row.append(f"{r},{g},{b}")
            binary_row.append(COLOR_ENCODING[pixel])
        
        pixel_matrix.append(pixel_row)
        binary_matrix.append(binary_row)
    
    return pixel_matrix, binary_matrix


def split_string_into_groups(input_string: str, group_size: int = 8) -> List[str]:

    return [input_string[i:i + group_size] for i in range(0, len(input_string), group_size)]


def save_to_csv(data: List[List[Any]], filename: str) -> None:

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(data)


def convert_binary_parts(input_string: str) -> Tuple[int, int, int]:
    """
    Split an 8-bit string into three parts and convert to integers.
    
    Args:
        input_string: 8-bit binary string
        
    Returns:
        Tuple of three integers (first 2 bits, middle 3 bits, last 3 bits)
        
    Raises:
        ValueError: If input string length is not 8
    """
    if len(input_string) != 8:
        raise ValueError("Input string must have a length of 8.")
    
    first_two = input_string[:2]
    middle_three = input_string[2:5]
    last_three = input_string[5:8]
    
    first_two_decimal = int(first_two, 2) if first_two else 0
    middle_three_decimal = int(middle_three, 2) if middle_three else 0
    last_three_decimal = int(last_three, 2) if last_three else 0
    
    return first_two_decimal, middle_three_decimal, last_three_decimal


def string_to_matrix(input_string: str, row_length: int) -> List[str]:

    dna_matrix = []
    for i in range(0, len(input_string), row_length):
        dna_matrix.append(input_string[i:i + row_length])
    return dna_matrix


def split_matrix_rows(matrix: List[str], chunk_size: int) -> List[List[str]]:

    new_matrix = []
    for row in matrix:
        split_row = [row[i:i + chunk_size] for i in range(0, len(row), chunk_size)]
        new_matrix.append(split_row)
    return new_matrix


def generate_indexed_list(original_list: List[List[str]]) -> List[str]:

    indexed_list = []
    
    for row_index, row in enumerate(original_list):
        for col_index, _ in enumerate(row):
            row_number = str(row_index + 1).zfill(3)
            col_number = col_index + 1
            indexed_string = f"{row_number}{col_number}"
            indexed_list.append(indexed_string)
    
    return indexed_list


def string_to_binary(input_string: str) -> List[str]:

    binary_list = []
    
    for char in input_string:
        binary_repr = bin(int(char))[2:]
        binary_list.append(binary_repr.zfill(4))
    
    return binary_list


def prepend_characters(list1: List[str], list2: List[str]) -> List[str]:

    result = [b + a for a, b in zip(list1, list2)]
    return result


def create_matrix_from_string_list(string_list: List[str], n: int = 5) -> List[List[str]]:

    matrix = [string_list[i:i + n] for i in range(0, len(string_list), n)]
    return matrix


# Main Execution
# ==============

if __name__ == "__main__":
    input_image = "picture.png"
    
    try:
        # Process image and save pixel and binary matrices
        pixels, binaries = process_image(input_image)
        save_to_csv(pixels, "pixel_matrix.csv")
        save_to_csv(binaries, "binary_matrix.csv")
        
        print("Conversion successful!")
        print("- pixel_matrix.csv")
        print("- binary_matrix.csv")
        print("- dna_sequence.csv")
        
    except FileNotFoundError:
        print(f"Error: {input_image} not found")
        exit(1)
    except ValueError as ve:
        print(str(ve))
        exit(1)
    
    # Convert binary matrix to DNA sequence
    DNA = []
    dna = []
    
    for a in binaries:
        result = ''.join(a)
        m = split_string_into_groups(result)
        xl, yl = last_four_bits(m[87])
        d1 = get_mapping_value(xl)
        d2 = get_mapping_value(yl)
        
        for i in range(87):
            x, y, z = convert_binary_parts(m[i])
            N1 = get_mapping_value(x)
            dna.append(N1)
            N2 = get_tri_mapping_value(y)
            dna.append(N2)
            N3 = get_tri_mapping_value(z)
            dna.append(N3)
        
        dna.append(d1)
        dna.append(d2)
        DNA = ''.join(dna)
    
    # Create DNA matrix and process further
    DNA_matrix = string_to_matrix(DNA, 437)
    y = split_matrix_rows(DNA_matrix, 90)
    row_list = generate_indexed_list(y)
    
    # Process indexed list to create nucleotide sequences
    xuhao = []
    print(row_list)
    print(len(row_list))
    
    for i in range(0, len(row_list)):
        xuhao_b = []
        tmp = string_to_binary(row_list[i])
        result = ''.join(tmp)
        
        a = xuhao_binary(result[0:2])
        xuhao_b.append(a)
        b = xuhao_threebits(result[2:5])
        xuhao_b.append(b)
        c = xuhao_threebits(result[5:8])
        xuhao_b.append(c)
        d = xuhao_binary(result[8:10])
        xuhao_b.append(d)
        e = xuhao_threebits(result[10:13])
        xuhao_b.append(e)
        f = xuhao_threebits(result[13:16])
        xuhao_b.append(f)
        
        tmp_nt = ''.join(xuhao_b)
        xuhao.append(tmp_nt)
    
    # Create final DNA sequence matrix
    flattened_list = list(itertools.chain.from_iterable(y))
    final_dna = prepend_characters(flattened_list, xuhao)
    final_matrix = create_matrix_from_string_list(final_dna)
    
    # Save final DNA sequences to CSV
    with open('DNA.csv', 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(final_matrix)