import openpyxl
from openpyxl.utils.cell import column_index_from_string

class Unecon_Parser():
    '''
    Считывает информацию о парах
    для всех групп
    с всех рабочих листов
    одного файла.
    load_file - загрузить файл
    find_corner_cell - найти опорный угол шапки таблицы на листе
    find_start_parse - найти опорный угол тела таблицы
    for_group - выдать расписание для одной группы.
    '''
    keywords = ('день недели','пара','часы')
    corner_coords = ()

    def load_file(self, path):
        self.wb = openpyxl.load_workbook(path, read_only=False, guess_types=True)
        self.worksheets = self.wb.get_sheet_names()

    def find_corner_cell(self, ws):
        #  finding left upper table corner
        find_range = ws['A1:C20']
        for row in find_range:
            for cell in row:
                if str(cell.value).lower() == self.keywords[0]:
                    col1 = cell.column
                    row1 = cell.row
                    break
                else: continue
            try:
                if row1: break
            except NameError: continue

        self.corner_coords = (row1,column_index_from_string(col1))

    def find_parse_start(self, ws):
        #  finding where the actual data is stored
        find_range = ws['A1:C20']
        for row in find_range:
            for cell in row:
                if str(cell.value).lower() == 'понедельник':
                    col1 = cell.column
                    row1 = cell.row
                    break
                else: continue
            try:
                if row1: break
            except NameError: continue
        self.start_coords = (row1,column_index_from_string(col1))

    def set_coordinates(self, ws):
        self.find_corner_cell(ws=ws)
        self.find_parse_start(ws=ws)

        self.WEEKDAY_COL = self.corner_coords[1]
        self.CLASSNUM_COL = self.corner_coords[1]+1
        self.CLASSTIME_col = self.corner_coords[1]+2
        self.GROUPNAME_ROW = self.start_coords[0]-1
        self.PARSE_ROW = self.start_coords[0]
        self.PARSE_COL = self.start_coords[1]+4  # main blocks +=2

    def for_group(self, group_col, PARSE_ROW, ws):
        group_name = ws.cell(row=PARSE_ROW-1,column=group_col).value
        if group_name.lower() in self.keywords:
            return False
        print('РАСПИСАНИЕ для группы {}\n'.format(group_name))
        for row in ws.iter_rows(min_row=PARSE_ROW,
                                max_col=group_col,
                                max_row=200):
            name = row[group_col-1].value
            if not name: continue
            place = row[group_col-2].value
            time = row[2].value
            day = row[0].value
            print(
                '{0} \n в аудитории {1} в {2}, {3}\n'.format(
                    name, place, day, time
                )

            )

#  пример использования
FILENAME = 'fekonomiki_i_finansov_ofo_1_kurs_0_NEW.xlsx'

p = Unecon_Parser()
p.load_file(FILENAME)
for ws_name in p.worksheets:
    ws = p.wb[ws_name]
    p.set_coordinates(ws=ws)

    for group_col in range(p.PARSE_COL,400,2):
        try:
            p.for_group(group_col=group_col,PARSE_ROW=p.PARSE_ROW, ws=ws)
        except AttributeError:
            #  конец текущей таблицы
            break

#  TO DO  **********************************************
#  xls support
#  четные/нечетные недели
#  экспорт данных
