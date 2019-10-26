from specclass import TableSpec

offices = TableSpec(tablename = "offices",
                    columns = [("varchar", "officeCode", 10), ("varchar", "city", 50),
                               ("varchar", "phone", 50), ("varchar", "addressLine1", 50),
                               ("varchar", "addressLine2", 50), ("varchar", "state", 50),
                               ("varchar", "country", 50), ("varchar", "postalCode", 15),
                               ("varchar", "territory", 10), ("char", "delflg", 1)],
                    keycolumn = ("varchar", "officeCode"))

employees = TableSpec(tablename = "employees",
                      columns = [("varchar", "lastName", 50), ("varchar", "firstName", 50),
                                 ("varchar", "jobTitle", 50), ("varchar", "email", 100),
                                 ("int", "officeCode", None), ("int", "reportsTo", None),
                                 ("int", "employeeNumber", None), ("char", "delflg", 1)],
                      keycolumn = ("int", "employeeNumber"))

tables = [offices, employees]
