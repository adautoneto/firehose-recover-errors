# Recover Firehose Error Files

If you have a Kinesis Firehose setup to send incomding data to Redshift, and at some point that copy failed for any reason, the delivery stream will keep saving the data in S3 and creating [MANIFEST](https://docs.aws.amazon.com/redshift/latest/dg/loading-data-files-using-manifest.html) files point to the files  that failed to be copied.

Since there could be a lot of manifest files, manually running the [COPY](https://docs.aws.amazon.com/redshift/latest/dg/tutorial-loading-run-copy.html) command to each of them may not be a good solution. That's why this repository has been created.



## Pre-requisites:

1. AWS Cli
2. Docker or Python3



## Getting the manifests file

This will work as index of manifest files you want to reprocess.

Using AWS Cli, run the following command:

`aws s3api list-objects-v2 --bucket <bucket> --prefix "<prefix>" --query "Contents[].[Key]" --output text > manifests.txt`

This will print only the filenames in S3 and save them into a file called manifests.txt.

The parameters are:

- `<bucket>`: the S3 bucket where your data are located 
- `<prefix>`: The path within the bucket, e.g.: `ses-logs/errors/manifests/2020/03`



## Configuring the application

Clone this repository and place the _manifests.txt_ file created previously in the same folder of the cloned files.

Change the _firehose.yaml_ configuration file appropriately. You will need to set the Redshift connection parameters and the COPY paramenters (which you can find in your Firehose Delivery stream settings).



## Running with Docker

The docker image will make it easier to setup the environment to run the COPY commands. 



### Building the image

Run this command to build the image:

`docker build -t <name> .` 

where the _name_ parameter is the name of the docker container. It can be anything.



### Running the application

To run the application using Docker, execute the following command:

```bash
docker run -it --rm --name my-running-app -v "$PWD":/usr/src/myapp -w /usr/src/myapp <image_name>
```

replacing the parameter _image_name_ with the name used in the previous step. 

The application will show the commands it's sending to Redshift, and stop once it's finished.



## Running with Python

In case you don't want to run the application using Docker, you can run it with Python by yourself.

Install the necessary libraries by running:

`pip install --no-cache-dir -r requirements.txt`

and execute the application by running:

`python ./load_manifests.py`