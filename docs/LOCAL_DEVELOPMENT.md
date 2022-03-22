## Local Development

### Pre-Requisites
The following dependencies must be installed. Please refer to your operating system, how to install them.

> **Note:** For Windows 10, we recommend enabling Windows Subsystem for Linux (WSL) and installing Linux distribution of your choice,
> for example, here are the instructions on how to install [Ubuntu](https://ubuntu.com/tutorials/ubuntu-on-windows).

- Python >=3.8 and pip
- VirtualEnv
- Go
- Ruby >=2.6 and gem
- [cfn-nag](https://github.com/stelligent/cfn_nag)

Here is an example how to install pre-requisites on macOS/Linux using [Homebrew](https://brew.sh/).
```shell
# install python3
brew install python

# install VirtualEnv
pip3 install virtualenv

# install go
brew install go

# install ruby, gem and cfn-nag
brew install ruby brew-gem
brew gem install cfn-nag
```

### Build local development environment
Once you have installed pre-requisites, run commands below:

#### Step 1 - Clone the repository (Required)
In the first step, you will clone the repository.

1. Clone the repository:
   ```shell
   $ git clone https://github.com/aws-samples/aws-iot-smart-wastebin-solution.git
   ```

#### Step 2 - `make init` (Required)
In the second step, you will use `make` to create a virtual environment.

1. Initialize the local environment
   ```shell
   make init
   ```
1. Activate `VirtualEnv` environment.
   ```shell
   source venv/bin/activate
   ```
1. Run pre-commit tests for the first time to check the installation.
   ```shell
   make test
   ```

#### Step 2 - `make config` (Required)
In the second step you will create configuration file for your deployment. The command will,
set the stack name, AWS region and bucket name.

1. Run configuration command
   ```shell
   make config
   ```
1. Set AWS Region, for example us-east-1
   ```shell
   AWS Region to create bucket in (e.g. us-east-1)?: us-east-1
   ```
1. Set the bucket name, for example my-unique-bucket-name (the name has to be unique)
   ```shell
   S3 Bucket name (e.g. s3-bucket-name)?: my-unique-bucket-name
   ```
1. Set the project name, for example aws-iot-wastebin
   ```shell
   CloudFormation Stack name (e.g. my-project-name)?: aws-iot-wastebin
   ```
1. This will create and populate `config.mk` file
   ```shell
   AWS_REGION=us-east-1
   BUCKET_NAME=my-unique-bucket-name
   STACK_NAME=aws-iot-wastebin
   ```
> Note: You can change these values manually in the `config.mk` file. You can change any variables generated and
> replace with own values. Also, here is the good place to add your template overrides.

#### Step 3 - `make bucket` (Optional)
In this step, you can create S3 bucket where you will store all your assets, such as CloudFormation templates, Lambda
functions and any other project related stuff. This step is optional as you may already have a bucket for development.

1. Create bucket
   ```shell
   make bucket
   ```

#### Step 4 - `make deploy`
In the last step, you will deploy your infrastructure with CloudFormation. The `make deploy` command will **build** your libraries,
**package** the templates and lambda functions and **deploy** it in your AWS account.

1. Deploy CloudFormation
   ```shell
   make deploy
   ```

### Testing(Automated and Manual)
The repository has a GitHub actions set up which will run `cfn-lint` and `cfn-nag` tests on pull requests.

Furthermore, pre-commit configuration file is provided to format the code and content. See below various tests you can
run locally.

* `make test` - will run pre-commit tests. Useful to run before committing changes.
* `make lint` - will run cfn-lint test against CloudFormation templates in `/cfn/`.
* `make nag` - will run cfn-nag test against CloudFormation templates in `/cfn/`.

## Troubleshooting
If you get an error installing rain
```shell
[INFO] Installing environment for https://github.com/aws-cloudformation/rain.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
An unexpected error has occurred: CalledProcessError: command:...
```

The default **proxy.golang.org** is blocked on your network. To fix it, run:
```shell
export GOPROXY=direct
```
