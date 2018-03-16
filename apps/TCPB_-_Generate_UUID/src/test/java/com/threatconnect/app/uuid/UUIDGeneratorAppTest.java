package com.threatconnect.app.uuid;

import com.threatconnect.app.addons.util.config.install.StandardPlaybookType;
import com.threatconnect.app.apps.AppConfig;
import com.threatconnect.apps.playbooks.test.config.PlaybooksTestConfiguration;
import com.threatconnect.apps.playbooks.test.orc.PlaybooksOrchestrationBuilder;
import org.junit.Before;
import org.junit.Test;

public class UUIDGeneratorAppTest {
    @Before
    public void setUp()
    {
        //register the inmemory database
        PlaybooksTestConfiguration.getInstance().registerEmbeddedDBService();

        //Get the global config
        AppConfig ac = PlaybooksTestConfiguration.getInstance().getGlobalAppConfig();

        //doesn't drive anything during junit test as there is a log4j2.xml file existing in playbooks-test
        //that sets the global level to info which you can change if needed for testing.
        ac.set(AppConfig.TC_LOG_LEVEL, "debug");

        //set base params
        ac.set(AppConfig.TC_TEMP_PATH, "./AppOutput");
        ac.set(AppConfig.TC_LOG_PATH,  "./AppOutput");
        ac.set(AppConfig.TC_OUT_PATH,  "./AppOutput");
        ac.set(AppConfig.TC_API_PATH,  "https://localhost:8443/api");

    }

    @Test
    public void testVersion1() throws Exception
    {
        PlaybooksOrchestrationBuilder.runApp(UUIDGeneratorApp.class)
                .withAppParam()
                .set(UUIDGeneratorApp.INPUT_VERSION, "1")
                .then().onSuccess().assertOutput()
                .assertNotNull(UUIDGeneratorApp.OUTPUT_UUID, StandardPlaybookType.String)
                .assertMessageTcContains("Successfully generated UUID.")
                .runTest(UUIDGeneratorApp.OUTPUT_UUID, StandardPlaybookType.String, o -> {
                    System.out.println(o);
                    return true;
                })
                .then().build().run();
    }

    @Test
    public void testVersion3() throws Exception
    {
        PlaybooksOrchestrationBuilder.runApp(UUIDGeneratorApp.class)
                .withAppParam()
                .set(UUIDGeneratorApp.INPUT_VERSION, "3")
                .then()
                .withPlaybookParam()
                .asString(UUIDGeneratorApp.INPUT_NAMESPACE, "63475079-2605-11e8-a408-27f70ff2806d")
                .asString(UUIDGeneratorApp.INPUT_NAME, "foobar")
                .then().onSuccess().assertOutput()
                .assertNotNull(UUIDGeneratorApp.OUTPUT_UUID, StandardPlaybookType.String)
                .assertEquals(UUIDGeneratorApp.OUTPUT_UUID, StandardPlaybookType.String, "8ee110a3-4998-3fe1-b47e-61e897ff1832")
                .assertMessageTcContains("Successfully generated UUID.")
                .then().build().run();
    }

    @Test
    public void testVersion5() throws Exception
    {
        PlaybooksOrchestrationBuilder.runApp(UUIDGeneratorApp.class)
                .withAppParam()
                .set(UUIDGeneratorApp.INPUT_VERSION, "5")
                .then()
                .withPlaybookParam()
                .asString(UUIDGeneratorApp.INPUT_NAMESPACE, "63475079-2605-11e8-a408-27f70ff2806d")
                .asString(UUIDGeneratorApp.INPUT_NAME, "foobar")
                .then().onSuccess().assertOutput()
                .assertNotNull(UUIDGeneratorApp.OUTPUT_UUID, StandardPlaybookType.String)
                .assertEquals(UUIDGeneratorApp.OUTPUT_UUID, StandardPlaybookType.String, "b8b3c9a4-fc0c-509e-881d-8f87ab349360")
                .assertMessageTcContains("Successfully generated UUID.")
                .runTest(UUIDGeneratorApp.OUTPUT_UUID, StandardPlaybookType.String, o -> {
                    System.out.println(o);
                    return true;
                })
                .then().build().run();
    }

