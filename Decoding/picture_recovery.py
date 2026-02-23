import csv
import numpy as np
#对填充的序列进行处理，主要是null和非法序列的判别
filename = 'matrix.csv'

with open(filename, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)
    data_array = np.array(rows)

#检查空值
def fill_individual_nulls_with_G(arr: np.ndarray) -> np.ndarray:
    arr_copy = arr.copy()
    error=0
    def is_empty_or_null(x):
        return x is None or (isinstance(x, str) and x.strip().lower() in ('', 'null'))

    for i in range(arr_copy.shape[0]):
        for j in range(arr_copy.shape[1]):
            if is_empty_or_null(arr_copy[i, j]):
                if j < 4:
                    arr_copy[i, j] = 'G' * 90
                    error = error+1
                elif j == 4:
                    arr_copy[i, j] = 'G' * 77
                    error = error + 1
                # 其他列保持不变

    return arr_copy,error

#检查长度
def fix_length_with_G(arr: np.ndarray) -> np.ndarray:
    arr_copy = arr.copy()
    error=0
    for i in range(arr_copy.shape[0]):
        for j in range(arr_copy.shape[1]):
            val = arr_copy[i, j]
            # 只处理前5列
            if j < 5:
                # 如果值是 None 或空字符串等，也统一处理
                if val is None or not isinstance(val, str):
                    val_str = ''  # 转成空字符串进行长度检查
                else:
                    val_str = val.strip()
                # 检查长度
                if (j < 4 and len(val_str) != 90):
                    arr_copy[i, j] = 'G' * 90
                    error=error+1
                elif (j == 4 and len(val_str) != 77):
                    arr_copy[i, j] = 'G' * 77
                    error=error+1
    return arr_copy,error



filled_data ,error_null = fill_individual_nulls_with_G(data_array)
#print(filled_data)
fixed,error_len = fix_length_with_G(filled_data)




with open('matrix_del_d2.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(fixed)

print("矩阵已保存到 matrix_recovery1_d2.csv 文件中")