# Playbooks Contribution Guide

Contributing to the ThreatConnect Playbooks Github repository is a powerful and scalable way to make a positive impact to the infosec community. At ThreatConnect, we believe that Threat Intelligence can have a visible impact on your company’s success, and that orchestration and automation is a force multiplier for Threat Intelligence.

## Guidelines

+ All Playbooks, Components, and Playbook Apps must have their own README.md files.
  + Playbooks README.md should include the following headers:
    + Summary
    + App Dependencies
    + Use Cases (Optional)
  + Playbook Apps and Components README.md should include the following headers:
    + Summary
    + Dependencies
    + Input Definitions
    + Output Definitions
    + Use Cases (Optional)
+ Playbooks, Components, and Playbook Apps should be included in unique, separate folders.
  + Playbooks and Components must include the PBX file of the Playbook or Component.
  + Playbook Apps must include the zip/tcx file of the App.

## Contributing Playbooks

Playbooks are stored in JSON as PBX files, which allows them to be easily shared between instances of ThreatConnect.

In order to contribute a Playbook, first Export the Playbook as a PBX file from your instance of ThreatConnect, then create a Pull request. To modify or use the Playbook in your instance, click the “Import Playbook” button and select the appropriate PBX file.

## Contributing Playbook Components

A Playbook Component is a special type of Playbook that's designed to be executed inside another Playbook; in many ways, it's like an app that's built using Playbooks instead of the ThreatConnect App Framework. Like Playbooks, Components are stored in JSON as PBX files. Components take input variables as parameters and return output variables (like a function or method).

## Contributing Playbook Apps

A Playbook App is a single component of a Playbook. These Apps are intended to be reusable, standalone elements with minimum functionality to solve a single purpose. Multiple Playbook Apps will make up a Playbook that solves a use case.

## Contribution Best Practices

**Give your Playbook, Component, and App a descriptive name.** There are hundreds of Playbooks, Components, and Apps, so it's important that the name is notable and references key functions and/or integrations. For example, "Triage" is bad, "Email Triage" is better, "VirusTotal Email Triage" is awesome, and "VirusTotal Email Triage & Detonation - Host, Address, and Mutex Ingestion" is best.

**Include a description in the Playbook, Component, or App.** Just like commenting in code, this helps other users better understand the purpose of your contribution and how to use it most effectively in their environment.

If you have any feedback, please open an Issue in this repo. For general questions, please contact support@threatconnect.com.
