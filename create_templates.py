import jinja2
import pandas as pd
from dateutil.parser import parse, ParserError
from datetime import date

templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template('tei_template.xml')

main_df = pd.read_csv('enriched_gesamt.csv')

for gr, df in main_df.groupby('folder'):
    file_name = f"./data/editions/{gr}.xml"
    with open(file_name, 'w') as f:
        row = df.iloc[0]
        item = {}
        item['settlement'] = "München"
        item['repositor'] = "some archive in munich"
        item['id'] = gr.lower()
        item['file_name'] = f"{gr}.xml".lower()
        item['title'] = f"{row['weranwen']}, {row['Ort']} am {row['Datum']}"
        item['sender'] = row['weranwen'].split()[0]
        item['receiver'] = row['weranwen'].split()[-1]
        item['place'] = row['Ort']
        item['writte_date'] = row['Datum']
        item['current_date'] = f"{date.today()}"
        try:
            item['parsed_date'] = parse(item['writte_date'])
        except ParserError:
            item['parsed_date'] = None
        item['pages'] = []
        for i, nrow in df.iterrows():
            p = {}
            p['width'] = nrow['width']
            p['height'] = nrow['height']
            p['url'] = f"https://iiif.acdh.oeaw.ac.at/kem/{nrow['Dateiname'].split('.')[0]}"
            item['pages'].append(p)
        f.write(template.render(**item))
    