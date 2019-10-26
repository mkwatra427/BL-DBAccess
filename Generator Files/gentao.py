def generate(tablename, keycolumn):

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
    TAOname = tablename.capitalize().rstrip("s") + "TAO"
    
    
    keycolumntype = keycolumn[0] # keycolumn: (<type>, <name>)
    if keycolumntype in typedict:
        keycolumntype = typedict[keycolumntype] # map to Java data type

    f = open(TAOname + ".java", "w")
    f.write("import java.sql.Connection;\nimport java.sql.SQLException;\n\n"
            "public class " + TAOname + " {\n\n"
            "  private " + DAOname + " dbSource;\n"
            "  private DBCache cache;\n\n"
            "  public " + TAOname + "(" + DAOname + " dbSource, DBCache cache) {\n"
            "    this.dbSource = dbSource;\n"
            "    this.cache = cache;\n"
            '    if(cache.getTableEntry("' + tablename + '") == null)\n'
            '      cache.addTableEntry("' + tablename + '");\n  }\n\n'
            "  public " + TAOname + "(DBCache cache) {\n"
            "    this(new " + DAOname + "(), cache);\n  }\n\n")

    # writing select method

    f.write("  public " + VOname + " select(Connection conn, " + keycolumntype + " id) "
            "throws SQLException {\n\n"
            "    validate();\n"
            "    DBCache.TableEntry tableEntry = getTableEntry();\n\n    " +
            VOname + " vo = (" + VOname + ")tableEntry.get(id);\n"
            "    if(vo != null)\n"
            "      return vo;\n"
            "    else {\n"
            "      vo = dbSource.select(conn, id);\n"
            "      if(vo != null)\n"
            "        tableEntry.put(id, vo);\n"
            "      return vo;\n    }\n\n  }\n\n")

    # writing update method

    f.write("  public void update(Connection conn, " + keycolumntype + " id, " +
            VOname + " obj) throws SQLException {\n"
            "    validate();\n"
            "    DBCache.TableEntry table = getTableEntry();\n"
            "    try {\n"
            "      table.workingList.put(id, null);\n"
            "      dbSource.update(conn, id, obj);\n"
            "      table.put(id, dbSource.select(conn, id));\n"
            "    } catch(SQLException e) {\n"
            "      table.dirtyList.put(id, null);\n"
            "      throw e;\n    }\n"
            "    table.workingList.clear();\n  }\n\n")

    # writing insert method

    f.write("  public void insert(Connection conn, " + VOname +
            " obj) throws SQLException {\n"
            "    validate();\n"
            "    dbSource.insert(conn, obj);\n  }\n\n")

    # writing delete method

    f.write("  public void delete(Connection conn, " + VOname +
            " obj) throws SQLException {\n"
            "    validate();\n"
            "    DBCache.TableEntry table = getTableEntry();\n    " +
            keycolumntype + " id = obj.get" + keycolumn[1] + "();\n"
            "    try {\n"
            "      table.workingList.put(id, null);\n"
            "      dbSource.delete(conn, obj);\n"          
            "    } catch(SQLException e) {\n"
            "      table.dirtyList.put(id, null);\n"
            "      throw e;\n    }\n"
            "    table.remove(id);\n"
            "    table.workingList.clear();\n  }\n\n")

    # writing logdel method

    f.write("  public void logdel(Connection conn, " + keycolumntype +
            " id) throws SQLException {\n"
            "    validate();\n"
            "    DBCache.TableEntry table = getTableEntry();\n"
            "    try {\n"
            "      table.workingList.put(id, null);\n"
            "      dbSource.logdel(conn, id);\n"
            "      table.put(id, dbSource.select(conn, id));\n"
            "    } catch(SQLException e) {\n"
            "      table.dirtyList.put(id, null);\n"
            "      throw e;\n    }\n"
            "    table.workingList.clear();\n  }\n\n")

    # writing getTableEntry method

    f.write("  public DBCache.TableEntry getTableEntry() {\n"
            '    return cache.getTableEntry("' + tablename + '");\n  }\n\n')

    # writing validation methods

    f.write("  public boolean isValid() {\n"
            '    return cache.hasTableEntry("' + tablename + '");\n  }\n\n'
            "  public void validate() throws SQLException {\n"
            "    if(!isValid())\n"
            '      throw new SQLException("Table entry no longer exists in cache");\n  }\n\n')
    
    f.write("}")
    f.close()
            
