# Blue Canary - An AWS CloudWatch Metric Alarm Automation Suite

## Installation

Blue Canary supports Python 3 and can be installed via pip:

```
$ pip install blue-canary
```

## Usage

Blue Canary currently supports two commands:   
update_tags   
update_alarms   

__update_tags__:   
update_tags will tag each resource with the given key/value pair.

__update_alarms__:
update_alarms will create and/or update alarms for any resource in your AWS account that matches your specified key/value tags.   

**Example usage**:
```
$ bluecanary update_tags -p /path/to/config/ -v
```

### Parameters

Both update_tags and update_alarms accept the following parameters and options:

--path (-p): Path to yaml file or directory.  If a directory, Blue Canary will recursively load any yaml files in the directory.  May be provided multiple times to specify multiple files or directories.

--verbose (-v): Enable verbose output.  Add the flag multiple times for additional output (.eg -vv, -vvv)

## Configuration

To use Blue Canary you must set up authentication credentials.  AWS credentials are configured in the [IAM Console](https://console.aws.amazon.com/iam/home).  Once you have a set of valid AWS credentials.  You can set them up in several ways:

1.) Credentials Files

You can set up credentials in ~/.aws/credentials and regions in ~/.aws/config

~/.aws/credentials
```
[default]
aws_access_key_id = <<YOUR_ACCESS_KEY>>
aws_secret_access_key = <<YOUR_SECRET_KEY>>
```

~/.aws/config
```
[default]
region=us-east-1
```

2.) Environment Variables

```
$ export AWS_ACCESS_KEY_ID=<<YOUR_ACCESS_KEY>>
$ export AWS_SECRET_ACCESS_KEY=<<YOUR_SECRET_KEY>>
$ export AWS_DEFAULT_REGION=us-east-1
```

3.) Within Blue Canary configuration files.  See the Setup section below.

## Setup

Blue Canary is configured via yaml files.  There are 4 sections:

1.) Configuration:   
Currently used to configured the locations of additional alarm plugins.   
2.) AWSProfiles:   
If you do not wish to store AWS credentials in ~/.aws/credentials or environment variables, you can define them here.   
3.) AlarmGroups:   
Definitions of suites of alarms to be created/applied to any resources that match the specified tag/value combonation.   
4.) TagGroups:   
Lists of resources to be tagged with the given tag/value combonation.   

/example/blue-canary-configuration.yaml
```
---
Configuration:
  Plugins:
    - /path/to/additional/alarm/plugins
AWSProfiles:
  -
    AWS_PROFILE: <<profile name>>
    AWS_ACCESS_KEY_ID: <<aws access key>>
    AWS_SECRET_ACCESS_KEY: <<aws secret key>>
    AWS_DEFAULT_REGION: <<aws region>>
AlarmGroups:
  -
    AWSProfile: example_profile
    TagKey: <<aws ec2 tag key>>
    TagValue: <<aws tag value>>
    Alarms:
      -
        MetricName: CPUUtilization
        Statistic: Average
        Period: 60
        EvaluationPeriods: 5
        Threshold: 90.0
        ComparisonOperator: GreaterThanOrEqualToThreshold
        AlarmActions:
          - <<aws arn identifier>>
        Namespace: AWS/EC2
  -
    AWSProfile: another_example_profile
    TagKey: <<aws elb tag key>>
    TagValue: <<aws elb tag value)
    Alarms:
      -
        MetricName: Latency
        Statistic: Average
        Period: 60
        EvaluationPeriods: 5
        Threshold: 5.0
        ComparisonOperator: GreaterThanThreshold
        AlarmActions:
          - <<aws arn identifier>>
        Namespace: AWS/ELB
TagGroups:
  -
    Profile: example_profile
    TagKey: <<aws ec2 tag key>>
    TagValue: <<aws ec2 tag value>>
    Type: EC2
    Resources:
      - i-12345678
  -
    AWSProfile: another_example_profile
    TagKey: <<aws elb tag key>>
    TagValue: <<aws elb tag value>>
    Type: ELB
    Resources:
      - example-load-balancer
```

## Development

### Getting Set Up

Assuming you already have Python 3 installed you can set up Blue Canary by cloning from GitHub:

```
$ git clone https://github.com/voxy/blue-canary.git
$ cd blue-canary
$ virtualenv venv
$ source venv/bin/activate
$ make develop
```

### Running Tests

```
$ make test
```

or 

```
$ make test-with-coverage
```
