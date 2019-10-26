import java.sql.*;

/**
 * A class to manage data in an 'employees' table.
 * 
 * @author Mitran Kwatra for billionloans
 */
public class EmployeeDAO {
  
  /**
   * Selects an employee from the table by their ID.
   * 
   * @param id the ID or employee number of the employee to be selected
   * 
   * @return the employee having the specified ID
   * 
   * @throws SQLException if the database returns an error
   */
  public EmployeeVO select(Connection conn, int id) throws SQLException {
    
    EmployeeVO emp = new EmployeeVO();
    
    String sql = "SELECT * FROM employees WHERE employeeNumber = " + id;
    Statement st = conn.createStatement();
    st.executeQuery(sql).next();
    ResultSet rs = st.getResultSet();

    try {
      emp.setLastName(rs.getString("lastName"));
      emp.setFirstName(rs.getString("firstName"));
      emp.setJobTitle(rs.getString("jobTitle"));
      emp.setEmail(rs.getString("email"));
      emp.setOfficeCode(rs.getInt("officeCode"));
      emp.setReportsTo(rs.getInt("reportsTo"));
      emp.setEmployeeNumber(rs.getInt("employeeNumber"));
      emp.setDelflg(rs.getString("delflg").charAt(0)); // ResultSet has no getChar() method?
    } catch(SQLException e) {
      if(e.getMessage().equals("Illegal operation on empty result set."))
        return null;
      else throw e;
    }
    
    st.close();
    return emp;
    
  }
  
  /**
   * Updates an employee to have data equal to that of the input employee entry.
   * 
   * @param id the ID or employee number of the entry to be updated
   * @param emp the new employee entry
   * 
   * @throws SQLException if the database returns an error
   */
  public void update(Connection conn, int id, EmployeeVO emp) throws SQLException {
    
    /* The added if-statements in the code block below are not implemented in the generators
     * or in any other method. They are a proposed solution for a bug described in the readme */
    StringBuilder columns = new StringBuilder();
    if(emp.getLastName() != null)
      columns.append("lastName = '" + emp.getLastName());
    if(emp.getFirstName() != null)
      columns.append("', firstName = '" + emp.getFirstName());
    if(emp.getJobTitle() != null)
      columns.append("', jobTitle = '" + emp.getJobTitle());
    if(emp.getEmail() != null)
      columns.append("', email = '" + emp.getEmail());
    columns.append("', officeCode = " + emp.getOfficeCode());
    columns.append(", reportsTo = " + emp.getReportsTo());
    columns.append(", delflg = '" + emp.getDelflg() + '\'');
    
    String sql = "UPDATE employees SET " + columns.toString() + " WHERE employeeNumber = " + id;
    Statement st = conn.createStatement();
    st.executeUpdate(sql);
    st.close();
    
  }
  
  /**
   * Inserts the specified employee entry into the 'employees' table
   * 
   * @param emp the employee entry to be inserted
   * 
   * @throws SQLException if the database returns an error
   */
  public void insert(Connection conn, EmployeeVO emp) throws SQLException {
    
    StringBuilder values = new StringBuilder();
    values.append('\'' + emp.getLastName() + "', '");
    values.append(emp.getFirstName() + "', '");
    values.append(emp.getJobTitle() + "', '");
    values.append(emp.getEmail() + "', ");
    values.append(emp.getOfficeCode() + ", ");
    values.append(emp.getReportsTo() + ", ");
    values.append(emp.getEmployeeNumber() + ", '");
    values.append(emp.getDelflg() + "'");
    
    String sql = "INSERT INTO employees(lastname, firstname, jobTitle, email, officeCode, " +
      "reportsTo, employeeNumber, delflg) VALUES (" + values.toString() + ')';
    Statement st = conn.createStatement();
    st.executeUpdate(sql);
    st.close();
    
  }
  
  /**
   * Deletes the specified employee from the 'employees' table
   * 
   * @param emp the employee entry to be deleted
   * 
   * @throws SQLException if the database returns an error
   */
  public void delete(Connection conn, EmployeeVO emp) throws SQLException {
    
    String sql = "DELETE FROM employees WHERE employeeNumber = " + emp.getEmployeeNumber();
    Statement st = conn.createStatement();
    st.executeUpdate(sql);
    st.close();
    
  }
  
  /**
   * Sets the logdel flag to 'Y' for the indicated employee entry.
   * 
   * @param id the ID or employee number of the employee entry to be altered
   * 
   * @throws SQLException if the database returns an error
   */
  public void logdel(Connection conn, int id) throws SQLException {
    
    String sql = "UPDATE employees SET delflg = 'Y' WHERE employeeNumber = " + id;
    Statement st = conn.createStatement();
    st.executeUpdate(sql);
    st.close();
    
  }
      
}