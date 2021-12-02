#!/usr/bin/env python
# coding: utf-8

#Чтение fasta файлов
def fasta_to_seq(link):
    with open(link) as file:
        lines = file.readlines() #прочитали строчки и запомнили
    seq = ''
    lines = lines[1:]
    for i in range (len(lines)):
        if lines[i].isalpha() and lines[i].isupper(): #проверяем, что то, что мы добавляем - английская заглавная буква
            seq = seq + lines[i]
    return seq

seq1 = fasta_to_seq('1.fasta') 
seq2 = fasta_to_seq('2.fasta') 

match = 2 
mismatch = -2 
gap = -1 

alignment1 = '' 
alignment2 = ''

M = [[0 for _ in range(len(seq1) + 1)] for _ in range(len(seq2) + 1)] #задали матрицу со строчкой для пропусков

print('Последовательность 1:', seq1)
print('Последовательность 2:', seq2)

for i in range (1, len(seq2)+1):
    M[i][0] = M[(i-1)][0] + gap
for j in range (1, len(seq1)+1):
    M[0][j] = M[0][(j-1)] + gap

#заполним табличку
for i in range (1, len(seq2)+1):
    for j in range (1, len(seq1)+1):
        m_ver = M[i-1][j] + gap #приходим сверху - значение ячейки откуда пришли + гэп
        m_hor = M[i][j-1] + gap #приходим слева - значение ячейки откуда пришли + гэп      
        if seq2[i-1] == seq1[j-1]:
            m_dia = M[i-1][j-1] + match #диагональ если значения элементов равны
        else:
            m_dia = M[i-1][j-1] + mismatch #диагональ если значения элементов равны
            
        M[i][j] = max(m_ver, m_hor, m_dia) #заполним ячейку максимальным из трёх значений

n = len(seq1) #счётчик шагов от длины строки до нуля
m = len(seq2)

while m != 0 or n != 0: 
    score = M[m][n] 
    score_ver = M[m-1][n]
    score_hor = M[m][n-1]
    score_dia = M[m-1][n-1]
    if score == score_dia + match and seq1[n - 1] == seq2[m - 1]:  
        alignment1 = alignment1 + seq1[n-1]                                
        alignment2 = alignment2 + seq2[m-1]
        m = m - 1
        n = n - 1
    elif score == score_ver + gap:
        alignment1 = alignment1 + '_'
        alignment2 = alignment2 + seq2[m-1] 
        m = m-1
    elif score == score_hor + gap: 
        alignment1 = alignment1 + seq1[n-1]
        alignment2 = alignment2 + '_'
        n = n-1
    elif score == score_dia + mismatch and seq1[n - 1] != seq2[m - 1]:
        alignment1 = alignment1 + seq1[n - 1]
        alignment2 = alignment2 + seq2[m - 1]
        m = m - 1
        n = n - 1
        
print('Итоговое выравнивание:')
print(alignment1[::-1]) #пишем в обратную сторону так как мы добавляли каждый новый символ в конец
print(alignment2[::-1])

