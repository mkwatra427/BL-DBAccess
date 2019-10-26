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
        
    f = open(DAOname + ".java", "w")
    f.write("import java.sql.*;\n\n"
                "public class " + DAOname + " {\n\n")

    # writing select method

    f.write("  public " + VOname + " select(Connection conn, " + keycolumntype +
            " id) throws SQLException {\n\n    " +
            VOname + " obj = new " + VOname + "();\n\n"
            '    String sql = "SELECT * FROM ' + tablename +
            " WHERE " + keycolumn[1] + ' = " + id;\n'
            "    Statement st = conn.createStatement();\n"
            "    st.executeQuery(sql).next();\n"
            "    ResultSet rs = st.getResultSet();\n\n"
            "    try {\n")

    for datatype, columnname, maxlength in columns:
        if datatype in typedict: # map to Java data type
            datatype = typedict[datatype]
        if datatype == "char": # ResultSet cannot retrieve 'char' values directly
            f.write("      obj.set" + columnname + '(rs.getString("' +
                    columnname + '").charAt(0));\n')
        else:
            f.write("      obj.set" + columnname + "(rs.get" +
                    datatype.capitalize() + '("' + columnname + '"));\n')

    f.write("    } catch(SQLException e) {\n"
            '      if(e.getMessage().equals("Illegal operation on empty result set."))\n'
            "        return null;\n"
            "      else throw e;\n"
            "    }\n\n"
            "    st.close();\n"
            "    return obj;\n\n"
            "  }\n\n")

    # writing update method

    keycolumntype = keycolumn[0]
    if keycolumntype in typedict:
        keycolumntype = typedict[keycolumntype]
    f.write("  public void update(Connection conn, " + keycolumntype +
            " id, " + VOname + " obj) throws SQLException {\n\n"
            "    StringBuilder columns = new StringBuilder();")

    columnbuilder = ""    
    for datatype, columnname, maxlength in columns: # 'quotes' for Strings, not for numbers
        if datatype in typedict:
            datatype = typedict[datatype] # map to Java
        if datatype in ["int", "double", "short", "float", "long",
                        "byte", "boolean"]:
            columnbuilder = (columnbuilder + '\n    columns.append("' +
                             columnname + ' = " + obj.get' +
                             columnname + '() + ", ");')
        else: # String, Date, etc. types need 'quotes'
            columnbuilder = (columnbuilder +  '\n    columns.append("' + 
                             columnname + ' = \'" + obj.get' +
                             columnname + '() + "\', ");')

    columnbuilder = columnbuilder.rstrip(' ");').rstrip(",")
    columnbuilder = columnbuilder +  '");\n\n'
    f.write(columnbuilder)
    f.write('    String sql = "UPDATE ' + tablename +
            ' SET " + columns.toString() + " WHERE ' +
            keycolumn[1] + ' = " + id;\n'
            "    Statement st = conn.createStatement();\n"
            "    st.executeUpdate(sql);\n"
            "    st.close();\n\n"
            "  }\n\n")

    # writing insert method

    f.write("  public void insert(Connection conn, " + VOname + " obj) throws SQLException {\n\n"
                "    StringBuilder values = new StringBuilder();")

    valuebuilder = ""
    fieldbuilder = ""
    for datatype, columnname, maxlength in columns: # 'quotes' for Strings, not for numbers
        if datatype in typedict:
            datatype = typedict[datatype] # map to Java
        if datatype in ["int", "double", "short", "float", "long",
                        "byte", "boolean"]:
           valuebuilder = (valuebuilder + "\n    values.append(obj.get" +
                           columnname + '() + ", ");')
        else: # String types need quotes
            valuebuilder = (valuebuilder + '\n    values.append("\'" + obj.get' +
                            columnname + '() + "\', ");')
        fieldbuilder = fieldbuilder + columnname + ", "

    valuebuilder = valuebuilder.rstrip(' ");').rstrip(",")
    valuebuilder = valuebuilder + '");\n\n'
    f.write(valuebuilder)
    f.write('    String sql = "INSERT INTO ' + tablename + "(" +
            fieldbuilder.rstrip(", ") + ') VALUES (" + values.toString() + ")";\n'
            "    Statement st = conn.createStatement();\n"
            "    st.executeUpdate(sql);\n"
            "    st.close();\n\n"
            "  }\n\n")

    # writing delete method

    f.write("  public void delete(Connection conn, " + VOname + " obj) throws SQLException {\n\n"
            '    String sql = "DELETE FROM ' + tablename +
            " WHERE " + keycolumn[1] + ' = " + obj.get' +
            keycolumn[1] + "();\n"
            "    Statement st = conn.createStatement();\n"
            "    st.executeUpdate(sql);\n"
            "    st.close();\n\n"
            "  }\n\n")

    # writing logdel method

    f.write("  public void logdel(Connection conn, " + keycolumntype + " id) throws SQLException {\n\n"
            '    String sql = "UPDATE ' + tablename + " SET delflg = 'Y' WHERE " +
            keycolumn[1] + ' = " + id;\n'
            "    Statement st = conn.createStatement();\n"
            "    st.executeUpdate(sql);\n"
            "    st.close();\n\n"
            "  }\n\n")

    f.write("}")
    f.close()
