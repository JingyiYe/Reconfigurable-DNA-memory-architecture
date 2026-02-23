import csv
import numpy as np
from PIL import Image

filename = 'matrix_tmp.csv'
error = 0

COLOR_ENCODING = {
    '00': (255, 255, 255),  # White
    '01': (0, 0, 0),        # Black
    '10': (255, 0, 0),      # Red
    '11': (14, 110, 184)    # Blue
}

COLOR_ENCODING_FOR_PICTURE = {
    (255, 255, 255): '00',  # White
    (0, 0, 0): '01',        # Black
    (255, 0, 0): '10',      # Red
    (14, 110, 184): '11'    # Blue
}

def char_to_number(char):
    """
    Convert nucleotide character to 2-bit binary code.
    
    Args:
        char: Nucleotide character (G, C, T, A)
        
    Returns:
        Corresponding 2-bit binary string or None if not found
    """
    mapping = {
        'G': '00',
        'C': '01',
        'T': '10',
        'A': '11'
    }
    return mapping.get(char.upper(), None)

def get_tri_mapping_value(X):
    """
    Convert dinucleotide to 3-bit binary code.
    
    Args:
        X: Dinucleotide string (CA, CT, GA, GT, TC, TG, AC, AG)
        
    Returns:
        Corresponding 3-bit binary string or None if not found
    """
    mapping = {
        'CA': '000',
        'CT': '001',
        'GA': '010',
        'GT': '011',
        'TC': '100',
        'TG': '101',
        'AC': '110',
        'AG': '111',
    }
    return mapping.get(X, None)

def get_mapping_value(X):
    """
    Convert nucleotide character to 2-bit binary code.
    
    Args:
        X: Nucleotide character (G, C, T, A)
        
    Returns:
        Corresponding 2-bit binary string or None if not found
    """
    mapping = {
        'G': '00',
        'C': '01',
        'T': '10',
        'A': '11'
    }
    return mapping.get(X, None)

def fill_matrix(binary_list):

    if len(binary_list) != 341:
        raise ValueError("Input list length must be 341")
    if any(len(s) != 700 for s in binary_list):
        raise ValueError("Each string in the input list must be of length 700")
    
    matrix = [[None] * 350 for _ in range(341)]

    for i in range(341):
        for j in range(350):
            index = j * 2
            binary_value = binary_list[i][index:index + 2]
            matrix[i][j] = binary_value
    return matrix

def restore_pixel_matrix(binary_matrix):
    height = len(binary_matrix)
    width = len(binary_matrix[0]) if height > 0 else 0

    pixel_matrix = []

    for y in range(height):
        pixel_row = []
        for x in range(width):
            binary_code = binary_matrix[y][x]
            if binary_code not in COLOR_ENCODING:
                raise ValueError(f"Undefined binary code {binary_code} detected at position ({x + 1}, {y + 1})")
            pixel = COLOR_ENCODING[binary_code]
            pixel_row.append(pixel)
        pixel_matrix.append(pixel_row)

    return pixel_matrix

def restore_image(pixel_matrix):
    height = len(pixel_matrix)
    width = len(pixel_matrix[0]) if height > 0 else 0
    image = Image.new('RGB', (width, height))
    
    for y in range(height):
        for x in range(width):
            image.putpixel((x, y), pixel_matrix[y][x])
    
    image.show()
    image.save("del.png")  # Save the restored image

def process_image(image_path):
    """
    Process an image file and convert to pixel and binary matrices.
    
    Args:
        image_path: Path to the input image file
        
    Returns:
        Tuple containing:
        - pixel_matrix: Matrix of RGB color strings
        - binary_matrix: Matrix of binary color codes
        
    Raises:
        ValueError: If undefined color is encountered
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

            if pixel not in COLOR_ENCODING_FOR_PICTURE:
                print(pixel)
                raise ValueError(f"Undefined color {pixel} detected at position ({x + 1}, {y + 1})")

            pixel_row.append(f"{r},{g},{b}")
            binary_row.append(COLOR_ENCODING_FOR_PICTURE[pixel])

        pixel_matrix.append(pixel_row)
        binary_matrix.append(binary_row)

    return pixel_matrix, binary_matrix

if __name__ == "__main__":
    # Read the CSV file
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)
        data_array = np.array(rows)
    print("Matrix has been read")

    binary_result = []
    
    for i in range(341):
        row_dna = data_array[i]
        row_dna = ''.join(row_dna)
        row_binary = []
        row_dna_front = row_dna[0:435]
        row_dna_5 = [row_dna_front[i:i+5] for i in range(0, len(row_dna_front), 5)]
        binary_result_tmp = []
        
        for single in row_dna_5:
            a = char_to_number(single[0])
            b = get_tri_mapping_value(single[1:3])
            c = get_tri_mapping_value(single[3:5])
            
            if a is None:
                print(f"Error: Cannot convert character {single[0]} to binary")
                error += 1
                a = '00'
            if b is None:
                print(f"Error: Cannot convert string {single[1:3]} to binary")
                error += 1
                b = '000'
            if c is None:
                print(f"Error: Cannot convert string {single[3:5]} to binary")
                error += 1
                c = '000'
            
            binary_result_tmp.append([a, b, c])
        
        every_result = ''.join(''.join(inner_list) for inner_list in binary_result_tmp)
        row_dna_4 = row_dna[435:437]
        d_t = row_dna_4[0:1]
        e_t = row_dna_4[1:2]
        d = get_mapping_value(d_t)
        e = get_mapping_value(e_t)
        every_result += d + e
        binary_result.append(every_result)
    
    matrix = fill_matrix(binary_result)
    pixel_matrix = restore_pixel_matrix(matrix)
    restore_image(pixel_matrix)
    
    '''
    # Comparison code (commented out)
    input_image = "black_white.png"
    input_image2 = "black.png"

    pixels_row, binaries = process_image(input_image)
    pixels_row2, binaries2 = process_image(input_image2)

    different_elements = np.array([[x != y for x, y in zip(row1, row2)] for row1, row2 in zip(binaries, matrix)])

    # Calculate number of different elements
    num_different_elements = np.sum(different_elements)
    rate = num_different_elements / (len(pixels_row) * len(pixels_row[0]))
    print("Error rate:", {rate})

    filename = 'matrix_shanchu.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(binaries)

    filename = 'matrix_shanchu_to_recovery.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(matrix)

    filename = 'matrix_duizhao.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(binaries2)
    '''