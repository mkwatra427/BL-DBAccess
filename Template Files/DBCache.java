import java.util.HashMap;

public class DBCache {
  
  public class TableEntry extends HashMap<Object, Object> {
    
    private String tableName;
    
    public HashMap<Object, Void> workingList = new HashMap<Object, Void>();
    
    public HashMap<Object, Void> dirtyList = new HashMap<Object, Void>();
    
    public TableEntry(String tableName) {
      this.tableName = tableName;
    }
    
    public String getTableName() {
      return this.tableName;
    }
        
  }
  
  public HashMap<String, TableEntry> entries = new HashMap<String, TableEntry>();
  
  public TableEntry getTableEntry(String tableName) {
    return entries.get(tableName);
  }
  
  public void addTableEntry(String tableName) {
    entries.put(tableName, new TableEntry(tableName));
  }
  
  public boolean hasTableEntry(String tableName) {
    return getTableEntry(tableName) != null;
  }
    
  public void flushTable(String tableName) {
    entries.remove(tableName);
  }
  
  public void flushTable(TableEntry entry) {
    entries.remove(entry.getTableName(), entry);
  }
  
  public void flushAll() {
    entries.clear();
  }
    
}