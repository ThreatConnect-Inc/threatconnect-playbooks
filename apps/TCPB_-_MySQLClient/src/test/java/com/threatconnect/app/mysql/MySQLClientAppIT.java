package com.threatconnect.app.mysql;

import com.threatconnect.app.addons.util.config.install.StandardPlaybookType;
import com.threatconnect.apps.playbooks.test.config.PlaybooksTestConfiguration;
import com.threatconnect.apps.playbooks.test.orc.PlaybooksOrchestrationBuilder;
import org.junit.Before;
import org.junit.Test;

public class MySQLClientAppIT
{
	@Before
	public void init()
	{
		PlaybooksTestConfiguration.getInstance().registerEmbeddedDBService();
	}
	
	@Test
	public void runTest()
	{
		//@formatter:off
		// create a new playbooks orchestration builder for defining our runtime
		PlaybooksOrchestrationBuilder
		  .runApp(MySQLClientApp.class)
			 .withAppParam()
				.set(MySQLClientApp.PARAM_COMMAND, "SELECT NOW();")
			 .then()
			 .onSuccess().assertOutput()
				.assertNotNull(MySQLClientApp.OUTPUT, StandardPlaybookType.String)
			 .then()
		  //execute the apps
		  .build().run();
		//@formatter:on
	}
}