    @Test
    public void testVersion4() throws Exception
    {
        PlaybooksOrchestrationBuilder.runApp(UUIDGeneratorApp.class)
                .withAppParam()
                .set(UUIDGeneratorApp.INPUT_VERSION, "4")
                .then().onSuccess().assertOutput()
                .assertNotNull(UUIDGeneratorApp.OUTPUT_UUID, StandardPlaybookType.String)
                .assertMessageTcContains("Successfully generated UUID.")
                .runTest(UUIDGeneratorApp.OUTPUT_UUID, StandardPlaybookType.String, o -> {
                    System.out.println(o);
                    return true;
                })
                .then().build().run();
    }

    @Test
    public void testVersion3NoNamespace() throws Exception
    {
        PlaybooksOrchestrationBuilder.runApp(UUIDGeneratorApp.class)
                .withAppParam()
                .set(UUIDGeneratorApp.INPUT_VERSION, "3")
                .then()
                .withPlaybookParam()
                .asString(UUIDGeneratorApp.INPUT_NAME, "foobar")
                .then()
                .onFailure()
                .assertOutput()
                .assertMessageTcContains("Namespace must be given for UUID versions 3 and 5.")
                .then().build().run();
    }

    @Test
    public void testVersion3NoName() throws Exception
    {
        PlaybooksOrchestrationBuilder.runApp(UUIDGeneratorApp.class)
                .withAppParam()
                .set(UUIDGeneratorApp.INPUT_VERSION, "3")
                .then()
                .withPlaybookParam()
                .asString(UUIDGeneratorApp.INPUT_NAMESPACE, "63475079-2605-11e8-a408-27f70ff2806d")
                .then()
                .onFailure()
                .assertOutput()
                .assertMessageTcContains("Name must be given for UUID versions 3 and 5.")
                .then().build().run();
    }

    @Test
    public void testVersion3BadNameSpace() throws Exception
    {
        PlaybooksOrchestrationBuilder.runApp(UUIDGeneratorApp.class)
                .withAppParam()
                .set(UUIDGeneratorApp.INPUT_VERSION, "3")
                .then()
                .withPlaybookParam()
                .asString(UUIDGeneratorApp.INPUT_NAME, "foobar")
                .asString(UUIDGeneratorApp.INPUT_NAMESPACE, "63475079-2605-11e8-a408-27")
                .then()
                .onFailure()
                .assertOutput()
                .assertMessageTcContains("Namespace is not valid.")
                .then().build().run();
    }

    @Test
    public void testVersion5NoNamespace() throws Exception
    {
        PlaybooksOrchestrationBuilder.runApp(UUIDGeneratorApp.class)
                .withAppParam()
                .set(UUIDGeneratorApp.INPUT_VERSION, "5")
                .then()
                .withPlaybookParam()
                .asString(UUIDGeneratorApp.INPUT_NAME, "foobar")
                .then()
                .onFailure()
                .assertOutput()
                .assertMessageTcContains("Namespace must be given for UUID versions 3 and 5.")
                .then().build().run();
    }

    @Test
    public void testVersion5NoName() throws Exception
    {
        PlaybooksOrchestrationBuilder.runApp(UUIDGeneratorApp.class)
                .withAppParam()
                .set(UUIDGeneratorApp.INPUT_VERSION, "5")
                .then()
                .withPlaybookParam()
                .asString(UUIDGeneratorApp.INPUT_NAMESPACE, "63475079-2605-11e8-a408-27f70ff2806d")
                .then()
                .onFailure()
                .assertOutput()
                .assertMessageTcContains("Name must be given for UUID versions 3 and 5.")
                .then().build().run();
    }

    @Test
    public void testVersion5BadNameSpace() throws Exception
    {
        PlaybooksOrchestrationBuilder.runApp(UUIDGeneratorApp.class)
                .withAppParam()
                .set(UUIDGeneratorApp.INPUT_VERSION, "5")
                .then()
                .withPlaybookParam()
                .asString(UUIDGeneratorApp.INPUT_NAME, "foobar")
                .asString(UUIDGeneratorApp.INPUT_NAMESPACE, "63475079-2605-11e8-a408-27")
                .then()
                .onFailure()
                .assertOutput()
                .assertMessageTcContains("Namespace is not valid.")
                .then().build().run();
    }
}
