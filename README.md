# Terraform render - a collection of unit tests for terraform module

## General info
Testing is an essential element to highly effective DevOps practices, and testing your infrastructure code provides benefits such as ensuring that you will create exactly the resources you expect in the AWS cloud and helping to prevent regressions from being introduced to your infrastructure.

### Fine-grained Assertions
The assertions module provides several tools to both assert that certain parts of a template matches given objects and to retrieve certain parts of of a template. Using these tools, we can assert that resources with a given type and properties exist, assert that certain outputs exist, and assert that a template has a given number of resources.
Fine-grained assertions is a good mechanism to detect regressions.

### Snapshot Testing 
Snapshot tests take a snapshot of an object the first time they run. This snapshot is committed to version control, and every time the test is run after that, the object is compared to the snapshot. If the snapshot matches the object, the assertion passes. If the snapshot does not match, the assertion fails.
Snapshot testing is best used as a mechanism to alert you when anything at all changes in your TF stacks. Snapshot testing will make these changes visible to you early.
Refactoring your TF code is another good use of snapshot testing — you don’t want anything to change while you’re refactoring, and snapshot tests will clearly show you when that happens. For almost all other use cases, fine-grained assertions are a better tool.

## Prerequisites
- Terraform v0.12+
- Python v3.8+
- pipenv
- aws cli

## Usage

### Install
```bash
git clone
cd terraform-render
make install
```

### Build
```bash
cd terraform-render
make build
```

### Test
```bash
cd terraform-render
make test
```
