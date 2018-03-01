# Univa GridEngine #

This project installs and configures Univa GridEngine.   The project includes a basic UGE template as a sample, but is intended to be used to add UGE as the scheduler for production cluster types.

Use of this Univa GridEngine project requires a license agreement and GridEngine binaries obtained directly 
from [Univa Corporation](http://www.univa.com/products/).

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->

**Table of Contents**

- [Univa GridEngine](#univa-gridengine)
    - [Pre-Requisites](#pre-requisites)
    - [Configuring the Project](#configuring-the-project)
    - [Deploying the Project](#deploying-the-project)
    - [Importing the Cluster Template](#importing-the-cluster-template)
    - [Using the Project Specs in Other Clusters](#using-the-project-specs-in-other-clusters)
        - [Helper Specs](#helper-specs)

<!-- markdown-toc end -->


## Pre-Requisites ##


This project requires the following:

  1. A license to use Univa GridEngine from [Univa Corporation](http://www.univa.com/products/).
  
  2. The Univa GridEngine installation binaries.
  
      - Download the binaries from Univa Corporation and place them in the `./blobs/` directory.
      - Download the `${version}-bin-lx-amd64.tar.gz`, `${version}-bin-ulx-amd64.tar.gz`, `${version}-common.tar.gz` files. For example, if the Univa version you are using is 8.5.0, download the following files: `ge-8.5.0-bin-lx-amd64.tar.gz`, `ge-8.5.0-bin-ulx-amd64.tar.gz`, and `ge-8.5.0-common.tar.gz`
      - If the version is not 8.5.0 (the project default), then update the version number in the Files list in `./project.ini` and in the cluster template `./templates/gridengine_template.txt`
     
  3. CycleCloud must be installed and running.

     a. If this is not the case, see the CycleCloud QuickStart Guide for
        assistance.

  4. The CycleCloud CLI must be installed and configured for use.

  5. You must have login access to CycleCloud.

  6. You must have access to upload data and launch instances in your chosen
     Cloud Provider account.

  7. You must have access to a configured CycleCloud "Locker" for Project Storage
     (Cluster-Init and Chef).

  8. Optional: To use the `cyclecloud project upload <locker>` command, you must
     have a Pogo configuration file set up with write-access to your locker.

     a. You may use your preferred tool to interact with your storage "Locker"
        instead.


## Configuring the Project ##


The first step is to configure the project for use with your storage locker:

  1. Open a terminal session with the CycleCloud CLI enabled.

  2. Switch to the gridengine directory.

  3. Copy the following installers to `./blobs`
    * ge-8.5.0-bin-lx-amd64.tar.gz
    * ge-8.5.0-bin-ulx-amd64.tar.gz
    * ge-8.5.0-common.tar.gz
    
  4. If the version number is not 8.5.0, update the version numbers in `project.ini` and `templates/gridengine_template.txt`
    

## Deploying the Project ##


To upload the project (including any local changes) to your target locker, run the
`cyclecloud project upload` command from the project directory.  The expected output looks like
this:

``` bash

   $ cyclecloud project upload my_locker
   Sync completed!

```


**IMPORTANT**

For the upload to succeed, you must have a valid Pogo configuration for your target Locker.


## Importing the Cluster Template ##


To import the cluster:

 1. Open a terminal session with the CycleCloud CLI enabled.

 2. Switch to the gridengine directory.

 3. Run ``cyclecloud import_template uge -f templates/gridengine_template.txt``.
    The expected output looks like this:
    
    ``` bash
    
    $ cyclecloud import_template uge -f templates/gridengine_template.txt
    Importing template uge....
    ----------------
    uge : *template*
    ----------------
    Keypair: $awsKeypair
    Cluster nodes:
        master: off
    Total nodes: 1
    ```


## Using the Project Specs in Other Clusters ##

The only *required* spec is the `gridengine:default` spec.   The default spec should be applied to `[[node defaults]]`:

``` ini
    [[node defaults]]
    ...
        [[[configuration]]]
        gridengine.make = ge
        gridengine.version = 8.5.0
        gridengine.root = /sched/ge/ge-8.5.0
    
        [[[cluster-init gridengine:default:1.0.0]]]

```

To convert an existing SGE cluster template (such as the CycleCloud `sge_template.txt` sample) to use UGE, simply add the changes above to the `[[node defaults]]` section.

### Helper Specs ###

For new clusters (that are not already using the default SGE roles), the project includes 2 additional helper specs that may be used to avoid remembering how to set up the Chef run_list: 

  * **master** : provides the chef roles required to configure a GridEngine Master node
  * **execute** : provides the chef roles required to configure a GridEngine Execute / Worker node
  
  
For new clusters using the gridengine project, no run_list modifications are required if the QMaster node includes the master spec: and the execute node type includes the execute spec:

``` ini
    [[node defaults]]
    ...
        [[[configuration]]]
        gridengine.make = ge
        gridengine.version = 8.5.0
        gridengine.root = /sched/ge/ge-8.5.0
    
        [[[cluster-init gridengine:default:1.0.0]]]

    [[node master]]
    ...
        [[[cluster-init gridengine:master:1.0.0]]]

    [[nodearray execute]]
    ...
        [[[cluster-init gridengine:execute:1.0.0]]]

```

In this case, no explicit Chef `run_list` is required.
