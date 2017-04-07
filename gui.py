from Tkinter import *

def db_info(database):
    client = MongoClient()
    db = client[database]
    col = db.collection_names()

    doc_count = {}

    for collection in col:
        doc_count[collection] = db[collection].count()
    print(doc_count)

def startup(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=28, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

fields = ['Name',
          'Original Filename',
          'String ID',
          'Growth Media',
          'Growth Method (solid/liquid)',
          'Illicitor Name',
          'Illicitor Concentration (uM)',
          'Extraction Solvent',
          'Column Type',
          'Experiment Date',
          'Upload Date']


def fetch(entries):
    result = {}
    for entry in entries:
        field = entry[0]
        text = entry[1].get()
        print('%s: "%s"' % (field, text))

        result[field] = text

    return result

def makeform(root, fields):
   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=28, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries

if __name__ == '__main__':
   root = Tk()
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))
   b1 = Button(root, text='Enter',
          command=(lambda e=ents: fetch(e)))
   b1.pack(side=LEFT, padx=5, pady=5)
   b2 = Button(root, text='Quit', command=root.quit)
   b2.pack(side=LEFT, padx=5, pady=5)

   print(b1)
   root.mainloop()