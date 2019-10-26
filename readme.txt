--------------------------------
Python generator files
--------------------------------

 - master.py is the script file that the user runs to generate the Java files.
 	- It calls the appropriate methods from the other classes
 - All other files only define functions and running them produces nothing.
	- gencache generates the DBCache class, which acts as a data cache alongside the TAO class
	- gendbc generates the DBConnect class for obtaining a Connection to a database.
		- It contains hardcoded info: the URL and login credentials of the database to be used
	- genvo generates a value object (VO) class, one per table
	- gendao generates a data access object (DAO) class, one per table
		- Contains select, update, etc. methods
	- gentao generates a table access object (TAO) class, one per table
		- Contains select, update, etc. methods, and makes use of the DAO class
			in conjunction with the DBCache cache class

	- specclass contains a class TableSpec that defines the format of the spec file used for the generator files
		- A TableSpec object has 3 attributes:
			- tablename: - A String that is the name of the table
			- columns: - A list of tuples, each tuple representing a column in the table
				   - Each tuple has 3 attributes: - A String that is the SQL data type of the column
								  - A String that is the name of the column
								  - An int that is the maximum length of the column
									- Can be None, or anything for number/non-varchar, non-char types
			- keycolumn - A tuple that represents the primary key column of the table
				    - Has 2 values: - A String that is the SQL data type of the key column
						    - A String that is the name of the key column

	- dbspec is the spec file
		- Contains a list of TableSpec objects, each representing a table
		- The list is stored in a variable named 'table', and is accessed by the master.py script
		- the user can either rewrite the spec in this file as per their requirements, or
			write a new spec file that contains a list (named 'tables') of TableSpec objects
			and replace 'dbspec' in the master.py script with the name of the spec file

--------------------------------

 - Known issue: - With insert, update methods in the DAO class (which are used by the TAO class)
		- If a String value in the input VO is null, the method writes to the database
			 a varchar value of "null" rather than a null value
			- Can be rectified by adding an if-statement that checks for null values before writing
				to the SQL statement
				- This if-statement would be in the Java DAO class, not the gendao.py file
			- In gendao.py, the code that writes the insert and update methods contains a loop
				 that iterates through the table's columns, and writes the appropriate method calls
				 to the insert/update method of the DAO class
				- This loop must be changed to write an "if(getcolumnname() != null)" statement before
					writing each method call
		- Similarly, empty primitive values are written as 0, because Java has no way to store these as null
			- Could be rectified by using wrapper classes (Integer, Character)instead of primitives (int, char)
				and implementing the above if-not-null statement

--------------------------------
DBTester.java
--------------------------------

 - Tests the select, update, etc. methods of a TAO class, the flush methods of DBCache,
	and the validation methods of a TAO class
 - Hardcoded to test the OfficeTAO class as per the current version of the dbspec.py spec file
 - Performs operations on the 'offices' table of a database and prints the results to the screen

--------------------------------
Generated Java files
--------------------------------

 - DBCache: - A cache used by the TAO class
	    - Contains a HashMap of TableEntrys, with the name of the table as the key
		  - TableEntry: - a class to represent an entry of cached VOs from a particular table
				- Extends a HashMap<Object, Object>
					- The two contained values represent a primary key and
						a corresponding cached VO respectively
				- Contains two HashMaps - workingList and dirtyList
					- These have not been tested fully
	    - Contains getTableEntry, hasTableEntry, addTableEntry, flushTable, and flushAll methods
		  - getTableEntry and related methods take a String input that is the name of the table represented by the TableEntry

 - DBConnect: - Has methods to return a DataSource and a Connection object connected to a database
	      - Currently hardcoded with some database URL and login credentials

 - <table>VO:   - One generated per table
		- Represents a row/entry in a table
		- Contains private fields corresponding to the columns in the appropriate table
		- Contains public getters and setters for every field
			- Setters enforce the maximum length for varchar/String fields (as per the spec)
		- Contains toString and equals methods
			- .equals() checks whether the primary key (as per the spec) is the same for both VOs

 - <table>DAO:  - One generated per table
		- Contains select, insert, update, delete, and logdel methods
		- Each method takes a Connection object parameter that is connected to the appropriate database
		- The select and logdel methods also take the primary key parameter
		- The insert and delete methods take a corresponding VO type as a parameter
		- The update method takes both a primary key and a VO type (of the updated entry)

 - <table>TAO:  - One generated per table
		- Maintains access to a cache for the data
		- Also maintains a DAO object for accessing a database
		- Constructor takes a DBCache object, and either creates an appropriate TableEntry in the cache
			if it does not already exist
		- Contains select, insert, update, delete, and logdel methods
			- The select method selects from the cache if it contains the entry, and
				from the database (via the DAO object) if not
			- All methods except insert update the cache as necessary
		- Also contains: - getTableEntry method, for getting the corresponding TableEntry from the cache
				 - isValid method, for checking if this TAO's cache still holds an appropriate TableEntry
				 - If not, this TAO cannot be used, and a new TAO must be used
				 - Alternatively, a new ccorresponding TableEntry may be added to tha cache,
					making this TAO usable again
			 	 - validate method, called at the start of select, insert, update, delete, and logdel
					- If this TAO is no longer valid, throws an SQLException, hence terminating
						the select, insert, or other method from within which it is called

--------------------------------
Template Java files
--------------------------------

 - These are equivalents of the generated Java files, on a sample table "employees"
 - They have functionality almost equivalent to the generated files,
	but only used for testing and for designing the generators
 - Older template files hava JavaDoc comments to generate documentation for them
	- This documentation is likely no longer accurate

--------------------------------