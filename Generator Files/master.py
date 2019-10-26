import dbspec, genvo, gendao, gentao, gencache, gendbc
# dbspec is the sample spec.py file used, replace with the name of the spec file being used

for table in dbspec.tables:
    genvo.generate(table.tablename, table.columns, table.keycolumn)
    gendao.generate(table.tablename, table.columns, table.keycolumn)
    gentao.generate(table.tablename, table.keycolumn)
    
gencache.generate()
gendbc.generate()
