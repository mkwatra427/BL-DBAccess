import java.sql.Connection;
import java.sql.SQLException;
import javax.sql.DataSource;
import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;

/**
 * A class to connect to a database using a DataSource object.
 * 
 * @author Mitran Kwatra for billionloans
 */
public class DBConnect2 {
  
  /**
   * Returns a DataSource object for a database.
   * 
   * @return a DataSource object for a database
   * 
   * @throws SQLException if the database returns an error
   */
  public static DataSource getDataSource() throws SQLException {
    MysqlDataSource ds =  new MysqlDataSource();
    ds.setUrl("jdbc:mysql://localhost:3306/classicmodels");
    return ds;
  }
  
  /**
   * Returns a connection to a database, using a connection pool if available.
   * 
   * @return a connection to a database
   * 
   * @throws SQLException if the database returns an error
   */
  public static Connection getConnection() throws SQLException {
    return getDataSource().getConnection("root", "kabir");
  }
  
  /**
   * Returns an object to handle data from the 'employees' table.
   * 
   * @return an EmployeeDAO
   * 
   * @throws SQLException if the database returns an error
   */
  public static EmployeeDAO getEmployeeDAO() throws SQLException {
    return new EmployeeDAO(/*getConnection()*/);
  }
  
  /**
   * Returns an object to handle data from the 'tasks' table.
   * 
   * @return a TaskDAO
   * 
   * @throws SQLException if the database returns an error
   */
  public static TaskDAO getTaskDAO() throws SQLException {
    return new TaskDAO(getConnection());
  }
  
}