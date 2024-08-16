# JSON-LD Representations of CityJSON

This repository contains the resources and documentation related to the master's thesis titled "JSON-LD Representations of CityJSON". The aim of this project is to explore the conversion of CityJSON data into JSON-LD format, facilitating semantic web integration and interoperability with other linked data sources.

## Contents

1. [Introduction](#introduction)
2. [Ontology](#ontology)
3. [SHACL Shapes](#shacl-shapes)
4. [Examples](#examples)
5. [Code](#code)
   
## Introduction

CityJSON is a format for encoding 3D city models in a compact and easily readable JSON format. However, to enable better integration with the semantic web and to harness the benefits of linked data, there's a need to represent CityJSON data using JSON-LD. This master's thesis project aims to address this need by developing a methodology for transforming CityJSON into JSON-LD representations.

## Ontology

The ontology developed in this project serves as a conceptual framework for representing CityJSON data using JSON-LD. It defines the classes, properties, and relationships necessary to describe urban features and their attributes in a semantically rich manner. The ontology is available in the [ontology folder](Ontology/) of this repository.

## SHACL Shapes

To ensure the validity and consistency of the JSON-LD representations, SHACL (Shapes Constraint Language) shapes are provided. These shapes define the constraints and validation rules that the JSON-LD data must adhere to. The SHACL shapes can be found in the [shacl folder](SHACL/) of this repository.

## Examples

JSON-LD/Turtle representations of CityJSON data are provided to demonstrate the practical application of the ontology and SHACL shapes. These examples illustrate how different urban features and their attributes can be represented using JSON-LD/Turtle. You can explore the examples in the [examples folder](Examples/) of this repository.

## Code

This section contains the implementation code used in the conversion of CityJSON data to JSON-LD. You can explore the code in the [Code folder](Code/src) of this repository.

## Demo

A demo is provided to showcase how to use the CityJSON to JSON-LD and the conversion process. The demo can be found in the [Demo Folder](Demo/) of this repository.

## Case Studies

Two case studies were conducted to demonstrate the practical application of the CityJSON to JSON-LD conversion process:

1. **Helsinki**:
   - **[Helsinki Case Study Code](Case%20Study/Helsinki)**
   - **[Helsinki Data](Code/src/data/helsinki.city.json)**
   
2. **New York**: 

   - **[New York Case Study Code](Case%20Study/NYC)**
   - **[New York Data](https://3d.bk.tudelft.nl/opendata/cityjson/3dcities/v2.0/DA13_3D_Buildings_Merged.city.json)**




