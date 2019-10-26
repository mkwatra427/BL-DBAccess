import java.sql.SQLException;

/**
 * A class to represent an employee of a firm.
 * 
 * @author Mitran Kwatra for billionloans
 */
public class EmployeeVO {
  
  private String lastName;
  private String firstName;
  private String jobTitle;
  private String email;
  private int officeCode;
  private int reportsTo;
  private int employeeNumber;
  private char delflg = 'N';
  
  /** 
   * Returns the last name of this employee.
   * @return the last name of this employee
   */
  public String getLastName() { return this.lastName; }
  
  /** 
   * Returns the first name of this employee.
   * @return the first name of this employee
   */
  public String getFirstName() { return this.firstName; }
  
  /** 
   * Returns the job title of this employee.
   * @return the job title of this employee
   */
  public String getJobTitle() { return this.jobTitle; }
  
  /** 
   * Returns the email address of this employee.
   * @return the email address of this employee
   */
  public String getEmail() { return this.email; }
  
  /** 
   * Returns the office code of this employee.
   * @return the office code of this employee
   */
  public int getOfficeCode() { return this.officeCode; }
  
  /** 
   * Returns the ID number of whom this employee reports to.
   * @return the ID number of whom this employee reports to
   */
  public int getReportsTo() { return this.reportsTo; }
  
  /** 
   * Returns the ID number of this employee.
   * @return the ID number of this employee
   */
  public int getEmployeeNumber() { return this.employeeNumber; }
  
  /**
   * Returns the logdel flag of this employee.
   * @return the logdel flag of this employee
   */
  public char getDelflg() { return this.delflg; }
  
  /**
   * Sets the last name of this employee.
   * @param lastName the new last name of this employee
   */
  public void setLastName(String lastName) throws SQLException {
    if(lastName.length() > 50)
      throw new SQLException("lastName cannot be longer than 50 characters.");
    this.lastName = lastName; 
  }
  
  /**
   * Sets the first name of this employee.
   * @param firstName the new last name of this employee
   */
  public void setFirstName(String firstName) { this.firstName = firstName; }
  
  /**
   * Sets the job title of this employee.
   * @param jobTitle the new last name of this employee
   */
  public void setJobTitle(String jobTitle) { this.jobTitle = jobTitle; }
  
  /**
   * Sets the email address of this employee.
   * @param email address the new last name of this employee
   */
  public void setEmail(String email) { this.email = email; }
  
  /**
   * Sets the office code of this employee.
   * @param officeCode the new last name of this employee
   */
  public void setOfficeCode(int officeCode) { this.officeCode = officeCode; }
  
  /**
   * Sets the ID number of whom this employee reports to.
   * @param reportsTo the new ID number of whom this employee reports to
   */
  public void setReportsTo(int reportsTo) { this.reportsTo = reportsTo; }
  
  /**
   * Sets the ID number of this employee.
   * @param employeeNumber the new ID number of this employee
   */
  public void setEmployeeNumber(int employeeNumber) { this.employeeNumber = employeeNumber; }
  
  /**
   * Sets the logdel flag of this employee.
   * @param delflg the new logdel flag of this employee
   */
  public void setDelflg(char delflg) { this.delflg = delflg; };
  
  /**
   * Returns a String representation of this employee.
   * @return a String representation of this employee
   */
  @Override
  public String toString() {
    return "(" + getLastName() + ", " + getFirstName() + ", " + getJobTitle()
      + ", " + getEmail() + ", " + getOfficeCode() + ", " + getReportsTo()
      + ", " + getEmployeeNumber() + ", " + getDelflg() + ")";
  }
  
  /**
   * Returns true if the object is of type EmployeeVO
   *  and has the same employee number as this employee.
   * @return true if the EmployeeVOs represent the same employee
   */
  @Override
  public boolean equals(Object o) {
    if(o instanceof EmployeeVO)
      return this.getEmployeeNumber() == ((EmployeeVO)o).getEmployeeNumber();
    else return false;
  }
  
}