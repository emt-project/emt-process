import plac
from pathlib import Path
import pandas as pd
import jinja2
import os
import shutil

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
def main(folder, metadata, output="output/", mets_template="mets_template.xml", rows=None):
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
    count_0 = 0
    for index, row in metadata_df.iterrows():
        print(row)
        print(folder_name)
        print(row["folder"])
        if folder_name != row["folder"]:
            count_0 += 1
            folder_name = row["folder"]
            if count_0 not in list(range(start_row, end_row)):
                continue
            if len(doc) > 0:
                target_path = Path(os.path.join(output, metadata_df.loc[index-1, 'folder'], 'images', f"master_EMT_{metadata_df.loc[index-1, 'folder']}_media"))
                target_path.mkdir(parents=True, exist_ok=True)
                with open(os.path.join(output, metadata_df.loc[index-1, 'folder'], "meta.xml"), "w") as file:
                    author, adressee = row["weranwen"].split(" an ")
                    print([d.values for d in doc])
                    file.write(template.render(docs=[d.values for d in doc], author=map_authors[author], adressee=map_authors[adressee], **doc[0]))
                    src_files = os.listdir(os.path.join(folder, metadata_df.loc[index-1, 'folder']))
                    for file_name in src_files:
                        print(file_name)
                        print(src_files)
                        full_file_name = os.path.join(folder, metadata_df.loc[index-1, 'folder'], file_name)
                        if os.path.isfile(full_file_name):
                            shutil.copyfile(full_file_name, os.path.join(output, metadata_df.loc[index-1, 'folder'], "images", f"master_EMT_{metadata_df.loc[index-1, 'folder']}_media", file_name))
            doc = [row]
        else:
            doc.append(row)

if __name__ == '__main__':
    import plac;
    plac.call(main)
