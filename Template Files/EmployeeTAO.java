import java.sql.Connection;
import java.sql.SQLException;

public class EmployeeTAO {
  
  private EmployeeDAO dbSource;
  
  private DBCache cache;
  
  public EmployeeTAO(EmployeeDAO dbSource, DBCache cache) {
    this.dbSource = dbSource;
    this.cache = cache;
    if(!cache.hasTableEntry("employees"))
      cache.addTableEntry("employees");
  }
  
  public EmployeeTAO(DBCache cache) {
    this(new EmployeeDAO(), cache);
  }
  
  public EmployeeVO select(Connection conn, int id) throws SQLException {
        
    validate();
    DBCache.TableEntry tableEntry = getTableEntry();
    
    EmployeeVO vo = (EmployeeVO)tableEntry.get(id);
    if(vo != null) {
      System.out.println("From cache");
      return vo;
    } else {
      System.out.println("From database");
      vo = dbSource.select(conn, id);
      if(vo != null)
        tableEntry.put(id, vo);
      return vo;
    }
    
  }
  
  public void update(Connection conn, int id, EmployeeVO obj) throws SQLException {
    validate();
    DBCache.TableEntry table = getTableEntry();
    try {
      table.workingList.put(id, null);
      dbSource.update(conn, id, obj);
      table.put(id, dbSource.select(conn, id)); // gets updated value from db
    } catch(SQLException e) {
      table.dirtyList.put(id, null);
      throw e;
    }
    table.workingList.clear(); // if update succeeds
  }
  
  public void insert(Connection conn, EmployeeVO obj) throws SQLException {
    validate();
    dbSource.insert(conn, obj);
  }
  
  public void delete(Connection conn, EmployeeVO obj) throws SQLException {
    validate();
    DBCache.TableEntry table = getTableEntry();
    int id = obj.getEmployeeNumber();
    try {
      table.workingList.put(id, null);
      dbSource.delete(conn, obj);
    } catch(SQLException e) {
      table.dirtyList.put(id, null);
      throw e;
    }
    table.remove(id);
    table.workingList.clear();
  }
  
  public void logdel(Connection conn, int id) throws SQLException {
    validate();
    DBCache.TableEntry table = getTableEntry();
    try {
      table.workingList.put(id, null);
      dbSource.logdel(conn, id);
      table.put(id, dbSource.select(conn, id)); // gets updated value form db
    } catch(SQLException e) {
      table.dirtyList.put(id, null);
      throw e;
    }
    table.workingList.clear(); // if update succeeds
  }
  
  public DBCache.TableEntry getTableEntry() {
    return cache.getTableEntry("employees");
  }
    
  public boolean isValid() {
    return cache.hasTableEntry("employees");
  }
  
  public void validate() throws SQLException {
    if(!isValid())
      throw new SQLException("Table entry no longer exists in cache");
  }
  
}