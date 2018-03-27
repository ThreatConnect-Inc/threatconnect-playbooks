package com.threatconnect.app.mysql;

import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;
import com.threatconnect.app.apps.ExitStatus;
import com.threatconnect.app.playbooks.app.PlaybooksApp;
import com.threatconnect.app.playbooks.app.PlaybooksAppConfig;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.Statement;

public class MySQLClientApp extends PlaybooksApp
{
	public static final String PARAM_HOST = "host";
	public static final String PARAM_PORT = "port";
	public static final String PARAM_DATABASE = "database";
	public static final String PARAM_USERNAME = "username";
	public static final String PARAM_PASSWORD = "password";
	public static final String PARAM_COMMAND = "command";
	
	public static final String OUTPUT = "output";
	
	@Override
	protected ExitStatus execute(final PlaybooksAppConfig playbooksAppConfig) throws Exception
	{
		//read the input values
		final String host = getAppConfig().getString(PARAM_HOST);
		final Integer port = getAppConfig().getInteger(PARAM_PORT);
		final String database = getAppConfig().getString(PARAM_DATABASE);
		final String username = getAppConfig().getString(PARAM_USERNAME);
		final String password = getAppConfig().getString(PARAM_PASSWORD);
		final String command = getAppConfig().getString(PARAM_COMMAND);
		
		//build the datasource connection
		MysqlDataSource dataSource = new MysqlDataSource();
		dataSource.setUser(username);
		dataSource.setPassword(password);
		dataSource.setServerName(host);
		dataSource.setPort(port);
		dataSource.setDatabaseName(database);
		
		try (Connection conn = dataSource.getConnection())
		{
			//create a new statement and execute the command
			Statement stmt = conn.createStatement();
			ResultSet resultSet = stmt.executeQuery(command);
			
			//retrieve the result set meta data
			ResultSetMetaData resultSetMetaData = resultSet.getMetaData();
			int columnsNumber = resultSetMetaData.getColumnCount();
			
			//holds the results
			StringBuilder sb = new StringBuilder();
			
			//while there are more records
			while (resultSet.next())
			{
				//for each column
				for (int i = 1; i <= columnsNumber; i++)
				{
					if (i > 1)
					{
						sb.append(", ");
					}
					
					String columnValue = resultSet.getString(i);
					sb.append(columnValue);
				}
				sb.append("\n");
			}
			
			//write the result
			writeStringContent(OUTPUT, sb.toString());
		}
		
		return ExitStatus.Success;
	}
}
