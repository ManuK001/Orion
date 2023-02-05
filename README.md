# Orion

This is the source code and artefact of the research paper titled "A History-driven Fuzzing of Deep Learning Libraries. 

# How Orion works?

Orion is a hybrid fuzzer that combines determinism and randomization to produce inputs to deep learning APIs based on faulty data, which has previously been identified as the fundamental source of security issues. Orion analyses historical data from open-source security records to provide a set of flawed input-generating rules to guide its fuzzer generator. It collects APIs from three major sources: API reference documents, library test suites, and public repositories that employ DL APIs. Orion executes its fuzzing on the well-known and extensively used TensorFlow and PyTorch libraries. Orion instruments the API value and argument space and fuzz the input space using the instrumentation data.

# Getting start with Orion

The following sections help you to run Orion and find bugs in TensorFlow and PyTorch. It is highly recommended that to use UNIX-based operating systems
to test and run Orion, preferebly ubuntu-22.04. 

:o: Orion is a test case generator. It generate test cases that may harm SUT or even the while platform. Orion may generate test cases that freez your operating system. Please try to run Orion on completely isolated environment. It is highly recommended. :o:

## Requirements

You need the following dependencies to be able to run Orion:

### Python dependencies
```
inspect
git
selenium
beautiful-soup
requests
pandas
numpy
pymongo
```
You need the following releases of TensorFlow and PyTorch:

```
Tensorflow v2.3.0
Tensorflow v2.4.0
Tensorflow v2.10.0
Tensorflow v2.11.0
Pytorch v1.7.0
Pytorch v1.8.0
Pytorch v1.12.0
Pytorch v1.13.1
```

It is highly recommended that you create a single virtual environment for each release. It is better to make the running environment independent from
each other.

### System dependencies
```
mongodb
conda
```

## Collecting API

One of the significant features of Orion is that it can perform fuzzing on internal TensorFlow APIs. Also, it is able to perform fuzzing on high-level APIs for both TensorFlow and PyTorch. TensorFlow internal APIs are not often used by end-users, instead they are being actively used by developers to test downstream functionalities of TensorFlow. 

First, you need to clone the Orion's repository:

```
git clone https://github.com/dmc1778/Orion.git
```
Then change directory to Orion's root directory. 

### High-level APIs

To collect high-level API names, we use [beautiful-soup](https://beautiful-soup-4.readthedocs.io/en/latest/) package to scrape API reference documentation page of TensorFlow and PyTorch. You need change directory to ```scrapers``` folder located in the root directory to collect API names:


```
python scrape.py
```

### Internal APIs

## Instrumentation

### High-level APIs

### Internal APIs

## Fuzzing

# Bug list

Please find our bug list [here](https://docs.google.com/spreadsheets/d/1O846GErh1TIWwXzvEqcUOSl49u-mcHwk8_IttVZXunc/edit?usp=sharing).
