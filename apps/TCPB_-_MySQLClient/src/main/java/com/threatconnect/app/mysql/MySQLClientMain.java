package com.threatconnect.app.mysql;

import com.threatconnect.app.apps.App;
import com.threatconnect.app.apps.AppConfig;
import com.threatconnect.sdk.app.AppMain;

public class MySQLClientMain extends AppMain
{
	@Override
	public Class<? extends App> getAppClassToExecute(final AppConfig appConfig) throws ClassNotFoundException
	{
		return MySQLClientApp.class;
	}
	
	public static void main(String[] args)
	{
		new MySQLClientMain().execute();
	}
}
