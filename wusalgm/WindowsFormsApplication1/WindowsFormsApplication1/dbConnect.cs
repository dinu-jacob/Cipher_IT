using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Data;
using System.Data.SqlClient;

public class connection
{
    SqlConnection con = new SqlConnection();
    SqlCommand cmd = new SqlCommand();
    public connection()
    {
        con.ConnectionString = @"Data Source=GEETHIKA-PC\MSSQL;Initial Catalog=hat;Integrated Security=True";
        cmd.Connection = con;
    }
    public void openCon()
    {
        if (con.State == ConnectionState.Open)
            con.Close();
        con.Open();
    }
    public void closeCon()
    {
        con.Close();
    }
    public SqlCommand getCmd
    {
        get { return cmd; }
    }
}
public static class CRUD
{
    static connection c = new connection();
    private static void common(string spName,  object[] objValues)
    {
        c.openCon();
        c.getCmd.CommandType = CommandType.StoredProcedure;
        c.getCmd.CommandText = spName;
        c.getCmd.Parameters.Clear();
        SqlCommandBuilder.DeriveParameters(c.getCmd);
        int i = 0; int j = 0;
        foreach (SqlParameter sParam in c.getCmd.Parameters)
        {
            if (j > 0)
            {
                 sParam.Value = objValues[i];
                i++;
            }
            j++;
        }
    }
    public static void insUpDel(string spName, params object[] objValues)
    {
        common(spName, objValues);
        c.getCmd.ExecuteNonQuery();
        c.closeCon();
    }
    public static string selString(string spName, params object[] objValues)
    {
        try
        {
            common(spName, objValues);
            string s = c.getCmd.ExecuteScalar().ToString();
            c.closeCon();
            return s;
        }
        catch (Exception)
        {
            return null;
        }
    }
    public static int selInt(string spName, params object[] objValues)
    {
        common(spName, objValues);
        int n = Convert.ToInt32(c.getCmd.ExecuteScalar());
        c.closeCon();
        return n;
    }
    public static double selDouble(string spName, params object[] objValues)
    {
        common(spName, objValues);
        double d = Convert.ToDouble(c.getCmd.ExecuteScalar());
        c.closeCon();
        return d;
    }
    public static DataTable selDTable(string spName, params object[] objValues)
    {
        common(spName, objValues);
        DataTable dt = new DataTable();
        SqlDataAdapter da = new SqlDataAdapter();
        da.SelectCommand = c.getCmd;
        da.Fill(dt);
        c.closeCon();
        return dt;
    }
    public static DataSet selDSet(string spName, params object[] objValues)
    {
        common(spName, objValues);
        DataSet ds = new DataSet();
        SqlDataAdapter da = new SqlDataAdapter();
        da.SelectCommand = c.getCmd;
        da.Fill(ds);
        c.closeCon();
        return ds;
    }
}
public class _RFile : connection
{
    public byte[] selFile(string spName, params object[] objValues)
    {
        openCon();
        getCmd.CommandType = CommandType.StoredProcedure;
        getCmd.CommandText = spName;
        getCmd.Parameters.Clear();
        SqlCommandBuilder.DeriveParameters(getCmd);
        int i = 0; int j = 0;
        foreach (SqlParameter sParam in getCmd.Parameters)
        {
            if (j > 0)
            {
                sParam.Value = objValues[i];
                i++;
            }
            j++;
        }
        byte[] b = (byte[])getCmd.ExecuteScalar();
        closeCon();
        return b;
    }
}