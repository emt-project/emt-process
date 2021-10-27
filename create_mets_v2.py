import os
import shutil
import glob
import pandas as pd
import jinja2
from datetime import date
from pathlib import Path
from author_map import AUTHOR_MAP as map_authors

templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template('mets_template.xml')
output = "/mnt/acdh_resources/container/R_emt_19536/094_metadata_mets"
path_orig = "/mnt/acdh_resources/container/R_emt_19536/Korrespondenz Eleonore Magdalena"
files = glob.glob(f"{path_orig}/*/*.jpg")
main_df = pd.read_csv('enriched_gesamt.csv')

current_date = f"{date.today()}"
for gr, df in main_df.dropna(subset=['folder']).groupby('folder'):
    row = df.iloc[0]
    if "Kasten_blau_45_15_" in row['folder']:
        target_path = Path(
            os.path.join(
                output, row['folder'], 'images', f"EMT_{row['folder']}_master"
            )
        )
        target_path.mkdir(parents=True, exist_ok=True)
        try:
            if " an " in row['weranwen']:
                try:
                    author, adressee = row["weranwen"].split(" an ")
                except AttributeError:
                    author, adressee = 'NN', 'NN'
            else:
                author, adressee = 'NN', 'NN'
        except:
            author, adressee = 'NN', 'NN'
        docs = []
        with open(os.path.join(output, row['folder'], "meta.xml"), "w") as file:
            for i, cur_row in df.iterrows():
                cur_file_name = cur_row['Dateiname']
                docs.append(dict(cur_row))
                source_file = [x for x in files if x.endswith(cur_file_name)][0]
                target_file = os.path.join(target_path, cur_file_name)
                print(f"copy {source_file} to {target_file}")
                shutil.copyfile(source_file, target_file)
                try:
                    author_lk = map_authors[author]
                except KeyError:
                    author = "NN"
                try:
                    addr_lk = map_authors[adressee]
                except KeyError:
                    adressee = "NN"
            file.write(
                template.render(
                    docs=[d for d in docs],
                    author=map_authors[author],
                    adressee=map_authors[adressee],
                    current_date=current_date,
                    **dict(row)
                )
            )
