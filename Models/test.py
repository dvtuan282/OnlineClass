import pandas as pd


class CauHoi:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def show(self):
        print(f"ID: {self.id}")
        print(f"Title: {self.title}")
        print()


class CauTraLoi:
    def __init__(self, id, title, is_croo):
        self.id = id
        self.title = title
        self.is_croo = is_croo

    def show(self):
        print(f"ID: {self.id}")
        print(f"Title: {self.title}")
        print(f"Is Croo: {self.is_croo}")
        print()


df = pd.read_excel("C:\\Users\dvtua\Downloads\đềđề.xlsx")
lsTL = []
lsH = []
idH = 0
idT = 0
for index, row in df.iterrows():
    idH += 1
    cauHoi = CauHoi(id=idH, title=row["Câu hỏi"])
    lsH.append(cauHoi)
    for columnName, value in row.items():
        if columnName.startswicolth("Đáp án"):
            is_croo = 1 if columnName == "Đáp án đúng" else 0
            idT += 1
            cauTraLoi = CauTraLoi(id=idT, title=value, is_croo=is_croo)
            lsTL.append(cauTraLoi)


# for h in lsH:
#     print(h.show())

for j in lsTL:
    print(j.show())
