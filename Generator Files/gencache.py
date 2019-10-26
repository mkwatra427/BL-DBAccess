def generate():
    
    f = open("DBCache.java", "w")
    f.write("import java.util.HashMap;\n\n"
            "public class DBCache {\n\n"
            "  public class TableEntry extends HashMap<Object, Object> {\n\n" # inner TableEntry class
            "    private String tableName;\n\n"
            "    public HashMap<Object, Void> workingList = new HashMap<Object, Void>();\n\n"
            "    public HashMap<Object, Void> dirtyList = new HashMap<Object, Void>();\n\n"
            "    public TableEntry(String tableName) {\n"
            "      this.tableName = tableName;\n    }\n\n"
            "    public String getTableName() {\n"
            "      return this.tableName;\n    }\n\n  }\n\n")

    # HashMap of TableEntries + TableEntry retrieval methods
    f.write("  private HashMap<String, TableEntry> entries = new HashMap<String, TableEntry>();\n\n"
            "  public TableEntry getTableEntry(String tableName) {\n"
            "    return entries.get(tableName);\n  }\n\n"
            "  public void addTableEntry(String tableName) {\n"
            "    entries.put(tableName, new TableEntry(tableName));\n  }\n\n"
            "  public boolean hasTableEntry(String tableName) {\n"
            "    return getTableEntry(tableName) != null;\n  }\n\n")

    # cache flushing methods
    f.write("  public void flushTable(String tableName) {\n"
            "    entries.remove(tableName);\n  }\n\n"
            "  public void flushTable(TableEntry entry) {\n"
            "    entries.remove(entry.getTableName(), entry);\n  }\n\n"
            "  public void flushAll() {\n"
            "    entries.clear();\n  }\n\n}")

    f.close()
