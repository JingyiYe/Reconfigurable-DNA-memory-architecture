import numpy as np
import csv
#把DNA的测序序列填充到矩阵中
# 指定文件路径
file_path = "low_freq_5_percent.txt"
error = 0
seq_num = 0


# 打开文件并读取每一行的第一个空格之前的内容
# 打开文件并读取每一行的第一个空格之前的内容
with open(file_path, 'r') as file:
    lines = file.readlines()

# 打开文件并读取所有行
with open(file_path, 'r') as file:
    lines = file.readlines()

# 初始化筛选结果列表
filtered_sequences = []
dna_matrix =  np.empty((341, 5), dtype=object)#构建空白矩阵

for line in lines[1:]:
    # 提取第一个空格之前的内容
    first_part = line.split(maxsplit=1)[0]
    filtered_sequences.append(first_part)

def xuhao_binary(X):
    # 定义映射规则
    mapping = {
        'G':'00',
        'C':'01',
        'T':'10',
        'A':'11'
    }
    return mapping.get(X, None)

def threebits_xuhao(X):
    # 定义逆映射规则
    inverse_mapping = {
        'CA': '000',
        'CT': '001',
        'GA': '010',
        'GT': '011',
        'TC': '100',
        'TG': '101',
        'AC': '110',
        'AG': '111'
    }
    return inverse_mapping.get(X, None)


for seq in filtered_sequences:
    tmp_add = []
    a=seq[0:1]
    b=seq[1:3]
    c=seq[3:5]
    d=seq[5:6]
    e=seq[6:8]
    f=seq[8:10]
    xuhaoa=xuhao_binary(a)#0:2
    xuhaob=threebits_xuhao(b)#2:5
    xuhaoc=threebits_xuhao(c)#5:8
    xuhaod=xuhao_binary(d)#8:10
    xuhaoe=threebits_xuhao(e)#10:13
    xuhaof=threebits_xuhao(f)
    tmp_add.extend([xuhaoa,xuhaob,xuhaoc,xuhaod,xuhaoe,xuhaof])
    #print(tmp_add)

    #concatenated_str = ''.join(tmp_add)
    try:
        concatenated_str = ''.join(tmp_add)
    except TypeError as e:
        print("错误的序列是",tmp_add,seq[0:10], {e})
        error=error+1

        continue
    #print(concatenated_str)
    group_size = 4
    groups = [concatenated_str[i:i + group_size] for i in range(0, len(concatenated_str), group_size)]
    decimal_list = [int(b, 2) for b in groups]
    row=decimal_list[0]*100+decimal_list[1]*10+decimal_list[2]
    col=decimal_list[3]
    #print(row)
    try:
        if dna_matrix[row-1][col-1] == None and (len(seq) == 100 or len(seq) == 87):
            dna_matrix[row-1,col-1]=seq[10:]
    except IndexError as e:
        print("错误的序列是",seq[0:10],{e})
        error = error + 18
        continue
    seq_num=seq_num+1

print(error)
with open('matrix.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(dna_matrix)

print("矩阵已保存到 matrix.csv 文件中")

