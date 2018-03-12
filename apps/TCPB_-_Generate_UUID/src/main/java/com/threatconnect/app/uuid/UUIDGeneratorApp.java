package com.threatconnect.app.uuid;

import com.fasterxml.uuid.Generators;
import com.fasterxml.uuid.impl.UUIDUtil;
import com.threatconnect.app.addons.util.config.install.StandardPlaybookType;
import com.threatconnect.app.apps.ExitStatus;
import com.threatconnect.app.playbooks.app.PlaybooksApp;
import com.threatconnect.app.playbooks.app.PlaybooksAppConfig;
import com.threatconnect.app.playbooks.content.accumulator.ContentException;
import org.slf4j.LoggerFactory;

import java.security.MessageDigest;
import java.util.UUID;

/**
 * Playbook app that generates a UUID.
 *
 * @author Chris Blades
 * @version 1.0.0
 */
public class UUIDGeneratorApp extends PlaybooksApp {
    static final String INPUT_VERSION = "uuid_version";
    static final String INPUT_NAMESPACE = "uuid_namespace";
    static final String INPUT_NAME = "uuid_name";
    static final String OUTPUT_UUID = "uuid";

    protected static final org.slf4j.Logger logger = LoggerFactory.getLogger(UUIDGeneratorApp.class);

    @Override
    protected ExitStatus execute(PlaybooksAppConfig playbooksAppConfig) throws Exception {
        int uuidVersion = Integer.parseInt(
                playbooksAppConfig.getAppConfig().getString(INPUT_VERSION));

        String uuid = null;
        MessageDigest messageDigest = null;
        UUID namespace = null;
        try {
            switch (uuidVersion) {
                case 1:
                    uuid = Generators.timeBasedGenerator().generate().toString();
                    break;
                case 3:
                    messageDigest = MessageDigest.getInstance("MD5");
                    uuid = Generators.nameBasedGenerator(readNamespace(), messageDigest)
                            .generate(readName())
                            .toString();
                    break;
                case 4:
                    uuid = Generators.randomBasedGenerator().generate().toString();
                    break;
                case 5:
                    messageDigest = MessageDigest.getInstance("SHA-1");
                    uuid = Generators.nameBasedGenerator(readNamespace(), messageDigest)
                            .generate(readName())
                            .toString();
                    break;
            }
        } catch (ContentException e) {
            writeMessageTc(e.getMessage());
            return ExitStatus.Failure;
        }

        if (isOutputParamExpected(OUTPUT_UUID, StandardPlaybookType.String)) {
            writeStringContent(OUTPUT_UUID, uuid);
        }

        writeMessageTc("Successfully generated UUID.");
        return ExitStatus.Success;
    }

    private UUID readNamespace() throws ContentException {
        try {
            String namespace = readStringContent(INPUT_NAMESPACE);
            if (namespace == null) {
                throw new ContentException("Namespace must be given for UUID versions 3 and 5.");
            }
            return UUIDUtil.uuid(namespace);
        } catch (ContentException e) {
            logger.error("Error reading namespace.", e);
            throw new ContentException("Namespace must be given for UUID versions 3 and 5.");
        } catch (Exception e) {
            logger.error("Error reading namespace.", e);
            throw new ContentException("Namespace is not valid.");

        }
    }

    private String readName() throws ContentException {
        try {
            String name = readStringContent(INPUT_NAME);
            if (name == null) {
                throw new ContentException("");
            }

            return name;
        } catch (ContentException e) {
            logger.error("Error reading name.", e);
            throw new ContentException("Name must be given for UUID versions 3 and 5.");
        }
    }
}
