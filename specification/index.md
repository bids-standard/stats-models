BIDS Stats Models
=================

*A specification for neuroimaging statistical models.*

*BIDS Stats Models* (BSM) describe how to fit *statistical models for neuroimaging data* using *a machine-readable JSON document*.  Its purpose is prescriptive (e.g. a recipe), rather than descriptive (e.g. summary of already fit models). 

A *BSM*—in combination with a preprocessed BIDS dataset—is sufficient to execute statistical models, with minimal configuration and intervention required from the user.

The **mission** of *BSM* is to promote scientific best practice by making neuroimaging models *transparent and reproducible*, as well as encourging the development of *standardized and automated* statistical analysis pipelines.

:::{panels}
:column: col-lg-6 px-2 py-2
---
**Learn more**
^^^
**[](motivation.md)**: Why do we need *BSM*?

**[](walkthrough.rst)**: Step-by-step introduction

**[Specification](reference.rst)**: Dive into the technical reference

---
**Get started**
^^^
**[](model-zoo.md)**: View example models on public datasets, and modify them to your own data

**[Default model](default_model.md)**: How to create a simple model
:::
## Acknowledments

BIDS Stats Models is supported by by NIH award R01MH109682, and is part of the [Brain Imaging Data Standard (BIDS)](https://bids.neuroimaging.io/index.html) community.
