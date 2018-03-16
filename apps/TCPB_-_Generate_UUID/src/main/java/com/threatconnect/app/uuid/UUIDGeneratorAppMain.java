package com.threatconnect.app.uuid;

import com.threatconnect.app.apps.App;
import com.threatconnect.app.apps.AppConfig;
import com.threatconnect.sdk.app.AppMain;

public class UUIDGeneratorAppMain extends AppMain {
    @Override
    public Class<? extends App> getAppClassToExecute(final AppConfig appConfig) throws ClassNotFoundException
    {
        return UUIDGeneratorApp.class;
    }

    public static void main(String[] args)
    {
        new UUIDGeneratorAppMain().execute();
    }
}
