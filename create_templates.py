import glob
import jinja2
import pandas as pd
from acdh_tei_pyutils.tei import TeiReader
from dateutil.parser import parse, ParserError
from datetime import date
import lxml.etree as ET


templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template('tei_template.xml')

main_df = pd.read_csv('enriched_gesamt.csv')
filtered_df = main_df[main_df['folder'].str.startswith('Kasten_blau_45_8')]

files = glob.glob('./tmp/*.xml')

for gr, df in filtered_df.groupby('folder'):
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
            f_name = f"{nrow['Dateiname'].split('.')[0]}"
            legacy_xml_name = f"./tmp/{f_name}.xml"
            p = {}
            if legacy_xml_name in files:
                print(legacy_xml_name)
                doc = TeiReader(legacy_xml_name)
                facs = doc.any_xpath('.//tei:surface')[0]
                facs_string = ET.tostring(facs, encoding='utf-8', pretty_print=True).decode('utf-8')
                body = doc.any_xpath('.//tei:div[@type="page"]')[0]
                body_string = ET.tostring(body, encoding='utf-8', pretty_print=True).decode('utf-8')
                p['facs_string'] = facs_string
                p['body_string'] = body_string
            p['width'] = nrow['width']
            p['height'] = nrow['height']
            p['url'] = f"https://iiif.acdh.oeaw.ac.at/kem/{f_name}"
            item['pages'].append(p)
        f.write(template.render(**item))
