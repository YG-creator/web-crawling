# ‪load

from openpyxl import load_workbook

read_xlsx = load_workbook(r'C:\Users\YG\Desktop\test\2021-3-30  20시 53분 52초 merging.xlsx')
read_sheet = read_xlsx.active

name_col = read_sheet['E']
names = []
for cell in name_col :
    names.append(cell.value)

print(names)

