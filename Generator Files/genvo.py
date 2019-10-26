def generate(tablename, columns, keycolumn):

    # used to map SQL data types to Java data types
    typedict = {"varchar": "String", "tinytext": "String",
                "text": "String", "blob": "String",
                "mediumtext": "String", "mediumblob": "String",
                "longtext": "String", "longblob": "String",
                "tinyint": "byte", "smallint": "short",
                "mediumint": "int", "bigint": "long",
                "decimal": "double", "date": "java.sql.Date",
                "datetime": "java.sql.TimeStamp", "timestamp": "java.sql.TimeStamp",
                "time": "java.sql.Time" }                         

    VOname = tablename.capitalize().rstrip("s") + "VO"
    DAOname = tablename.capitalize().rstrip("s") + "DAO"
    
    keycolumntype = keycolumn[0] # keycolumn: (<type>, <name>)
    if keycolumntype in typedict:
        keycolumntype = typedict[keycolumntype] # map to Java data type

    f = open(VOname + ".java", "w")
    f.write("import java.sql.SQLException;\n\n"
            "public class " + VOname + " {\n\n")

    tostring = "  @Override\n  public String toString() {\n    return "
    for datatype, columnname, maxlength in columns:
        if datatype in typedict:
            datatype = typedict[datatype] # map to Java
        f.write("  private " + datatype + " " + columnname + ";\n\n") # field
        f.write("  public " + datatype + " get" + columnname +        # getter
                "() {\n    return this." + columnname + ";\n  }\n\n")
        if datatype == "String":
            f.write("  public void set" + columnname + "(" + # setter, String - account for length limit
                    datatype + " " + columnname + ") throws SQLException {\n" +
                    "    if(" + columnname + " != null && " +
                    columnname + ".length() > " + str(maxlength) + ")\n" +
                    '      throw new SQLException("' + columnname + " cannot be longer than " +
                    str(maxlength) + ' characters.");\n' +
                    "    else this." +
                    columnname + " = " + columnname + ";\n  }\n\n")
        else: # setter, number
            f.write("  public void set" + columnname + "(" +
                    datatype + " " + columnname + ") {\n" +
                    "    this." + columnname + " = " + columnname + ";\n  }\n\n")
        tostring = tostring + '"' + columnname + ': " + get' + columnname + "() + '\\n' + "

    tostring = tostring.rstrip("n\+' ")
    f.write(tostring + ";\n  }\n\n")
    f.write("  @Override\n  public boolean equals(Object o) {\n"
            "    if(o instanceof " + VOname + ")\n")
    
    if keycolumntype in ["String", "java.sql.Date",
                         "java.sql.TimeStamp", "java.sql.Time"]:
        f.write("      return this.get" + keycolumn[1] + "().equals(")
    else: # String types use .equals(), primitive types use ==
        f.write("      return this.get" + keycolumn[1] + "() == (")
        
    f.write("((" + VOname + ")o).get" + keycolumn[1] + "());\n"
            "    else return false;\n  }\n\n}")
    f.close()
