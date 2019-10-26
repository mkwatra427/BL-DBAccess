def generate():

    f = open("DBConnect.java", "w")
    f.write("import java.sql.Connection;\n"
            "import java.sql.SQLException;\n"
            "import javax.sql.DataSource;\n"
            "import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;\n\n"
            "public class DBConnect {\n\n"
            "  public static DataSource getDataSource() throws SQLException {\n"
            "    MysqlDataSource ds =  new MysqlDataSource();\n"
            '    ds.setUrl("jdbc:mysql://localhost:3306/classicmodels");\n' # database, address info hard-coded
            "    return ds;\n"
            "  }\n\n"
            "  public static Connection getConnection() throws SQLException {\n"
            '    return getDataSource().getConnection("root", "kabir");\n' # login credentials hard-coded
            "  }\n\n}")                     # username ^       ^ password
    f.close()
