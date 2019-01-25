import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('ActivoBot-9df24e883e77.json', self.scope)
        gc = gspread.authorize(credentials)
        # Open a worksheet from spreadsheet with one shot
        self.wks = gc.open("Dennis Copy of Seat Allocation 2019").get_worksheet(3)

    def get_all_hot_desks(self):
        all_sheet_data = self.wks.get_all_values()
        hot_desk_list = []
        for i in all_sheet_data:
            if i[4] == "Hot Desk":
                hot_desk_list.append(i)
        return hot_desk_list
