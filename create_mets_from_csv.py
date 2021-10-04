import plac
from pathlib import Path
import pandas as pd
import jinja2
import os

map_authors = {
    "EMT": {
        "firstName": "Eleonore Magdalena Theresia von",
        "lastName": "Pfalz-Neuburg",
        "displayName": "Eleonore Magdalena Theresia von Pfalz-Neuburg"
    },
    "JW": {
        "firstName": "Johann Wilhelm Joseph Janaz von der",
        "lastName": "Pfalz",
        "displayName": "Johann Wilhelm von der Pfalz"
    },
    "PW": {
        "firstName": "Philipp Wilhelm von der",
        "lastName": "Pfalz",
        "displayName": "Philipp Wilhelm von der Pfalz"
    },


}

@plac.pos("folder", "Folder containing the images", type=Path)
@plac.pos("metadata", "CSV file containing the Metadata", type=Path)
@plac.opt("output_dir", "folder for the output METS files", type=Path)
@plac.opt("mets_template", "Path to METS template relative to current directory", type=Path)
@plac.opt("rows", "Rows to process from CSV (eg 20-30) -> str")
def main(folder, metadata, output="output/", mets_template="mets_template.xml", rows=False):
    metadata_df = pd.read_csv(metadata)
    templateLoader = jinja2.FileSystemLoader(searchpath=".")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(str(mets_template))
    if rows:
        rows = rows.split("-") 
        start_row, end_row = (int(rows[0].strip()), int(rows[1].strip()))
    else:
        start_row = 0
        end_row = metadata_df.shape[0]
    folder_name = None
    doc = []
    for index, row in metadata_df[start_row:end_row].iterrows():
        print(row)
        print(folder_name)
        print(row["folder"])
        if folder_name != row["folder"]:
            folder_name = row["folder"]
            if len(doc) > 0:
                with open(os.path.join(output, f"{row['folder']}_mets.xml"), "w") as file:
                    author, adressee = row["weranwen"].split(" an ")
                    print([d.values for d in doc])
                    file.write(template.render(docs=[d.values for d in doc], author=map_authors[author], adressee=map_authors[adressee], **doc[0]))
            doc = [row]
        else:
            doc.append(row)

if __name__ == '__main__':
    import plac;
    plac.call(main)
