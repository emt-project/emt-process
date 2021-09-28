# emt-process

## enrich.py

writes image size into dataframe, merges the result with `gesamt_liste.csv` and saves results as `enriched_gesamt.csv`

## `Kasten_blau_45_8.xml`

holds Transkribus-TEI-Export

## create_tempates.py

parses `enriched_gesamt.csv` and saves an XML/TEI Document for each letter into `data/editions`
be aware to apply `split.xsl` to `Kasten_blau_45_8.xml` previously

